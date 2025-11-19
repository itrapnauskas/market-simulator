"""Tests for market configuration and auction pricing logic."""

import pytest
from market_lab.core.market import MarketConfig, MarketState, find_equilibrium_price
from market_lab.core.orders import Order, OrderCurves, build_order_curves


class TestMarketConfig:
    """Test MarketConfig dataclass."""

    def test_basic_config_creation(self):
        """Test creating a basic market configuration."""
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
        )
        assert config.n_traders == 10
        assert config.initial_price == 100.0
        assert config.price_volatility == 5.0
        assert config.max_daily_volume == 100.0
        assert config.wealth_mode == "unlimited"
        assert config.sentiment_mode == "none"
        assert config.price_tick == 1.0
        assert config.seed is None

    def test_config_with_custom_wealth_mode(self):
        """Test config with limited wealth mode."""
        config = MarketConfig(
            n_traders=5,
            initial_price=50.0,
            price_volatility=2.0,
            max_daily_volume=50.0,
            wealth_mode="limited",
        )
        assert config.wealth_mode == "limited"

    def test_config_with_seed(self):
        """Test config with random seed."""
        config = MarketConfig(
            n_traders=20,
            initial_price=200.0,
            price_volatility=10.0,
            max_daily_volume=200.0,
            seed=42,
        )
        assert config.seed == 42

    def test_config_with_custom_price_tick(self):
        """Test config with custom price tick."""
        config = MarketConfig(
            n_traders=10,
            initial_price=100.0,
            price_volatility=5.0,
            max_daily_volume=100.0,
            price_tick=0.01,
        )
        assert config.price_tick == 0.01


class TestMarketState:
    """Test MarketState dataclass."""

    def test_basic_state_creation(self):
        """Test creating a basic market state."""
        state = MarketState(
            day=1,
            price=100.0,
            volume=500.0,
            sentiment_value=0.5,
        )
        assert state.day == 1
        assert state.price == 100.0
        assert state.volume == 500.0
        assert state.sentiment_value == 0.5
        assert state.order_curves is None
        assert state.manipulation_score is None

    def test_state_with_order_curves(self):
        """Test state with order curves attached."""
        curves = OrderCurves(
            price_grid=[90.0, 100.0, 110.0],
            buy_curve=[300.0, 200.0, 100.0],
            sell_curve=[100.0, 200.0, 300.0],
        )
        state = MarketState(
            day=5,
            price=100.0,
            volume=200.0,
            sentiment_value=0.0,
            order_curves=curves,
        )
        assert state.order_curves is not None
        assert state.order_curves.price_grid == [90.0, 100.0, 110.0]

    def test_state_with_manipulation_score(self):
        """Test state with manipulation detection score."""
        state = MarketState(
            day=10,
            price=150.0,
            volume=1000.0,
            sentiment_value=-1.0,
            manipulation_score=0.85,
        )
        assert state.manipulation_score == 0.85


