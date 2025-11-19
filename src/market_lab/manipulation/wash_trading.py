"""Implementation of wash trading market manipulation strategy.

Wash trading involves simultaneously buying and selling the same asset
to create artificial trading volume and give the appearance of market activity.
"""

from __future__ import annotations

from random import Random

from ..core.market import MarketConfig
from ..core.orders import Order
from ..core.traders import WealthLimitedTrader


class WashTradingManipulator(WealthLimitedTrader):
    """Manipulator that uses wash trading to create artificial volume.

    Wash trading is a form of market manipulation where a trader simultaneously
    buys and sells the same asset, often through different accounts or order IDs,
    to create misleading market activity. This gives the false impression of
    high liquidity and market interest, potentially attracting other traders.

    The manipulator:
    1. Places matching buy and sell orders at similar prices
    2. Creates artificial volume without changing net position
    3. Maintains approximately neutral holdings over time
    4. Uses small price spreads to ensure both orders execute

    This implementation simulates wash trading by:
    - Generating paired buy/sell orders at tight spreads
    - Tracking order pairs to maintain position neutrality
    - Varying timing and size to appear more natural

    Attributes:
        wash_probability: Probability of generating wash trades on each turn.
            Default is 0.5 (50% chance).
        volume_multiplier: Size multiplier for wash trades relative to normal volume.
            Default is 3.0 (wash trades are 3x larger).
        price_spread: Price spread between buy and sell as a fraction of price.
            Default is 0.001 (0.1% spread).
        pairs_per_session: Number of buy/sell pairs to create per session.
            Default is 2.
        randomize_timing: Whether to randomize order timing within pairs.
            Default is True.
        max_position_drift: Maximum allowed drift from initial holdings as a fraction.
            Default is 0.1 (10% drift allowed).

    Example:
        >>> from random import Random
        >>> manipulator = WashTradingManipulator(
        ...     trader_id="washer_001",
        ...     rng=Random(42),
        ...     wealth=100_000.0,
        ...     holdings=100.0,
        ...     wash_probability=0.6,
        ...     volume_multiplier=4.0,
        ...     price_spread=0.0005
        ... )
    """

    def __init__(
        self,
        trader_id: str,
        rng: Random,
        wealth: float = 10_000.0,
        holdings: float = 0.0,
        active_probability: float = 0.8,
        wash_probability: float = 0.5,
        volume_multiplier: float = 3.0,
        price_spread: float = 0.001,
        pairs_per_session: int = 2,
        randomize_timing: bool = True,
        max_position_drift: float = 0.1,
    ):
        """Initialize the wash trading manipulator.

        Args:
            trader_id: Unique identifier for this trader.
            rng: Random number generator for this trader.
            wealth: Initial wealth (cash) available.
            holdings: Initial holdings (shares) available.
            active_probability: Probability of being active each turn.
            wash_probability: Probability of generating wash trades.
            volume_multiplier: Size multiplier for wash trades.
            price_spread: Price spread between buy/sell as fraction.
            pairs_per_session: Number of buy/sell pairs per session.
            randomize_timing: Whether to randomize order timing.
            max_position_drift: Maximum allowed drift from initial holdings.
        """
        # Initialize parent class manually
        object.__setattr__(self, 'trader_id', trader_id)
        object.__setattr__(self, 'rng', rng)
        object.__setattr__(self, 'active_probability', active_probability)
        object.__setattr__(self, 'wealth', wealth)
        object.__setattr__(self, 'holdings', holdings)

        # Initialize own attributes
        self.wash_probability = wash_probability
        self.volume_multiplier = volume_multiplier
        self.price_spread = price_spread
        self.pairs_per_session = pairs_per_session
        self.randomize_timing = randomize_timing
        self.max_position_drift = max_position_drift

        # Internal state
        self._initial_holdings: float = holdings
        self._pending_pairs: list[tuple[Order, Order]] = []
        self._current_pair_index: int = 0
        self._session_counter: int = 0

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Generate wash trading orders or regular orders.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Order object if one is generated, None otherwise.
        """
        # Check if we should engage in wash trading
        if self.rng.random() < self.wash_probability:
            return self._generate_wash_order(
                last_price=last_price,
                config=config
            )
        else:
            # Generate normal order occasionally
            return self._generate_rebalancing_order(
                last_price=last_price,
                sentiment_value=sentiment_value,
                config=config
            )

    def _generate_wash_order(
        self,
        *,
        last_price: float,
        config: MarketConfig,
    ) -> Order | None:
        """Create matching buy/sell orders for wash trading.

        Args:
            last_price: Current market price.
            config: Market configuration parameters.

        Returns:
            One order from a wash trading pair, or None.
        """
        # Generate new pairs if we've exhausted current batch
        if self._current_pair_index >= len(self._pending_pairs):
            self._generate_wash_pairs(last_price=last_price, config=config)
            self._current_pair_index = 0
            self._session_counter += 1

        # Return next order from pending pairs
        if self._current_pair_index < len(self._pending_pairs):
            buy_order, sell_order = self._pending_pairs[self._current_pair_index]

            # Alternate between buy and sell, or randomize
            if self.randomize_timing:
                order = buy_order if self.rng.random() < 0.5 else sell_order
            else:
                # Alternate systematically
                order = buy_order if self._current_pair_index % 2 == 0 else sell_order

            self._current_pair_index += 1
            return order

        return None

    def _generate_wash_pairs(
        self,
        *,
        last_price: float,
        config: MarketConfig,
    ) -> None:
        """Generate a batch of matching buy/sell order pairs.

        Args:
            last_price: Current market price.
            config: Market configuration parameters.
        """
        self._pending_pairs = []

        for pair_idx in range(self.pairs_per_session):
            # Calculate wash trade prices with tight spread
            spread_amount = last_price * self.price_spread
            buy_price = max(last_price - spread_amount / 2, config.price_tick)
            sell_price = last_price + spread_amount / 2

            # Add small random variation to make it less obvious
            if self.randomize_timing:
                price_variation = self.rng.gauss(0, spread_amount * 0.1)
                buy_price = max(buy_price + price_variation, config.price_tick)
                sell_price = max(sell_price + price_variation, config.price_tick)

            # Calculate volume for this pair
            base_volume = self._draw_volume(config)
            wash_volume = base_volume * self.volume_multiplier

            # Add slight variation to each order in pair
            buy_volume = wash_volume * self.rng.uniform(0.95, 1.05)
            sell_volume = wash_volume * self.rng.uniform(0.95, 1.05)

            # Apply wealth constraints
            max_buy_volume = self.wealth / max(buy_price, config.price_tick)
            max_buy_volume = min(max_buy_volume, config.max_daily_volume * self.volume_multiplier)
            buy_volume = min(buy_volume, max_buy_volume)

            max_sell_volume = min(self.holdings, config.max_daily_volume * self.volume_multiplier)
            sell_volume = min(sell_volume, max_sell_volume)

            # Only create pair if both orders are valid
            if buy_volume > 0 and sell_volume > 0:
                buy_order = Order(
                    trader_id=f"{self.trader_id}_wash_buy_{self._session_counter}_{pair_idx}",
                    side="buy",
                    price=buy_price,
                    volume=buy_volume
                )

                sell_order = Order(
                    trader_id=f"{self.trader_id}_wash_sell_{self._session_counter}_{pair_idx}",
                    side="sell",
                    price=sell_price,
                    volume=sell_volume
                )

                self._pending_pairs.append((buy_order, sell_order))

    def _generate_rebalancing_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Generate an order to rebalance position back to initial holdings.

        Wash trading should maintain a neutral position, so periodically
        rebalance if holdings drift too far from initial state.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Rebalancing order or None.
        """
        # Check if we've drifted too far from initial holdings
        drift = abs(self.holdings - self._initial_holdings)
        max_drift = self._initial_holdings * self.max_position_drift

        if drift > max_drift:
            # Rebalance towards initial holdings
            if self.holdings > self._initial_holdings:
                # Sell excess
                volume = min(drift, config.max_daily_volume)
                if volume > 0:
                    return Order(
                        trader_id=f"{self.trader_id}_rebalance",
                        side="sell",
                        price=last_price,
                        volume=volume
                    )
            else:
                # Buy to reach initial holdings
                volume = drift
                max_volume = self.wealth / max(last_price, config.price_tick)
                volume = min(volume, max_volume, config.max_daily_volume)
                if volume > 0:
                    return Order(
                        trader_id=f"{self.trader_id}_rebalance",
                        side="buy",
                        price=last_price,
                        volume=volume
                    )

        # Otherwise generate normal order
        # Check if active
        if self.rng.random() > self.active_probability:
            return None

        # Generate random order
        side = "buy" if self.rng.random() < 0.5 else "sell"
        price = self._draw_price(last_price=last_price, sentiment_value=sentiment_value, config=config)
        volume = self._draw_volume(config)

        # Apply wealth constraints
        if side == "buy":
            max_volume = self.wealth / max(price, config.price_tick)
            max_volume = min(max_volume, config.max_daily_volume)
        else:
            max_volume = min(self.holdings, config.max_daily_volume)

        if max_volume <= 0:
            return None

        volume = min(volume, max_volume)
        if volume <= 0:
            return None

        return Order(trader_id=self.trader_id, side=side, price=price, volume=volume)

    def apply_fill(self, order: Order, *, price: float, volume: float) -> None:
        """Update wealth and holdings after order execution.

        Args:
            order: The order that was filled.
            price: Execution price.
            volume: Executed volume.
        """
        # Use parent class logic to update state
        super().apply_fill(order, price=price, volume=volume)


__all__ = ["WashTradingManipulator"]
