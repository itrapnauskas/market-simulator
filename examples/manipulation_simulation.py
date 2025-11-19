"""Example of running a market simulation with manipulation strategies.

This script demonstrates how to integrate the new manipulation strategies
into a full market simulation alongside regular traders.
"""

from random import Random

from market_lab.core.market import MarketConfig
from market_lab.core.simulation import run_simulation
from market_lab.core.traders import build_traders
from market_lab.manipulation import (
    LayeringManipulator,
    SpoofingManipulator,
    WashTradingManipulator,
)


def create_manipulated_market():
    """Create a market with both regular traders and manipulators."""

    # Market configuration
    config = MarketConfig(
        n_traders=50,  # Regular traders
        initial_price=100.0,
        price_volatility=2.0,
        max_daily_volume=10.0,
        wealth_mode="limited",
        sentiment_mode="none",
        price_tick=0.01,
        seed=42,
    )

    # Create regular traders
    rng = Random(config.seed)
    traders = build_traders(config, rng)

    # Add manipulators
    manipulators = [
        SpoofingManipulator(
            trader_id="SPOOFER_A",
            rng=Random(rng.randrange(0, 10**9)),
            wealth=500_000.0,  # Well-capitalized
            holdings=200.0,
            spoof_multiplier=10.0,  # Very large spoof orders
            spoof_probability=0.5,
            price_offset=0.025,
            target_side="buy",
        ),
        WashTradingManipulator(
            trader_id="WASHER_A",
            rng=Random(rng.randrange(0, 10**9)),
            wealth=300_000.0,
            holdings=150.0,
            wash_probability=0.7,  # Frequently wash trades
            volume_multiplier=5.0,
            price_spread=0.0002,  # Very tight spread
            pairs_per_session=4,
        ),
        LayeringManipulator(
            trader_id="LAYERER_A",
            rng=Random(rng.randrange(0, 10**9)),
            wealth=400_000.0,
            holdings=180.0,
            n_layers=8,  # Many layers
            layer_spacing=0.004,
            volume_decay=0.7,
            layer_probability=0.8,
            target_side="sell",
        ),
    ]

    # Combine all traders
    all_traders = traders + manipulators

    print("=" * 70)
    print("MARKET SIMULATION WITH MANIPULATION")
    print("=" * 70)
    print()
    print(f"Market Configuration:")
    print(f"  Regular Traders: {len(traders)}")
    print(f"  Manipulators: {len(manipulators)}")
    print(f"    - Spoofers: 1")
    print(f"    - Wash Traders: 1")
    print(f"    - Layerers: 1")
    print(f"  Initial Price: ${config.initial_price:.2f}")
    print(f"  Price Volatility: {config.price_volatility}")
    print()

    return config, all_traders


def run_manipulated_simulation(days=30):
    """Run a simulation with manipulators and analyze results."""

    config, traders = create_manipulated_market()

    print(f"Running {days}-day simulation...")
    print()

    # Run simulation
    history = run_simulation(
        config=config,
        traders=traders,
        days=days,
        sentiment_values=[0.0] * days,  # Neutral sentiment
    )

    # Analyze results
    print("=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    print()

    # Price statistics
    prices = [state.price for state in history]
    volumes = [state.volume for state in history]

    print(f"Price Statistics:")
    print(f"  Initial: ${prices[0]:.2f}")
    print(f"  Final: ${prices[-1]:.2f}")
    print(f"  Min: ${min(prices):.2f}")
    print(f"  Max: ${max(prices):.2f}")
    print(f"  Change: {((prices[-1] - prices[0]) / prices[0] * 100):.2f}%")
    print()

    print(f"Volume Statistics:")
    print(f"  Average: {sum(volumes) / len(volumes):.2f}")
    print(f"  Min: {min(volumes):.2f}")
    print(f"  Max: {max(volumes):.2f}")
    print(f"  Total: {sum(volumes):.2f}")
    print()

    # Find manipulator wealth changes
    manipulator_ids = ["SPOOFER_A", "WASHER_A", "LAYERER_A"]

    print("Manipulator Performance:")
    for trader in traders:
        if trader.trader_id in manipulator_ids:
            # Calculate total value (wealth + holdings value)
            final_value = trader.wealth + (trader.holdings * prices[-1])

            # Estimate initial value (rough approximation)
            if trader.trader_id == "SPOOFER_A":
                initial_value = 500_000.0 + (200.0 * prices[0])
            elif trader.trader_id == "WASHER_A":
                initial_value = 300_000.0 + (150.0 * prices[0])
            else:  # LAYERER_A
                initial_value = 400_000.0 + (180.0 * prices[0])

            profit = final_value - initial_value
            profit_pct = (profit / initial_value) * 100

            print(f"  {trader.trader_id}:")
            print(f"    Initial Value: ${initial_value:,.2f}")
            print(f"    Final Value: ${final_value:,.2f}")
            print(f"    Profit: ${profit:,.2f} ({profit_pct:+.2f}%)")
            print(f"    Holdings: {trader.holdings:.2f} units")
            print(f"    Cash: ${trader.wealth:,.2f}")
            print()

    # Print some daily details
    print("Sample Daily Activity (First 5 Days):")
    print()
    for day in range(min(5, len(history))):
        state = history[day]
        print(
            f"  Day {day + 1}: "
            f"Price=${state.price:.2f}, "
            f"Volume={state.volume:.2f}, "
            f"Sentiment={state.sentiment_value:.2f}"
        )
    print()

    return history


if __name__ == "__main__":
    # Run simulation
    history = run_manipulated_simulation(days=30)

    print("=" * 70)
    print("NOTES")
    print("=" * 70)
    print()
    print("This simulation demonstrates how manipulation strategies can")
    print("coexist with regular traders in a market environment.")
    print()
    print("Key observations to look for:")
    print("  1. Price volatility compared to regular simulations")
    print("  2. Volume patterns (especially from wash trading)")
    print("  3. Manipulator profitability vs regular traders")
    print("  4. Detection signatures in order patterns")
    print()
    print("For visualization and detailed analysis, consider using:")
    print("  - market_lab.viz.plots for price/volume charts")
    print("  - market_lab.manipulation.detection for pattern analysis")
    print("  - market_lab.manipulation.metrics for manipulation scores")
    print()
