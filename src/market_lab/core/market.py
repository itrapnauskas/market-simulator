"""Market configuration and auction pricing helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .orders import OrderCurves, build_order_curves


@dataclass(slots=True)
class MarketConfig:
    """Configuration container for the simulator."""

    n_traders: int
    initial_price: float
    price_volatility: float
    max_daily_volume: float
    wealth_mode: str = "unlimited"
    sentiment_mode: str = "none"
    price_tick: float = 1.0
    seed: Optional[int] = None


@dataclass(slots=True)
class MarketState:
    """Snapshot of the market after a trading day."""

    day: int
    price: float
    volume: float
    sentiment_value: float
    order_curves: OrderCurves | None = None
    manipulation_score: float | None = None


def find_equilibrium_price(order_curves: OrderCurves) -> tuple[float, float]:
    """Return the clearing price and traded volume using auction pricing."""

    satisfaction = order_curves.satisfaction()
    max_volume = max(satisfaction) if satisfaction else 0.0
    if max_volume <= 0:
        last_price = order_curves.price_grid[-1] if order_curves.price_grid else 0.0
        return last_price, 0.0

    candidates = [price for price, volume in zip(order_curves.price_grid, satisfaction, strict=False) if volume == max_volume]
    price = sum(candidates) / len(candidates) if candidates else (order_curves.price_grid[-1] if order_curves.price_grid else 0.0)
    return price, max_volume


__all__ = [
    "MarketConfig",
    "MarketState",
    "find_equilibrium_price",
    "build_order_curves",
]
