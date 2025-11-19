"""Tests for trader behavior and order generation logic."""

import pytest
from random import Random
from market_lab.core.traders import Trader, RandomTrader, WealthLimitedTrader, build_traders
from market_lab.core.market import MarketConfig
from market_lab.core.orders import Order


class TestRandomTrader:
    """Test RandomTrader order generation."""

    def test_trader_creation(self):
        """Test basic trader instantiation."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng)
        assert trader.trader_id == "test_trader"
        assert trader.active_probability == 0.8

    def test_trader_with_custom_activity(self):
        """Test trader with custom activity probability."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng, active_probability=0.5)
        assert trader.active_probability == 0.5

    def test_generate_order_returns_order_or_none(self):
        """Test that order generation returns Order or None."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Generate multiple orders to test randomness
        orders = []
        for _ in range(100):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            orders.append(order)

        # Should have mix of orders and None (due to active_probability=0.8)
        order_count = sum(1 for o in orders if o is not None)
        none_count = sum(1 for o in orders if o is None)

        assert order_count > 0
        assert none_count > 0
        assert order_count + none_count == 100

    def test_order_has_correct_properties(self):
        """Test that generated orders have valid properties."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng, active_probability=1.0)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        order = trader.maybe_generate_order(
            last_price=100.0,
            sentiment_value=0.0,
            config=config,
        )

        assert order is not None
        assert order.trader_id == "test_trader"
        assert order.side in ["buy", "sell"]
        assert order.price > 0
        assert order.volume > 0
        assert order.volume <= config.max_daily_volume

    def test_order_respects_sentiment(self):
        """Test that positive sentiment increases price center."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng, active_probability=1.0)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=1.0,
            max_daily_volume=100.0,
        )

        # Generate many orders with positive sentiment
        prices_with_sentiment = []
        for _ in range(50):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=10.0,  # Positive sentiment
                config=config,
            )
            if order:
                prices_with_sentiment.append(order.price)

        # Average should be higher than base price
        avg_price = sum(prices_with_sentiment) / len(prices_with_sentiment)
        assert avg_price > 100.0

    def test_order_respects_price_tick(self):
        """Test that orders respect minimum price tick."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng, active_probability=1.0)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            price_tick=0.5,
        )

        for _ in range(20):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            if order:
                assert order.price >= config.price_tick

    def test_buy_sell_distribution(self):
        """Test that buy/sell orders are roughly balanced."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng, active_probability=1.0)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        buy_count = 0
        sell_count = 0

        for _ in range(200):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            if order:
                if order.side == "buy":
                    buy_count += 1
                else:
                    sell_count += 1

        # Should be roughly 50/50 (allow some variance)
        total = buy_count + sell_count
        assert total > 0
        assert 0.3 <= buy_count / total <= 0.7

    def test_apply_fill_does_nothing(self):
        """Test that RandomTrader.apply_fill is a no-op."""
        rng = Random(42)
        trader = RandomTrader(trader_id="test_trader", rng=rng)
        order = Order("test_trader", "buy", 100.0, 50.0)

        # Should not raise error
        trader.apply_fill(order, price=100.0, volume=50.0)


class TestWealthLimitedTrader:
    """Test WealthLimitedTrader with balance constraints."""

    def test_trader_creation_with_wealth(self):
        """Test creating trader with initial wealth and holdings."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="wealthy_trader",
            rng=rng,
            wealth=50000.0,
            holdings=200.0,
        )
        assert trader.wealth == 50000.0
        assert trader.holdings == 200.0

    def test_buy_order_limited_by_cash(self):
        """Test that buy orders are limited by available cash."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="poor_trader",
            rng=rng,
            wealth=100.0,  # Only $100
            holdings=0.0,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=1000.0,  # Would want to buy more
        )

        # Generate buy orders
        buy_orders = []
        for _ in range(50):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            if order and order.side == "buy":
                buy_orders.append(order)

        # All buy orders should respect cash constraint
        for order in buy_orders:
            max_affordable = trader.wealth / order.price
            assert order.volume <= max_affordable

    def test_sell_order_limited_by_holdings(self):
        """Test that sell orders are limited by available holdings."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="holder_trader",
            rng=rng,
            wealth=100000.0,
            holdings=10.0,  # Only 10 units
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=1000.0,
        )

        # Generate sell orders
        sell_orders = []
        for _ in range(50):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            if order and order.side == "sell":
                sell_orders.append(order)

        # All sell orders should respect holdings constraint
        for order in sell_orders:
            assert order.volume <= trader.holdings

    def test_no_order_when_broke(self):
        """Test that trader with no cash cannot buy."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="broke_trader",
            rng=rng,
            wealth=0.0,
            holdings=0.0,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        # Try many times
        orders = []
        for _ in range(100):
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            if order:
                orders.append(order)

        # Should generate no orders (or very few due to randomness)
        assert len(orders) == 0

    def test_apply_fill_updates_buy_state(self):
        """Test that buying updates cash and holdings correctly."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="buyer_trader",
            rng=rng,
            wealth=10000.0,
            holdings=0.0,
        )
        order = Order("buyer_trader", "buy", 100.0, 50.0)

        initial_wealth = trader.wealth
        initial_holdings = trader.holdings

        # Apply fill
        trader.apply_fill(order, price=100.0, volume=50.0)

        # Wealth should decrease, holdings should increase
        assert trader.wealth == initial_wealth - (100.0 * 50.0)
        assert trader.holdings == initial_holdings + 50.0

    def test_apply_fill_updates_sell_state(self):
        """Test that selling updates cash and holdings correctly."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="seller_trader",
            rng=rng,
            wealth=5000.0,
            holdings=100.0,
        )
        order = Order("seller_trader", "sell", 100.0, 50.0)

        initial_wealth = trader.wealth
        initial_holdings = trader.holdings

        # Apply fill
        trader.apply_fill(order, price=100.0, volume=50.0)

        # Wealth should increase, holdings should decrease
        assert trader.wealth == initial_wealth + (100.0 * 50.0)
        assert trader.holdings == initial_holdings - 50.0

    def test_apply_fill_with_zero_volume(self):
        """Test that zero volume fill doesn't change state."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="trader",
            rng=rng,
            wealth=10000.0,
            holdings=100.0,
        )
        order = Order("trader", "buy", 100.0, 50.0)

        initial_wealth = trader.wealth
        initial_holdings = trader.holdings

        trader.apply_fill(order, price=100.0, volume=0.0)

        assert trader.wealth == initial_wealth
        assert trader.holdings == initial_holdings

    def test_apply_fill_partial_fill(self):
        """Test partial order fills."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="trader",
            rng=rng,
            wealth=10000.0,
            holdings=100.0,
        )
        order = Order("trader", "buy", 100.0, 50.0)

        # Only fill 25 units instead of 50
        trader.apply_fill(order, price=100.0, volume=25.0)

        assert trader.wealth == 10000.0 - (100.0 * 25.0)
        assert trader.holdings == 100.0 + 25.0

    def test_apply_fill_different_price(self):
        """Test that fill price can differ from order price."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="trader",
            rng=rng,
            wealth=10000.0,
            holdings=100.0,
        )
        order = Order("trader", "buy", 100.0, 50.0)  # Order at 100

        # Fill at 95 (better price for buyer)
        trader.apply_fill(order, price=95.0, volume=50.0)

        assert trader.wealth == 10000.0 - (95.0 * 50.0)
        assert trader.holdings == 100.0 + 50.0

    def test_wealth_constraints_prevent_negative_balance(self):
        """Test that trader cannot generate orders leading to negative wealth."""
        rng = Random(42)
        trader = WealthLimitedTrader(
            trader_id="trader",
            rng=rng,
            wealth=100.0,  # Small wealth
            holdings=1000.0,
            active_probability=1.0,
        )
        config = MarketConfig(
            n_traders=10,
            initial_price=1000.0,  # High price
            price_volatility=50.0,
            max_daily_volume=1000.0,
        )

        # Generate many buy orders
        for _ in range(50):
            order = trader.maybe_generate_order(
                last_price=1000.0,
                sentiment_value=0.0,
                config=config,
            )
            if order and order.side == "buy":
                # Order volume should be very small due to limited wealth
                cost = order.price * order.volume
                assert cost <= trader.wealth


