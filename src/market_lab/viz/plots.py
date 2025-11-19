"""Matplotlib helpers for inspecting simulation results."""

from __future__ import annotations

from typing import Iterable, Sequence

try:  # pragma: no cover - optional dependency
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None

from ..core.market import MarketState
from ..core.orders import OrderCurves


def _ensure_axis(ax=None):
    if ax is not None:
        return ax
    if plt is None:
        raise RuntimeError("matplotlib is required for plotting but is not installed")
    _, axis = plt.subplots()
    return axis


def plot_price_series(states: Sequence[MarketState], ax=None):
    ax = _ensure_axis(ax)
    ax.plot([state.day for state in states], [state.price for state in states], label="Price")
    ax.set_xlabel("Day")
    ax.set_ylabel("Price")
    ax.set_title("Price evolution")
    ax.legend()
    return ax


def plot_volume_series(states: Sequence[MarketState], ax=None):
    ax = _ensure_axis(ax)
    ax.bar([state.day for state in states], [state.volume for state in states], color="#4f83cc")
    ax.set_xlabel("Day")
    ax.set_ylabel("Volume")
    ax.set_title("Volume evolution")
    return ax


def plot_manipulation_score(states: Sequence[MarketState], ax=None):
    ax = _ensure_axis(ax)
    scores = [state.manipulation_score or 0.0 for state in states]
    ax.plot([state.day for state in states], scores, color="#c0392b", label="Score")
    ax.set_xlabel("Day")
    ax.set_ylabel("Score")
    ax.set_title("Manipulation score")
    ax.legend()
    return ax


def plot_order_curves(order_curves: OrderCurves, ax=None):
    ax = _ensure_axis(ax)
    ax.step(order_curves.price_grid, order_curves.buy_curve, where="post", label="Demand")
    ax.step(order_curves.price_grid, order_curves.sell_curve, where="post", label="Supply")
    ax.set_xlabel("Price")
    ax.set_ylabel("Cumulative volume")
    ax.set_title("Order curves")
    ax.legend()
    return ax


def plot_manipulator_vs_market(manip_wealth: Iterable[float], avg_wealth: Iterable[float], ax=None):
    ax = _ensure_axis(ax)
    ax.plot(list(manip_wealth), label="Manipulator")
    ax.plot(list(avg_wealth), label="Others")
    ax.set_xlabel("Day")
    ax.set_ylabel("Wealth")
    ax.set_title("Wealth comparison")
    ax.legend()
    return ax


__all__ = [
    "plot_price_series",
    "plot_volume_series",
    "plot_manipulation_score",
    "plot_order_curves",
    "plot_manipulator_vs_market",
]
