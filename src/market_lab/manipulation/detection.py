"""Detection helpers that operate on market states."""

from __future__ import annotations

from typing import Sequence

from ..core.market import MarketState
from ..core.orders import OrderCurves
from .metrics import rolling_zscore


def compute_price_volume_anomaly(states: Sequence[MarketState], window: int = 20) -> list[float]:
    """Return a composite anomaly score using price and volume z-scores."""

    prices = [state.price for state in states]
    volumes = [state.volume for state in states]
    price_z = rolling_zscore(prices, window=window)
    volume_z = rolling_zscore(volumes, window=window)
    return [abs(p) + abs(v) for p, v in zip(price_z, volume_z, strict=False)]


def curve_imbalance_score(order_curves: OrderCurves | None) -> float:
    """Measure the imbalance between demand and supply curves for a single day."""

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
    """Mutate ``states`` so that ``manipulation_score`` holds an anomaly score."""

    scores = compute_price_volume_anomaly(states, window=window)
    for state, score in zip(states, scores, strict=False):
        state.manipulation_score = float(score)


__all__ = [
    "compute_price_volume_anomaly",
    "curve_imbalance_score",
    "attach_anomaly_scores",
]
