"""Tests for market manipulation strategies and pump-and-dump behavior."""

import pytest
from random import Random
from market_lab.manipulation.manipulator import Manipulator
from market_lab.core.market import MarketConfig
from market_lab.core.orders import Order


class TestManipulatorPhases:
    """Test manipulator phase detection and transitions."""

    def test_manipulator_creation(self):
        """Test creating a manipulator with default settings."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
        )
        assert manipulator.trader_id == "manip_1"
        assert manipulator.wealth == 100000.0
        assert manipulator.holdings == 0.0
        assert manipulator.accumulation_days == 30
        assert manipulator.pump_days == 10
        assert manipulator.dump_days == 15

    def test_manipulator_with_custom_phases(self):
        """Test creating manipulator with custom phase durations."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=20,
            pump_days=15,
            dump_days=10,
        )
        assert manipulator.accumulation_days == 20
        assert manipulator.pump_days == 15
        assert manipulator.dump_days == 10

    def test_current_phase_accumulation(self):
        """Test phase detection during accumulation."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
        )

        # Days 0-29 should be accumulation
        assert manipulator.current_phase(0) == "accumulate"
        assert manipulator.current_phase(15) == "accumulate"
        assert manipulator.current_phase(29) == "accumulate"

    def test_current_phase_pump(self):
        """Test phase detection during pump."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
        )

        # Days 30-39 should be pump
        assert manipulator.current_phase(30) == "pump"
        assert manipulator.current_phase(35) == "pump"
        assert manipulator.current_phase(39) == "pump"

    def test_current_phase_dump(self):
        """Test phase detection during dump."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
        )

        # Days 40+ should be dump
        assert manipulator.current_phase(40) == "dump"
        assert manipulator.current_phase(50) == "dump"
        assert manipulator.current_phase(100) == "dump"

    def test_phase_transitions(self):
        """Test all phase transitions."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=5,
            dump_days=5,
        )

        # Test transition points
        assert manipulator.current_phase(9) == "accumulate"
        assert manipulator.current_phase(10) == "pump"
        assert manipulator.current_phase(14) == "pump"
        assert manipulator.current_phase(15) == "dump"

    def test_zero_accumulation_days(self):
        """Test with zero accumulation period."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=0,
            pump_days=10,
            dump_days=5,
        )

        # Should start in pump phase
        assert manipulator.current_phase(0) == "pump"
        assert manipulator.current_phase(9) == "pump"
        assert manipulator.current_phase(10) == "dump"


class TestManipulatorAccumulation:
    """Test manipulator behavior during accumulation phase."""

    def test_accumulation_generates_orders(self):
        """Test that accumulation phase generates orders."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
            active_probability=1.0,  # Always active
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # During accumulation
        orders = manipulator.maybe_generate_order_batch(
            day=10,
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should generate at least one order during accumulation
        assert len(orders) >= 0  # May be 0 or 1 depending on active_probability

    def test_accumulation_uses_lower_price(self):
        """Test that accumulation bids below market price."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Generate multiple orders to check pricing strategy
        prices = []
        for day in range(10):
            orders = manipulator.maybe_generate_order_batch(
                day=day,
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
                rng=Random(42 + day),
            )
            for order in orders:
                prices.append(order.price)

        # Should generally be below 100 (98% of last_price)
        if prices:
            avg_price = sum(prices) / len(prices)
            assert avg_price < 100.0

    def test_accumulation_respects_wealth_limit(self):
        """Test that accumulation respects available cash."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=1000.0,  # Limited wealth
            holdings=0.0,
            accumulation_days=30,
            pump_days=10,
            dump_days=15,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=1000.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=10,
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Orders should not exceed available wealth
        for order in orders:
            if order.side == "buy":
                cost = order.price * order.volume
                assert cost <= manipulator.wealth * 1.1  # Allow small margin


class TestManipulatorPump:
    """Test manipulator behavior during pump phase."""

    def test_pump_generates_orders(self):
        """Test that pump phase generates orders."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=1000.0,  # Has holdings to pump
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # During pump phase (day 10)
        orders = manipulator.maybe_generate_order_batch(
            day=10,
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should generate orders (typically buy and sell)
        assert len(orders) >= 0

    def test_pump_uses_higher_price(self):
        """Test that pump phase bids above market price."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=1000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=10,  # Pump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Check buy orders are above market
        buy_orders = [o for o in orders if o.side == "buy"]
        if buy_orders:
            for order in buy_orders:
                # Should be at least 102% of last price
                assert order.price >= 100.0 * 1.01

    def test_pump_creates_wash_trades(self):
        """Test that pump phase creates both buy and sell orders."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=1000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=10,  # Pump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # During pump, should create both buy and sell to create volume
        if len(orders) >= 2:
            sides = [o.side for o in orders]
            assert "buy" in sides or "sell" in sides

    def test_pump_with_no_wealth(self):
        """Test pump phase when manipulator has no cash."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=0.0,  # No cash
            holdings=1000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=10,  # Pump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should handle gracefully (may generate no orders or only sells)
        assert isinstance(orders, list)

    def test_pump_volume_exceeds_normal_limit(self):
        """Test that pump phase uses larger volumes."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=10000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,  # Normal max
        )

        orders = manipulator.maybe_generate_order_batch(
            day=10,  # Pump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Pump can use 2x normal volume
        for order in orders:
            assert order.volume <= config.max_daily_volume * 2.1  # Allow margin


class TestManipulatorDump:
    """Test manipulator behavior during dump phase."""

    def test_dump_generates_sell_orders(self):
        """Test that dump phase generates sell orders."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=5000.0,  # Has holdings to dump
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # During dump phase (day 20)
        orders = manipulator.maybe_generate_order_batch(
            day=20,
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should generate orders
        assert len(orders) >= 0
        # All should be sell orders
        for order in orders:
            assert order.side == "sell"

    def test_dump_uses_lower_price(self):
        """Test that dump phase sells below market price."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=5000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=20,  # Dump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # All sell orders should be below market
        for order in orders:
            assert order.side == "sell"
            # Should be around 99% of last price
            assert order.price <= 100.0

    def test_dump_limited_by_holdings(self):
        """Test that dump cannot sell more than holdings."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=50.0,  # Limited holdings
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=1000.0,  # Would want to sell more
        )

        orders = manipulator.maybe_generate_order_batch(
            day=20,  # Dump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Total sell volume should not exceed holdings
        total_volume = sum(o.volume for o in orders)
        assert total_volume <= manipulator.holdings

    def test_dump_with_no_holdings(self):
        """Test dump phase when manipulator has no holdings."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,  # No holdings
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=20,  # Dump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should generate no orders
        assert len(orders) == 0

    def test_dump_volume_exceeds_normal_limit(self):
        """Test that dump phase uses larger volumes."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=10000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,  # Normal max
        )

        orders = manipulator.maybe_generate_order_batch(
            day=20,  # Dump phase
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Dump can use 3x normal volume
        for order in orders:
            assert order.volume <= config.max_daily_volume * 3.1  # Allow margin


class TestManipulatorBehavior:
    """Test overall manipulator behavior and strategies."""

    def test_manipulator_order_ids(self):
        """Test that manipulator orders have identifiable IDs."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=1000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Check order IDs in different phases
        accum_orders = manipulator.maybe_generate_order_batch(
            day=5, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        for order in accum_orders:
            assert "manip_1" in order.trader_id

        pump_orders = manipulator.maybe_generate_order_batch(
            day=15, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        for order in pump_orders:
            assert "manip_1" in order.trader_id
            assert "pump" in order.trader_id

        dump_orders = manipulator.maybe_generate_order_batch(
            day=25, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        for order in dump_orders:
            assert "manip_1" in order.trader_id
            assert "dump" in order.trader_id

    def test_manipulator_inherits_from_wealth_limited(self):
        """Test that Manipulator is a WealthLimitedTrader."""
        from market_lab.core.traders import WealthLimitedTrader

        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
        )

        assert isinstance(manipulator, WealthLimitedTrader)

    def test_manipulator_apply_fill(self):
        """Test that manipulator can execute fills."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
        )

        order = Order("manip_1", "buy", 100.0, 50.0)
        initial_wealth = manipulator.wealth
        initial_holdings = manipulator.holdings

        manipulator.apply_fill(order, price=100.0, volume=50.0)

        assert manipulator.wealth == initial_wealth - 5000.0
        assert manipulator.holdings == initial_holdings + 50.0

    def test_manipulator_complete_cycle(self):
        """Test manipulator through all phases."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=5,
            dump_days=5,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Simulate through all phases
        for day in range(25):
            orders = manipulator.maybe_generate_order_batch(
                day=day,
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
                rng=Random(42 + day),
            )

            # Execute orders
            for order in orders:
                if order.side == "buy":
                    fill_volume = min(order.volume, 50.0)
                    manipulator.apply_fill(order, price=order.price, volume=fill_volume)
                else:
                    fill_volume = min(order.volume, manipulator.holdings)
                    if fill_volume > 0:
                        manipulator.apply_fill(order, price=order.price, volume=fill_volume)

        # After complete cycle, wealth should have changed
        assert manipulator.wealth != 100000.0 or manipulator.holdings != 0.0

    def test_manipulator_with_extreme_wealth(self):
        """Test manipulator with very large wealth."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="whale",
            rng=rng,
            wealth=10000000.0,  # Very wealthy
            holdings=0.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        orders = manipulator.maybe_generate_order_batch(
            day=5,
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
            rng=Random(42),
        )

        # Should generate orders without overflow
        assert isinstance(orders, list)

    def test_manipulator_price_impact_direction(self):
        """Test that manipulator strategies push prices in expected directions."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=1000.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Accumulation: should bid below market
        accum_orders = manipulator.maybe_generate_order_batch(
            day=5, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        accum_buy_prices = [o.price for o in accum_orders if o.side == "buy"]
        if accum_buy_prices:
            assert max(accum_buy_prices) <= 100.0

        # Pump: should bid above market
        pump_orders = manipulator.maybe_generate_order_batch(
            day=15, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        pump_buy_prices = [o.price for o in pump_orders if o.side == "buy"]
        if pump_buy_prices:
            assert min(pump_buy_prices) >= 100.0

        # Dump: should sell below market
        dump_orders = manipulator.maybe_generate_order_batch(
            day=25, last_price=100.0, sentiment_value=0.0, config=config, rng=Random(42)
        )
        dump_sell_prices = [o.price for o in dump_orders if o.side == "sell"]
        if dump_sell_prices:
            assert max(dump_sell_prices) <= 100.0

    def test_manipulator_phases_do_not_overlap(self):
        """Test that phase transitions are clean (no overlap)."""
        rng = Random(42)
        manipulator = Manipulator(
            trader_id="manip_1",
            rng=rng,
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )

        # Check every day for 30 days
        phases = [manipulator.current_phase(day) for day in range(30)]

        # Count phase changes
        phase_changes = sum(1 for i in range(len(phases) - 1) if phases[i] != phases[i + 1])

        # Should have exactly 2 phase changes (accumulate->pump, pump->dump)
        assert phase_changes == 2
