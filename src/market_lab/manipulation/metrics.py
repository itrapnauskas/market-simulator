"""Quantitative helpers used by detection functions."""

from __future__ import annotations

from typing import Iterable, List


def rolling_zscore(values: Iterable[float], window: int = 10) -> list[float]:
    """
    Calcula z-scores usando uma janela deslizante.

    Para cada ponto, calcula quantos desvios padrão ele está da média dos
    últimos 'window' valores. Útil para detectar outliers e anomalias em
    séries temporais.

    Args:
        values: Sequência de valores numéricos para análise
        window: Tamanho da janela deslizante (padrão: 10)

    Returns:
        Lista de z-scores, um por valor de entrada. Para índices menores que
        window, usa todos os valores disponíveis até aquele ponto.

    Example:
        >>> prices = [100, 101, 102, 150, 103, 104]
        >>> zscores = rolling_zscore(prices, window=4)
        >>> zscores[3]  # O valor 150 terá z-score alto
        2.5
    """

    series = list(values)
    if not series:
        return []
    zscores: List[float] = [0.0 for _ in series]
    for idx in range(len(series)):
        start = max(0, idx - window + 1)
        window_slice = series[start : idx + 1]
        mean = sum(window_slice) / len(window_slice)
        if len(window_slice) > 1:
            variance = sum((value - mean) ** 2 for value in window_slice) / (len(window_slice) - 1)
            std = variance**0.5
        else:
            std = 0.0
        if std == 0:
            zscores[idx] = 0.0
        else:
            zscores[idx] = (series[idx] - mean) / std
    return zscores


def band_distance(series: Iterable[float], *, lower: Iterable[float], upper: Iterable[float]) -> list[float]:
    """
    Mede o quão distante os valores estão de uma banda de referência.

    Calcula a distância de cada valor para fora da banda [lower, upper].
    Valores dentro da banda retornam distância zero.

    Args:
        series: Sequência de valores a serem comparados com a banda
        lower: Limite inferior da banda de referência
        upper: Limite superior da banda de referência

    Returns:
        Lista de distâncias, uma por valor. Zero se o valor estiver dentro da
        banda, caso contrário a distância até o limite mais próximo.

    Raises:
        ValueError: Se as sequências não tiverem o mesmo comprimento

    Example:
        >>> values = [5, 10, 15, 20]
        >>> lower = [8, 8, 8, 8]
        >>> upper = [12, 12, 12, 12]
        >>> distances = band_distance(values, lower=lower, upper=upper)
        >>> distances
        [3.0, 0.0, 3.0, 8.0]
    """

    values = list(series)
    low = list(lower)
    up = list(upper)
    if not (len(values) == len(low) == len(up)):
        raise ValueError("Input series must share the same length")
    distance: List[float] = [0.0 for _ in values]
    for idx, val in enumerate(values):
        if val < low[idx]:
            distance[idx] = low[idx] - val
        elif val > up[idx]:
            distance[idx] = val - up[idx]
        else:
            distance[idx] = 0.0
    return distance


__all__ = ["rolling_zscore", "band_distance"]
