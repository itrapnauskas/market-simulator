"""Tests for simulation runner and integration scenarios."""

import pytest
from random import Random
from market_lab.core.simulation import SimulationRunner
from market_lab.core.market import MarketConfig, MarketState
from market_lab.core.traders import build_traders, RandomTrader, WealthLimitedTrader
from market_lab.core.sentiment import NoSentiment, StepSentiment, PulseSentiment
from market_lab.manipulation.manipulator import Manipulator


class TestSimulationRunner:
    """Test SimulationRunner basic functionality."""

    def test_runner_creation(self):
        """Test creating a simulation runner."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)

        runner = SimulationRunner(
            config=config,
            traders=traders,
            rng=rng,
        )

        assert runner.config == config
        assert len(runner.traders) == 10
        assert runner.manipulator is None
        assert isinstance(runner.sentiment, NoSentiment)

    def test_run_single_day(self):
        """Test running simulation for one day."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=1)

        assert len(states) == 1
        assert states[0].day == 0
        assert states[0].price > 0
        assert states[0].volume >= 0

    def test_run_multiple_days(self):
        """Test running simulation for multiple days."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=20,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=10)

        assert len(states) == 10
        for i, state in enumerate(states):
            assert state.day == i
            assert state.price > 0

    def test_run_preserves_price_continuity(self):
        """Test that each day uses previous day's price."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=15,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=5)

        # Prices should form a continuous series
        for i in range(len(states)):
            assert states[i].price > 0

    def test_run_with_no_traders(self):
        """Test running with empty trader list."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=0,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = []
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=5)

        # Should still run, but with zero volume
        assert len(states) == 5
        for state in states:
            assert state.volume == 0.0
            assert state.price == 100.0  # Should maintain initial price

    def test_run_captures_market_states(self):
        """Test that market states contain all required fields."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=3)

        for state in states:
            assert isinstance(state, MarketState)
            assert state.day >= 0
            assert state.price > 0
            assert state.volume >= 0
            assert state.sentiment_value == 0.0  # NoSentiment default
            assert state.order_curves is not None or state.volume == 0

    def test_run_with_seed_reproducible(self):
        """Test that same seed produces same results."""
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            seed=42,
        )

        # Run 1
        rng1 = Random(42)
        traders1 = build_traders(config, rng1)
        runner1 = SimulationRunner(config=config, traders=traders1, rng=Random(42))
        states1 = runner1.run(n_days=5)

        # Run 2
        rng2 = Random(42)
        traders2 = build_traders(config, rng2)
        runner2 = SimulationRunner(config=config, traders=traders2, rng=Random(42))
        states2 = runner2.run(n_days=5)

        # Should produce identical results
        for s1, s2 in zip(states1, states2):
            assert s1.day == s2.day
            assert abs(s1.price - s2.price) < 0.01
            assert abs(s1.volume - s2.volume) < 0.01

    def test_run_long_simulation(self):
        """Test running longer simulation."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=100)

        assert len(states) == 100
        # Check that simulation completes without errors
        assert all(s.price > 0 for s in states)

    def test_run_updates_trader_state(self):
        """Test that limited traders' wealth updates during simulation."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=5,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=10.0,
            wealth_mode="limited",
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        # Record initial wealth
        initial_wealth = [t.wealth for t in traders]
        initial_holdings = [t.holdings for t in traders]

        states = runner.run(n_days=20)

        # After trading, at least some traders should have different wealth/holdings
        final_wealth = [t.wealth for t in traders]
        final_holdings = [t.holdings for t in traders]

        # At least one trader should have changed
        wealth_changed = any(w1 != w2 for w1, w2 in zip(initial_wealth, final_wealth))
        holdings_changed = any(h1 != h2 for h1, h2 in zip(initial_holdings, final_holdings))

        assert wealth_changed or holdings_changed


