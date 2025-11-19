"""Implementation of spoofing market manipulation strategy.

Spoofing involves placing large orders to create false price signals,
then canceling them before execution to manipulate market perception.
"""

from __future__ import annotations

from random import Random

from ..core.market import MarketConfig
from ..core.orders import Order
from ..core.traders import WealthLimitedTrader


class SpoofingManipulator(WealthLimitedTrader):
    """Manipulator that uses spoofing tactics to influence market prices.

    This strategy places large limit orders on one side of the book to create
    the illusion of strong buying or selling pressure, thereby influencing
    other traders' behavior and the market price. These "spoof" orders are
    cancelled before they can be filled.

    The manipulator alternates between:
    1. Placing large spoof orders (buy or sell) to move the price
    2. Placing smaller genuine orders on the opposite side to profit
    3. Cancelling spoof orders before execution

    Attributes:
        spoof_multiplier: Size multiplier for spoof orders relative to normal volume.
            Default is 5.0 (spoof orders are 5x larger than normal).
        spoof_probability: Probability of creating a spoof order on each turn.
            Default is 0.3 (30% chance).
        price_offset: Price offset from last price for spoof orders, as a fraction.
            Default is 0.02 (2% offset).
        cancel_threshold: Days to keep spoof orders before canceling.
            Default is 1 (cancel after 1 day).
        target_side: Preferred side for spoofing ("buy", "sell", or "random").
            Default is "random".

    Example:
        >>> from random import Random
        >>> manipulator = SpoofingManipulator(
        ...     trader_id="spoofer_001",
        ...     rng=Random(42),
        ...     wealth=100_000.0,
        ...     holdings=50.0,
        ...     spoof_multiplier=8.0,
        ...     spoof_probability=0.4,
        ...     price_offset=0.03
        ... )
    """

    def __init__(
        self,
        trader_id: str,
        rng: Random,
        wealth: float = 10_000.0,
        holdings: float = 0.0,
        active_probability: float = 0.8,
        spoof_multiplier: float = 5.0,
        spoof_probability: float = 0.3,
        price_offset: float = 0.02,
        cancel_threshold: int = 1,
        target_side: str = "random",
    ):
        """Initialize the spoofing manipulator.

        Args:
            trader_id: Unique identifier for this trader.
            rng: Random number generator for this trader.
            wealth: Initial wealth (cash) available.
            holdings: Initial holdings (shares) available.
            active_probability: Probability of being active each turn.
            spoof_multiplier: Size multiplier for spoof orders.
            spoof_probability: Probability of creating a spoof order.
            price_offset: Price offset from market for spoof orders (fraction).
            cancel_threshold: Days to keep spoof orders before canceling.
            target_side: Preferred side for spoofing ("buy", "sell", or "random").
        """
        # Initialize parent class manually
        # Note: Can't use super().__init__() with slotted dataclass parent
        object.__setattr__(self, 'trader_id', trader_id)
        object.__setattr__(self, 'rng', rng)
        object.__setattr__(self, 'active_probability', active_probability)
        object.__setattr__(self, 'wealth', wealth)
        object.__setattr__(self, 'holdings', holdings)

        # Initialize own attributes
        self.spoof_multiplier = spoof_multiplier
        self.spoof_probability = spoof_probability
        self.price_offset = price_offset
        self.cancel_threshold = cancel_threshold
        self.target_side = target_side

        # Internal state tracking
        self._spoof_orders: list[tuple[int, Order]] = []
        self._current_day: int = 0

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Generate either a spoof order or a genuine trading order.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Order object if one is generated, None otherwise.
        """
        # Clean up old spoof orders (simulates cancellation)
        self._cleanup_old_spoofs()

        # Decide whether to spoof
        if self.rng.random() < self.spoof_probability:
            return self._generate_spoof_order(
                last_price=last_price,
                config=config
            )
        else:
            # Generate genuine order on opposite side
            return self._generate_genuine_order(
                last_price=last_price,
                sentiment_value=sentiment_value,
                config=config
            )

    def _generate_spoof_order(
        self,
        *,
        last_price: float,
        config: MarketConfig,
    ) -> Order | None:
        """Create a large spoof order to manipulate price perception.

        Args:
            last_price: Current market price.
            config: Market configuration parameters.

        Returns:
            Large spoof order or None if constraints prevent it.
        """
        # Determine spoof side
        if self.target_side == "random":
            spoof_side = "buy" if self.rng.random() < 0.5 else "sell"
        else:
            spoof_side = self.target_side

        # Calculate spoof price (offset from market)
        if spoof_side == "buy":
            # Place buy orders below market to suggest support
            price = max(last_price * (1 - self.price_offset), config.price_tick)
        else:
            # Place sell orders above market to suggest resistance
            price = last_price * (1 + self.price_offset)

        # Calculate large volume for spoof
        base_volume = self._draw_volume(config)
        spoof_volume = base_volume * self.spoof_multiplier

        # Apply wealth constraints
        if spoof_side == "buy":
            max_volume = self.wealth / max(price, config.price_tick)
            max_volume = min(max_volume, config.max_daily_volume * self.spoof_multiplier)
        else:
            max_volume = min(self.holdings, config.max_daily_volume * self.spoof_multiplier)

        if max_volume <= 0:
            return None

        volume = min(spoof_volume, max_volume)
        if volume <= 0:
            return None

        # Create and track spoof order
        order = Order(
            trader_id=f"{self.trader_id}_spoof_{len(self._spoof_orders)}",
            side=spoof_side,
            price=price,
            volume=volume
        )

        # Track this as a spoof order
        self._spoof_orders.append((self._current_day, order))
        self._current_day += 1

        return order

    def _generate_genuine_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Create a genuine order to profit from price movement.

        This order is placed on the opposite side of the spoof orders
        to capitalize on the price movement they create.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Genuine trading order or None.
        """
        # Check if active
        if self.rng.random() > self.active_probability:
            return None

        # Generate random order
        side = "buy" if self.rng.random() < 0.5 else "sell"
        price = self._draw_price(last_price=last_price, sentiment_value=sentiment_value, config=config)
        volume = self._draw_volume(config)

        # Apply wealth constraints (from WealthLimitedTrader logic)
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

        # Adjust price to be more aggressive if we have active spoofs
        if self._spoof_orders:
            latest_spoof = self._spoof_orders[-1][1]
            if latest_spoof.side == "buy" and side == "sell":
                # If spoofing buy pressure, sell at higher price
                price = max(price * 1.01, config.price_tick)
            elif latest_spoof.side == "sell" and side == "buy":
                # If spoofing sell pressure, buy at lower price
                price = max(price * 0.99, config.price_tick)

        return Order(trader_id=self.trader_id, side=side, price=price, volume=volume)

    def _cleanup_old_spoofs(self) -> None:
        """Remove spoof orders that are older than cancel_threshold.

        This simulates the cancellation of spoof orders before they execute.
        """
        if not self._spoof_orders:
            return

        # Filter out old spoofs
        cutoff_day = self._current_day - self.cancel_threshold
        self._spoof_orders = [
            (day, order) for day, order in self._spoof_orders
            if day >= cutoff_day
        ]


__all__ = ["SpoofingManipulator"]
