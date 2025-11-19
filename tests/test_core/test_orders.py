"""
Tests for core.orders module.
"""

import pytest
from market_lab.core.orders import Order, aggregate_orders, allocate_fills


def test_order_creation():
    """Test that orders are created correctly."""
    order = Order(
        trader_id=1,
        is_buy=True,
        price_limit=100.0,
        volume=10
    )

    assert order.trader_id == 1
    assert order.is_buy is True
    assert order.price_limit == 100.0
    assert order.volume == 10


def test_order_validation():
    """Test that invalid orders raise ValueError."""
    with pytest.raises(ValueError, match="volume must be positive"):
        Order(trader_id=1, is_buy=True, price_limit=100.0, volume=0)

    with pytest.raises(ValueError, match="price_limit must be positive"):
        Order(trader_id=1, is_buy=True, price_limit=-10.0, volume=10)


def test_aggregate_orders_empty():
    """Test aggregation with no orders."""
    curves = aggregate_orders([], n_price_points=10, min_price=50, max_price=150)

    assert len(curves.price_grid) == 10
    assert all(v == 0 for v in curves.buy_volume)
    assert all(v == 0 for v in curves.sell_volume)


def test_aggregate_orders_single_buy():
    """Test aggregation with single buy order."""
    orders = [Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10)]
    curves = aggregate_orders(orders, n_price_points=10, min_price=50, max_price=150)

    # Buy volume should be non-zero at prices <= 100
    assert any(v > 0 for v in curves.buy_volume)


def test_allocate_fills_no_volume():
    """Test allocation when no volume is cleared."""
    orders = [Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10)]
    fills = allocate_fills(orders, cleared_volume=0.0, is_buy=True)

    assert all(f == 0.0 for f in fills)


def test_allocate_fills_partial():
    """Test partial fills are distributed proportionally."""
    orders = [
        Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10),
        Order(trader_id=2, is_buy=True, price_limit=100.0, volume=20),
    ]
    fills = allocate_fills(orders, cleared_volume=15.0, is_buy=True)

    # Should fill proportionally: 5 and 10
    assert abs(fills[0] - 5.0) < 0.01
    assert abs(fills[1] - 10.0) < 0.01