class TestFindEquilibriumPrice:
    """Test auction pricing algorithm."""

    def test_equilibrium_with_single_crossing(self):
        """Test equilibrium when demand and supply cross once."""
        # Create orders: buyers willing to pay up to 105, sellers willing to accept 95+
        buy_orders = [
            Order("buyer1", "buy", 105.0, 100.0),
            Order("buyer2", "buy", 100.0, 150.0),
            Order("buyer3", "buy", 95.0, 50.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 95.0, 80.0),
            Order("seller2", "sell", 100.0, 120.0),
            Order("seller3", "sell", 105.0, 100.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # At price 100, we should have meaningful volume
        assert 95.0 <= price <= 105.0
        assert volume > 0

    def test_equilibrium_with_perfect_match(self):
        """Test equilibrium when buy and sell match exactly."""
        buy_orders = [
            Order("buyer1", "buy", 100.0, 100.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 100.0, 100.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        assert price == 100.0
        assert volume == 100.0

    def test_equilibrium_with_no_overlap(self):
        """Test when buyers won't meet sellers' prices."""
        buy_orders = [
            Order("buyer1", "buy", 90.0, 100.0),
            Order("buyer2", "buy", 85.0, 150.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 110.0, 100.0),
            Order("seller2", "sell", 115.0, 150.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # No overlap means zero volume
        assert volume == 0.0

    def test_equilibrium_with_zero_volume(self):
        """Test edge case with no orders."""
        curves = OrderCurves(
            price_grid=[100.0],
            buy_curve=[0.0],
            sell_curve=[0.0],
        )

        price, volume = find_equilibrium_price(curves)

        assert price == 100.0  # Should return last price in grid
        assert volume == 0.0

    def test_equilibrium_with_empty_grid(self):
        """Test edge case with empty price grid."""
        curves = OrderCurves(
            price_grid=[],
            buy_curve=[],
            sell_curve=[],
        )

        price, volume = find_equilibrium_price(curves)

        assert price == 0.0
        assert volume == 0.0

    def test_equilibrium_with_only_buyers(self):
        """Test when only buy orders exist."""
        buy_orders = [
            Order("buyer1", "buy", 100.0, 100.0),
            Order("buyer2", "buy", 95.0, 50.0),
        ]
        sell_orders = []

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # No sellers means zero volume
        assert volume == 0.0

    def test_equilibrium_with_only_sellers(self):
        """Test when only sell orders exist."""
        buy_orders = []
        sell_orders = [
            Order("seller1", "sell", 100.0, 100.0),
            Order("seller2", "sell", 105.0, 50.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # No buyers means zero volume
        assert volume == 0.0

    def test_equilibrium_with_multiple_price_candidates(self):
        """Test when multiple prices yield the same max volume."""
        # Create flat satisfaction curve
        buy_orders = [
            Order("buyer1", "buy", 105.0, 100.0),
            Order("buyer2", "buy", 100.0, 100.0),
            Order("buyer3", "buy", 95.0, 100.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 95.0, 100.0),
            Order("seller2", "sell", 100.0, 100.0),
            Order("seller3", "sell", 105.0, 100.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # Should return average of candidate prices
        # Volume is higher due to order aggregation
        assert volume > 0
        assert 95.0 <= price <= 105.0

    def test_equilibrium_with_large_orders(self):
        """Test with realistic large order volumes."""
        buy_orders = [
            Order("buyer1", "buy", 100.5, 1000.0),
            Order("buyer2", "buy", 100.0, 2000.0),
            Order("buyer3", "buy", 99.5, 1500.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 99.5, 1200.0),
            Order("seller2", "sell", 100.0, 1800.0),
            Order("seller3", "sell", 100.5, 1000.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=0.5)
        price, volume = find_equilibrium_price(curves)

        assert volume > 0
        assert 99.5 <= price <= 100.5

    def test_equilibrium_price_tick_sensitivity(self):
        """Test that price tick affects the equilibrium calculation."""
        buy_orders = [Order("buyer1", "buy", 100.0, 100.0)]
        sell_orders = [Order("seller1", "sell", 100.0, 100.0)]

        # Test with different price ticks
        curves_1 = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price_1, volume_1 = find_equilibrium_price(curves_1)

        curves_01 = build_order_curves(buy_orders, sell_orders, price_tick=0.1)
        price_01, volume_01 = find_equilibrium_price(curves_01)

        # Both should find the same volume, price should be at 100
        assert volume_1 == volume_01 == 100.0
        assert price_1 == price_01 == 100.0

    def test_equilibrium_with_aggressive_buyers(self):
        """Test when buyers are very aggressive (high prices)."""
        buy_orders = [
            Order("buyer1", "buy", 150.0, 100.0),
            Order("buyer2", "buy", 140.0, 200.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 100.0, 150.0),
            Order("seller2", "sell", 105.0, 150.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # Should clear at a price favorable to sellers
        assert volume > 0
        assert price >= 100.0

    def test_equilibrium_with_aggressive_sellers(self):
        """Test when sellers are very aggressive (low prices)."""
        buy_orders = [
            Order("buyer1", "buy", 100.0, 150.0),
            Order("buyer2", "buy", 95.0, 150.0),
        ]
        sell_orders = [
            Order("seller1", "sell", 50.0, 100.0),
            Order("seller2", "sell", 60.0, 200.0),
        ]

        curves = build_order_curves(buy_orders, sell_orders, price_tick=1.0)
        price, volume = find_equilibrium_price(curves)

        # Should clear at a price favorable to buyers
        assert volume > 0
        assert price <= 100.0
