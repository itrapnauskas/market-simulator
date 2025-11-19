"""Utilities for representing orders and aggregated curves."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(slots=True)
class Order:
    """Represents a single limit order."""

    trader_id: str
    side: str  # "buy" | "sell"
    price: float
    volume: float

    def __post_init__(self) -> None:
        if self.side not in {"buy", "sell"}:
            raise ValueError(f"Invalid side '{self.side}'")
        if self.price <= 0:
            raise ValueError("Order price must be positive")
        if self.volume <= 0:
            raise ValueError("Order volume must be positive")


@dataclass(slots=True)
class OrderCurves:
    """Aggregated order book curves along a discrete price grid."""

    price_grid: list[float]
    buy_curve: list[float]
    sell_curve: list[float]

    def satisfaction(self) -> list[float]:
        """Return the executable volume for each price level."""

        return [min(b, s) for b, s in zip(self.buy_curve, self.sell_curve, strict=False)]


def _ensure_price_grid(
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    *,
    price_tick: float,
) -> list[float]:
    prices: list[float] = [order.price for order in buy_orders] + [order.price for order in sell_orders]
    if not prices:
        return [price_tick]
    min_price = max(min(prices) - price_tick, price_tick)
    max_price = max(prices) + price_tick
    steps = int((max_price - min_price) / price_tick) + 1
    return [min_price + price_tick * idx for idx in range(steps)]


def aggregate_orders(
    *,
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    price_tick: float,
    price_grid: Sequence[float] | None = None,
) -> OrderCurves:
    """Convert raw orders into aggregated demand and supply curves."""

    grid = list(price_grid) if price_grid is not None else _ensure_price_grid(buy_orders, sell_orders, price_tick=price_tick)
    if not grid:
        grid = [price_tick]

    buy_curve: list[float] = []
    sell_curve: list[float] = []

    for price in grid:
        buy_curve.append(sum(order.volume for order in buy_orders if order.price >= price))
        sell_curve.append(sum(order.volume for order in sell_orders if order.price <= price))

    return OrderCurves(price_grid=grid, buy_curve=buy_curve, sell_curve=sell_curve)


def build_order_curves(
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    *,
    price_tick: float,
) -> OrderCurves:
    """Public wrapper compatible with :mod:`market_lab.core.market`."""

    return aggregate_orders(buy_orders=buy_orders, sell_orders=sell_orders, price_tick=price_tick)


def allocate_fills(orders: Iterable[Order], volume: float) -> list[tuple[Order, float]]:
    """Return executed volume for the provided orders in arrival sequence."""

    remaining = max(volume, 0.0)
    fills: list[tuple[Order, float]] = []
    for order in orders:
        if remaining <= 0:
            break
        fill_volume = min(order.volume, remaining)
        if fill_volume > 0:
            fills.append((order, fill_volume))
            remaining -= fill_volume
    return fills
