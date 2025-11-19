"""
Pytest configuration and shared fixtures.
"""

import pytest
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
import random


@pytest.fixture
def rng():
    """Provides a seeded random number generator for reproducible tests."""
    return random.Random(42)


@pytest.fixture
def basic_config():
    """Provides a basic market configuration for tests."""
    return MarketConfig(
        n_traders=10,
        initial_price=100.0,
        initial_cash=10000.0,
        initial_holdings=100,
        min_price=50.0,
        max_price=200.0,
        n_price_points=50
    )


@pytest.fixture
def traders(basic_config, rng):
    """Provides a list of traders for tests."""
    return build_traders(basic_config, rng)