class TestBuildTraders:
    """Test trader factory function."""

    def test_build_unlimited_traders(self):
        """Test building traders with unlimited wealth mode."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            wealth_mode="unlimited",
        )

        traders = build_traders(config, rng)

        assert len(traders) == 10
        for trader in traders:
            assert isinstance(trader, RandomTrader)
            assert not isinstance(trader, WealthLimitedTrader)

    def test_build_limited_traders(self):
        """Test building traders with limited wealth mode."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=15,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            wealth_mode="limited",
        )

        traders = build_traders(config, rng)

        assert len(traders) == 15
        for trader in traders:
            assert isinstance(trader, WealthLimitedTrader)
            assert 5000.0 <= trader.wealth <= 15000.0
            assert 0.0 <= trader.holdings <= 20.0

    def test_traders_have_unique_ids(self):
        """Test that all traders get unique IDs."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=20,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        traders = build_traders(config, rng)
        trader_ids = [t.trader_id for t in traders]

        assert len(trader_ids) == len(set(trader_ids))

    def test_traders_have_different_rngs(self):
        """Test that traders get independent random generators."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=5,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        traders = build_traders(config, rng)

        # Generate orders from each trader
        orders = []
        for trader in traders:
            order = trader.maybe_generate_order(
                last_price=100.0,
                sentiment_value=0.0,
                config=config,
            )
            orders.append(order)

        # At least some orders should be different
        # (extremely unlikely all would be identical with independent RNGs)
        prices = [o.price for o in orders if o is not None]
        assert len(set(prices)) > 1

    def test_reproducible_with_seed(self):
        """Test that same seed produces same traders."""
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            wealth_mode="limited",
        )

        # Build traders twice with same seed
        rng1 = Random(42)
        traders1 = build_traders(config, rng1)

        rng2 = Random(42)
        traders2 = build_traders(config, rng2)

        # Should have same wealth and holdings
        for t1, t2 in zip(traders1, traders2):
            assert isinstance(t1, WealthLimitedTrader)
            assert isinstance(t2, WealthLimitedTrader)
            assert t1.wealth == t2.wealth
            assert t1.holdings == t2.holdings

    def test_single_trader(self):
        """Test edge case with only one trader."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=1,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        traders = build_traders(config, rng)

        assert len(traders) == 1
        assert traders[0].trader_id == "trader_0000"

    def test_many_traders(self):
        """Test building large population."""
        rng = Random(42)
        config = MarketConfig(
            n_traders=100,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )

        traders = build_traders(config, rng)

        assert len(traders) == 100
        # Check ID formatting
        assert traders[0].trader_id == "trader_0000"
        assert traders[99].trader_id == "trader_0099"