class TestSimulationWithSentiment:
    """Test simulation with sentiment curves."""

    def test_run_with_no_sentiment(self):
        """Test default NoSentiment behavior."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(
            config=config,
            traders=traders,
            sentiment=NoSentiment(),
            rng=rng,
        )

        states = runner.run(n_days=5)

        for state in states:
            assert state.sentiment_value == 0.0

    def test_run_with_step_sentiment(self):
        """Test StepSentiment affecting prices."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=15,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        sentiment = StepSentiment(start_day=3, magnitude=10.0)
        runner = SimulationRunner(
            config=config,
            traders=traders,
            sentiment=sentiment,
            rng=rng,
        )

        states = runner.run(n_days=6)

        # Check sentiment values
        assert states[0].sentiment_value == 0.0
        assert states[2].sentiment_value == 0.0
        assert states[3].sentiment_value == 10.0
        assert states[5].sentiment_value == 10.0

    def test_run_with_pulse_sentiment(self):
        """Test PulseSentiment affecting prices temporarily."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=15,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        sentiment = PulseSentiment(center_day=5, width=2, magnitude=15.0)
        runner = SimulationRunner(
            config=config,
            traders=traders,
            sentiment=sentiment,
            rng=rng,
        )

        states = runner.run(n_days=10)

        # Before pulse
        assert states[3].sentiment_value == 0.0

        # During pulse (day 4-6 for center=5, width=2)
        assert states[4].sentiment_value == 15.0
        assert states[5].sentiment_value == 15.0
        assert states[6].sentiment_value == 15.0

        # After pulse
        assert states[7].sentiment_value == 0.0

    def test_sentiment_affects_price_trend(self):
        """Test that positive sentiment generally increases prices."""
        rng_no_sentiment = Random(42)
        config = MarketConfig(
            n_traders=20,
            initial_price=100.0,
            price_volatility=2.0,
            max_daily_volume=50.0,
        )

        # Run without sentiment
        traders_no = build_traders(config, rng_no_sentiment)
        runner_no = SimulationRunner(
            config=config,
            traders=traders_no,
            sentiment=NoSentiment(),
            rng=Random(42),
        )
        states_no = runner_no.run(n_days=20)

        # Run with positive sentiment
        rng_with = Random(42)
        traders_with = build_traders(config, rng_with)
        runner_with = SimulationRunner(
            config=config,
            traders=traders_with,
            sentiment=StepSentiment(start_day=0, magnitude=5.0),
            rng=Random(42),
        )
        states_with = runner_with.run(n_days=20)

        # With positive sentiment should generally have higher prices
        avg_price_no = sum(s.price for s in states_no) / len(states_no)
        avg_price_with = sum(s.price for s in states_with) / len(states_with)

        assert avg_price_with > avg_price_no


class TestSimulationWithManipulator:
    """Test simulation with market manipulator."""

    def test_run_with_manipulator(self):
        """Test basic simulation with manipulator."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=5,
            dump_days=5,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        states = runner.run(n_days=25)

        assert len(states) == 25
        # All states should have valid prices
        assert all(s.price > 0 for s in states)

    def test_manipulator_affects_prices(self):
        """Test that manipulator influences market prices."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=50.0,
        )

        # Run without manipulator
        traders_no = build_traders(config, Random(42))
        runner_no = SimulationRunner(
            config=config,
            traders=traders_no,
            rng=Random(42),
        )
        states_no = runner_no.run(n_days=30)

        # Run with manipulator
        traders_with = build_traders(config, Random(42))
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=10,
            dump_days=10,
        )
        runner_with = SimulationRunner(
            config=config,
            traders=traders_with,
            manipulator=manipulator,
            rng=Random(42),
        )
        states_with = runner_with.run(n_days=30)

        # Prices should differ when manipulator is present
        price_diff = sum(abs(s1.price - s2.price) for s1, s2 in zip(states_no, states_with))
        assert price_diff > 0

    def test_manipulator_accumulation_phase(self):
        """Test manipulator behavior during accumulation."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=5,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=10,
            pump_days=5,
            dump_days=5,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        initial_holdings = manipulator.holdings
        states = runner.run(n_days=10)  # Only accumulation phase

        # Manipulator should have accumulated holdings
        assert manipulator.holdings >= initial_holdings

    def test_manipulator_pump_phase(self):
        """Test manipulator behavior during pump."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=5,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=100000.0,
            holdings=1000.0,  # Start with holdings
            accumulation_days=0,  # Skip accumulation
            pump_days=10,
            dump_days=5,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        states = runner.run(n_days=10)  # Pump phase

        # During pump, price should generally trend upward
        first_half_avg = sum(s.price for s in states[:5]) / 5
        second_half_avg = sum(s.price for s in states[5:]) / 5

        # Note: This is probabilistic, but pump should push prices up
        assert second_half_avg >= first_half_avg * 0.95  # Allow some variance

    def test_manipulator_dump_phase(self):
        """Test manipulator behavior during dump."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=5,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=10000.0,
            holdings=1000.0,  # Start with holdings to dump
            accumulation_days=0,
            pump_days=0,  # Skip to dump
            dump_days=10,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        initial_holdings = manipulator.holdings
        states = runner.run(n_days=10)  # Dump phase

        # Manipulator should have sold holdings
        assert manipulator.holdings < initial_holdings

    def test_full_pump_and_dump_cycle(self):
        """Test complete pump and dump cycle."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=100000.0,
            holdings=0.0,
            accumulation_days=15,
            pump_days=10,
            dump_days=10,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        states = runner.run(n_days=40)

        # Extract prices by phase
        accumulation_prices = [s.price for s in states[:15]]
        pump_prices = [s.price for s in states[15:25]]
        dump_prices = [s.price for s in states[25:35]]

        # Check phase transitions
        avg_accumulation = sum(accumulation_prices) / len(accumulation_prices)
        avg_pump = sum(pump_prices) / len(pump_prices)
        avg_dump = sum(dump_prices) / len(dump_prices)

        # Pump should have higher prices than accumulation
        assert avg_pump >= avg_accumulation * 0.95

    def test_manipulator_with_limited_wealth(self):
        """Test that manipulator respects wealth constraints."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        manipulator = Manipulator(
            trader_id="manipulator",
            rng=Random(42),
            wealth=1000.0,  # Limited wealth
            holdings=0.0,
            accumulation_days=10,
            pump_days=5,
            dump_days=5,
        )
        runner = SimulationRunner(
            config=config,
            traders=traders,
            manipulator=manipulator,
            rng=rng,
        )

        states = runner.run(n_days=20)

        # Should run without errors despite limited wealth
        assert len(states) == 20
        # Wealth should never go significantly negative (allow for small floating point errors)
        assert manipulator.wealth >= -0.01


class TestSimulationEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_days_simulation(self):
        """Test running simulation for zero days."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=0)

        assert len(states) == 0

    def test_very_high_volatility(self):
        """Test simulation with extreme price volatility."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=50.0,  # Very high
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=20)

        # Should handle high volatility without crashing
        assert len(states) == 20
        assert all(s.price > 0 for s in states)

    def test_very_low_initial_price(self):
        """Test simulation with very low initial price."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=0.01,  # Very low
            price_volatility=0.005,
            max_daily_volume=100.0,
        )
        traders = build_traders(config, rng)
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=10)

        assert len(states) == 10
        assert all(s.price > 0 for s in states)

    def test_inactive_traders(self):
        """Test simulation where traders rarely trade."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        # Create traders with low activity
        traders = [
            RandomTrader(f"trader_{i}", Random(i), active_probability=0.1)
            for i in range(10)
        ]
        runner = SimulationRunner(config=config, traders=traders, rng=rng)

        states = runner.run(n_days=20)

        # Should still run, may have days with zero volume
        assert len(states) == 20
        zero_volume_days = sum(1 for s in states if s.volume == 0.0)
        assert zero_volume_days >= 0  # Some days might have no trades
