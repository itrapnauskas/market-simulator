"""Detection helpers that operate on market states."""

from __future__ import annotations

from typing import Sequence

from ..core.market import MarketState
from ..core.orders import OrderCurves
from .metrics import rolling_zscore


def compute_price_volume_anomaly(states: Sequence[MarketState], window: int = 20) -> list[float]:
    """
    Calcula pontuação de anomalia combinando z-scores de preço e volume.

    Detecta comportamento anormal no mercado analisando desvios estatísticos
    tanto no preço quanto no volume negociado. Usa rolling z-scores para
    capturar anomalias relativas ao histórico recente.

    Args:
        states: Sequência de estados do mercado para análise
        window: Tamanho da janela deslizante para cálculo dos z-scores (padrão: 20)

    Returns:
        Lista de scores de anomalia, um por dia, onde valores maiores indicam
        comportamento mais anormal. Score = |z_price| + |z_volume|

    Example:
        >>> states = runner.run(n_days=100)
        >>> anomaly_scores = compute_price_volume_anomaly(states, window=20)
        >>> max_anomaly_day = anomaly_scores.index(max(anomaly_scores))
        >>> print(f"Maior anomalia no dia {max_anomaly_day}")
    """

    prices = [state.price for state in states]
    volumes = [state.volume for state in states]
    price_z = rolling_zscore(prices, window=window)
    volume_z = rolling_zscore(volumes, window=window)
    return [abs(p) + abs(v) for p, v in zip(price_z, volume_z, strict=False)]


def curve_imbalance_score(order_curves: OrderCurves | None) -> float:
    """
    Mede o desequilíbrio entre curvas de demanda e oferta para um único dia.

    Calcula uma métrica de assimetria entre buy_curve e sell_curve. Desequilíbrios
    grandes podem indicar pressão de compra/venda artificial ou manipulação.

    Args:
        order_curves: Curvas de ordens para um dia específico, ou None

    Returns:
        Score de desequilíbrio normalizado. Zero se order_curves for None ou vazio.
        Valores maiores indicam maior desequilíbrio entre oferta e demanda.

    Example:
        >>> state = states[42]
        >>> imbalance = curve_imbalance_score(state.order_curves)
        >>> if imbalance > 2.0:
        ...     print("Possível manipulação detectada")
    """

    if order_curves is None:
        return 0.0
    buy = order_curves.buy_curve
    sell = order_curves.sell_curve
    if not buy or not sell:
        return 0.0
    diff_sum = sum(abs(b - s) for b, s in zip(buy, sell, strict=False))
    avg_sell = sum(sell) / len(sell)
    return float(diff_sum / len(buy) / (avg_sell + 1e-6))


def attach_anomaly_scores(states: Sequence[MarketState], window: int = 20) -> None:
    """
    Anexa scores de anomalia aos estados do mercado (operação in-place).

    Calcula scores de anomalia para todos os estados e atribui cada score ao
    campo manipulation_score do respectivo MarketState. Modifica a lista
    de estados diretamente.

    Args:
        states: Sequência de estados do mercado a serem anotados
        window: Tamanho da janela para cálculo de z-scores (padrão: 20)

    Example:
        >>> states = runner.run(n_days=100)
        >>> attach_anomaly_scores(states, window=20)
        >>> high_risk_days = [s.day for s in states if s.manipulation_score > 3.0]
        >>> print(f"Dias suspeitos: {high_risk_days}")
    """

    scores = compute_price_volume_anomaly(states, window=window)
    for state, score in zip(states, scores, strict=False):
        state.manipulation_score = float(score)


__all__ = [
    "compute_price_volume_anomaly",
    "curve_imbalance_score",
    "attach_anomaly_scores",
]
