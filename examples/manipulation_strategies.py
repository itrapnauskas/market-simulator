"""Example demonstrating the three new manipulation strategies.

This script shows how to use SpoofingManipulator, WashTradingManipulator,
and LayeringManipulator in market simulations.
"""

from random import Random

from market_lab.core.market import MarketConfig
from market_lab.manipulation import (
    LayeringManipulator,
    SpoofingManipulator,
    WashTradingManipulator,
)


def example_spoofing_manipulator():
    """Demonstrate spoofing strategy."""
    print("=" * 70)
    print("SPOOFING MANIPULATOR EXAMPLE")
    print("=" * 70)
    print()
    print("Strategy: Place large orders to influence price, then cancel them")
    print()

    # Create a spoofing manipulator
    manipulator = SpoofingManipulator(
        trader_id="spoofer_001",
        rng=Random(42),
        wealth=100_000.0,
        holdings=50.0,
        spoof_multiplier=8.0,  # Spoof orders are 8x normal size
        spoof_probability=0.4,  # 40% chance to spoof
        price_offset=0.03,  # 3% price offset
        target_side="buy",  # Focus on buy-side spoofing
    )

    # Simulate market configuration
    config = MarketConfig(
        n_traders=100,
        initial_price=100.0,
        price_volatility=2.0,
        max_daily_volume=10.0,
        price_tick=0.01,
    )

    print(f"Initial State:")
    print(f"  Wealth: ${manipulator.wealth:,.2f}")
    print(f"  Holdings: {manipulator.holdings:.2f} units")
    print()

    # Generate some orders
    print("Generating orders over 10 simulated turns:")
    print()

    for turn in range(10):
        order = manipulator.maybe_generate_order(
            last_price=100.0,
            sentiment_value=0.5,
            config=config,
        )

        if order:
            order_type = "SPOOF" if "spoof" in order.trader_id else "GENUINE"
            print(
                f"Turn {turn + 1}: [{order_type}] {order.side.upper()} "
                f"{order.volume:.2f} units @ ${order.price:.2f}"
            )
        else:
            print(f"Turn {turn + 1}: No order generated")

    print()
    print("Key characteristics:")
    print("  - Large spoof orders influence perceived support/resistance")
    print("  - Smaller genuine orders on opposite side capture profit")
    print("  - Spoof orders are tracked and 'cancelled' after threshold")
    print()


def example_wash_trading_manipulator():
    """Demonstrate wash trading strategy."""
    print("=" * 70)
    print("WASH TRADING MANIPULATOR EXAMPLE")
    print("=" * 70)
    print()
    print("Strategy: Simultaneously buy and sell to create artificial volume")
    print()

    # Create a wash trading manipulator
    manipulator = WashTradingManipulator(
        trader_id="washer_001",
        rng=Random(123),
        wealth=150_000.0,
        holdings=100.0,
        wash_probability=0.6,  # 60% chance to wash trade
        volume_multiplier=4.0,  # Wash trades are 4x normal size
        price_spread=0.0005,  # 0.05% spread between buy/sell
        pairs_per_session=3,  # 3 buy/sell pairs per session
    )

    config = MarketConfig(
        n_traders=100,
        initial_price=100.0,
        price_volatility=2.0,
        max_daily_volume=15.0,
        price_tick=0.01,
    )

    print(f"Initial State:")
    print(f"  Wealth: ${manipulator.wealth:,.2f}")
    print(f"  Holdings: {manipulator.holdings:.2f} units")
    print()

    # Generate some orders
    print("Generating orders over 15 simulated turns:")
    print()

    for turn in range(15):
        order = manipulator.maybe_generate_order(
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
        )

        if order:
            order_type = "WASH" if "wash" in order.trader_id else "NORMAL"
            print(
                f"Turn {turn + 1}: [{order_type}] {order.side.upper()} "
                f"{order.volume:.2f} units @ ${order.price:.2f}"
            )
        else:
            print(f"Turn {turn + 1}: No order generated")

    print()
    print("Key characteristics:")
    print("  - Matching buy/sell pairs with tight spreads")
    print("  - Creates artificial volume without changing position")
    print("  - Periodic rebalancing to maintain neutral holdings")
    print()


