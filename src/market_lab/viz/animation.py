"""Lightweight animation utilities built on Matplotlib."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

try:  # pragma: no cover - optional dependency
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
except ImportError:  # pragma: no cover - optional dependency
    plt = None
    FuncAnimation = None

from ..core.market import MarketState


def animate_price_series(states: Sequence[MarketState], *, filepath: str, interval_ms: int = 200) -> None:
    """Create a simple line animation for the price series."""

    if plt is None or FuncAnimation is None:
        raise RuntimeError("matplotlib is required for animations but is not installed")

    path = Path(filepath)
    fig, ax = plt.subplots()
    days = [state.day for state in states]
    prices = [state.price for state in states]
    line, = ax.plot([], [], color="#222", linewidth=2)
    ax.set_xlim(min(days, default=0), max(days, default=1))
    ax.set_ylim(min(prices, default=0) * 0.95, max(prices, default=1) * 1.05)
    ax.set_xlabel("Day")
    ax.set_ylabel("Price")
    ax.set_title("Price animation")

    def init():
        line.set_data([], [])
        return (line,)

    def update(frame):
        line.set_data(days[: frame + 1], prices[: frame + 1])
        return (line,)

    animation = FuncAnimation(fig, update, frames=len(states), init_func=init, interval=interval_ms, blit=True)
    animation.save(path)
    plt.close(fig)


__all__ = ["animate_price_series"]
