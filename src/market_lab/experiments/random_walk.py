"""Entry point for running the baseline random walk experiment."""

from __future__ import annotations

import argparse
from random import Random

from ..core.market import MarketConfig
from ..core.simulation import SimulationRunner
from ..core.traders import build_traders
from ..core.sentiment import NoSentiment


def run_random_walk(days: int, seed: int | None = None, *, plot: bool = False):
    config = MarketConfig(
        n_traders=150,
        initial_price=100.0,
        price_volatility=2.5,
        max_daily_volume=15.0,
        wealth_mode="unlimited",
        price_tick=0.5,
        seed=seed,
    )
    rng = Random(seed)
    traders = build_traders(config, rng)
    runner = SimulationRunner(config=config, traders=traders, sentiment=NoSentiment(), rng=rng)
    states = runner.run(days)
    if plot:
        from ..viz.plots import plot_price_series, plot_volume_series  # noqa: WPS433

        plot_price_series(states)
        plot_volume_series(states)
    return states


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the baseline random walk experiment")
    parser.add_argument("--days", type=int, default=120, help="Number of simulated days")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--plot", action="store_true", help="Render matplotlib plots (requires matplotlib)")
    args = parser.parse_args()
    run_random_walk(days=args.days, seed=args.seed, plot=args.plot)


if __name__ == "__main__":
    main()