def example_layering_manipulator():
    """Demonstrate layering strategy."""
    print("=" * 70)
    print("LAYERING MANIPULATOR EXAMPLE")
    print("=" * 70)
    print()
    print("Strategy: Create multiple order layers to create false liquidity")
    print()

    # Create a layering manipulator
    manipulator = LayeringManipulator(
        trader_id="layer_001",
        rng=Random(456),
        wealth=200_000.0,
        holdings=150.0,
        n_layers=5,  # Create 5 price layers
        layer_spacing=0.005,  # 0.5% between each layer
        volume_decay=0.75,  # Each layer is 75% of previous
        layer_probability=0.7,  # 70% chance to add layers
        target_side="sell",  # Focus on sell-side layering
    )

    config = MarketConfig(
        n_traders=100,
        initial_price=100.0,
        price_volatility=2.0,
        max_daily_volume=20.0,
        price_tick=0.01,
    )

    print(f"Initial State:")
    print(f"  Wealth: ${manipulator.wealth:,.2f}")
    print(f"  Holdings: {manipulator.holdings:.2f} units")
    print()

    # Generate orders through different phases
    print("Generating orders through manipulation phases:")
    print()

    phases = ["BUILD", "MAINTAIN", "REMOVE", "PROFIT"]
    turns_per_phase = 8

    for phase_idx, phase_name in enumerate(phases):
        print(f"\n--- {phase_name} PHASE ---")
        for turn in range(turns_per_phase):
            order = manipulator.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )

            if order:
                order_type = "LAYER" if "layer" in order.trader_id else "PROFIT"
                print(
                    f"  Turn {turn + 1}: [{order_type}] {order.side.upper()} "
                    f"{order.volume:.2f} units @ ${order.price:.2f}"
                )
            else:
                print(f"  Turn {turn + 1}: No order generated")

    print()
    print("Key characteristics:")
    print("  - Multiple layers create illusion of deep liquidity")
    print("  - Layers are progressively removed before execution")
    print("  - Genuine profit orders on opposite side")
    print("  - Cycles through build/maintain/remove/profit phases")
    print()


def comparison_summary():
    """Print a comparison of the three strategies."""
    print("=" * 70)
    print("STRATEGY COMPARISON SUMMARY")
    print("=" * 70)
    print()

    strategies = [
        {
            "name": "Spoofing",
            "objective": "Create false price signals",
            "mechanism": "Large orders that are quickly cancelled",
            "detection_risk": "Medium - visible order cancellations",
            "market_impact": "Short-term price distortion",
        },
        {
            "name": "Wash Trading",
            "objective": "Inflate trading volume",
            "mechanism": "Simultaneous buy/sell pairs",
            "detection_risk": "Low - appears as normal trading",
            "market_impact": "Artificial volume, minimal price impact",
        },
        {
            "name": "Layering",
            "objective": "Create false liquidity impression",
            "mechanism": "Multiple order layers across price levels",
            "detection_risk": "High - distinctive pattern",
            "market_impact": "Medium-term liquidity illusion",
        },
    ]

    for strategy in strategies:
        print(f"{strategy['name'].upper()}")
        print(f"  Objective:        {strategy['objective']}")
        print(f"  Mechanism:        {strategy['mechanism']}")
        print(f"  Detection Risk:   {strategy['detection_risk']}")
        print(f"  Market Impact:    {strategy['market_impact']}")
        print()

    print("All strategies inherit from WealthLimitedTrader and respect:")
    print("  - Available wealth constraints")
    print("  - Holdings limits")
    print("  - Market configuration parameters")
    print()


if __name__ == "__main__":
    # Run all examples
    example_spoofing_manipulator()
    print("\n")

    example_wash_trading_manipulator()
    print("\n")

    example_layering_manipulator()
    print("\n")

    comparison_summary()
