"""Implementation of layering market manipulation strategy.

Layering (also known as quote stuffing) involves placing multiple orders
at different price levels to create a false impression of market depth
and liquidity, then systematically removing them.
"""

from __future__ import annotations

from random import Random

from ..core.market import MarketConfig
from ..core.orders import Order
from ..core.traders import WealthLimitedTrader


class LayeringManipulator(WealthLimitedTrader):
    """Manipulator that uses layering to create false liquidity impressions.

    Layering is a sophisticated manipulation technique where a trader places
    multiple limit orders at different price levels (layers) on one side of
    the order book to create the illusion of strong support or resistance.
    This false liquidity can influence other traders' perceptions and decisions.

    The strategy works in phases:
    1. BUILD: Create multiple layers of orders at incremental price levels
    2. MAINTAIN: Keep layers active to influence market perception
    3. REMOVE: Systematically cancel layers before execution
    4. PROFIT: Execute genuine orders on the opposite side at favorable prices

    The manipulator creates a "wall" of orders that appears to provide liquidity
    but is actually intended to move the price without the orders being filled.

    Attributes:
        n_layers: Number of price layers to create.
            Default is 5.
        layer_spacing: Price difference between layers as fraction of price.
            Default is 0.005 (0.5% spacing).
        volume_decay: Volume reduction factor for each successive layer.
            Default is 0.8 (each layer is 80% of previous).
        layer_probability: Probability of adding/maintaining layers each turn.
            Default is 0.6 (60% chance).
        removal_rate: Probability of removing a layer each turn during removal phase.
            Default is 0.3 (30% chance per layer).
        phase_duration: Number of turns to maintain each phase.
            Default is 10.
        target_side: Side for layering ("buy", "sell", or "random").
            Default is "random".
        base_volume_multiplier: Size multiplier for base layer volume.
            Default is 4.0.

    Example:
        >>> from random import Random
        >>> manipulator = LayeringManipulator(
        ...     trader_id="layer_001",
        ...     rng=Random(42),
        ...     wealth=100_000.0,
        ...     holdings=100.0,
        ...     n_layers=7,
        ...     layer_spacing=0.003,
        ...     volume_decay=0.75,
        ...     target_side="buy"
        ... )
    """

    def __init__(
        self,
        trader_id: str,
        rng: Random,
        wealth: float = 10_000.0,
        holdings: float = 0.0,
        active_probability: float = 0.8,
        n_layers: int = 5,
        layer_spacing: float = 0.005,
        volume_decay: float = 0.8,
        layer_probability: float = 0.6,
        removal_rate: float = 0.3,
        phase_duration: int = 10,
        target_side: str = "random",
        base_volume_multiplier: float = 4.0,
    ):
        """Initialize the layering manipulator.

        Args:
            trader_id: Unique identifier for this trader.
            rng: Random number generator for this trader.
            wealth: Initial wealth (cash) available.
            holdings: Initial holdings (shares) available.
            active_probability: Probability of being active each turn.
            n_layers: Number of price layers to create.
            layer_spacing: Price difference between layers as fraction.
            volume_decay: Volume reduction factor for each layer.
            layer_probability: Probability of adding/maintaining layers.
            removal_rate: Probability of removing a layer during removal phase.
            phase_duration: Number of turns to maintain each phase.
            target_side: Side for layering ("buy", "sell", or "random").
            base_volume_multiplier: Size multiplier for base layer volume.
        """
        # Initialize parent class manually
        object.__setattr__(self, 'trader_id', trader_id)
        object.__setattr__(self, 'rng', rng)
        object.__setattr__(self, 'active_probability', active_probability)
        object.__setattr__(self, 'wealth', wealth)
        object.__setattr__(self, 'holdings', holdings)

        # Initialize own attributes
        self.n_layers = n_layers
        self.layer_spacing = layer_spacing
        self.volume_decay = volume_decay
        self.layer_probability = layer_probability
        self.removal_rate = removal_rate
        self.phase_duration = phase_duration
        self.target_side = target_side
        self.base_volume_multiplier = base_volume_multiplier

        # Internal state
        self._phase: str = "build"
        self._phase_counter: int = 0
        self._active_layers: list[tuple[int, Order]] = []
        self._current_side: str | None = None
        self._cycle_counter: int = 0

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Generate orders based on current layering phase.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Order object if one is generated, None otherwise.
        """
        # Update phase if duration exceeded
        self._update_phase()

        # Execute phase-specific logic
        if self._phase == "build":
            return self._build_layer(last_price=last_price, config=config)
        elif self._phase == "maintain":
            return self._maintain_layers(last_price=last_price, config=config)
        elif self._phase == "remove":
            return self._remove_layer()
        else:  # profit phase
            return self._generate_profit_order(
                last_price=last_price,
                sentiment_value=sentiment_value,
                config=config
            )

    def _update_phase(self) -> None:
        """Progress through manipulation phases."""
        self._phase_counter += 1

        if self._phase_counter >= self.phase_duration:
            self._phase_counter = 0

            # Transition to next phase
            if self._phase == "build":
                self._phase = "maintain"
            elif self._phase == "maintain":
                self._phase = "remove"
            elif self._phase == "remove":
                self._phase = "profit"
                self._active_layers = []  # Clear all layers
            else:  # profit phase
                self._phase = "build"
                self._cycle_counter += 1
                # Potentially switch sides
                if self.target_side == "random":
                    self._current_side = None

    def _get_layer_side(self) -> str:
        """Determine which side to place layers on."""
        if self._current_side is not None:
            return self._current_side

        if self.target_side == "random":
            side = "buy" if self.rng.random() < 0.5 else "sell"
        else:
            side = self.target_side

        object.__setattr__(self, '_current_side', side)
        return side

    def _build_layer(
        self,
        *,
        last_price: float,
        config: MarketConfig,
    ) -> Order | None:
        """Add a new layer to the order book.

        Args:
            last_price: Current market price.
            config: Market configuration parameters.

        Returns:
            New layer order or None.
        """
        # Check if we should add a layer
        if self.rng.random() > self.layer_probability:
            return None

        # Don't exceed max layers
        if len(self._active_layers) >= self.n_layers:
            return None

        side = self._get_layer_side()
        layer_index = len(self._active_layers)

        # Calculate price for this layer
        if side == "buy":
            # Place buy layers below market price
            price_offset = (layer_index + 1) * self.layer_spacing
            price = max(last_price * (1 - price_offset), config.price_tick)
        else:
            # Place sell layers above market price
            price_offset = (layer_index + 1) * self.layer_spacing
            price = last_price * (1 + price_offset)

        # Calculate volume with decay
        base_volume = self._draw_volume(config) * self.base_volume_multiplier
        layer_volume = base_volume * (self.volume_decay ** layer_index)

        # Apply wealth constraints
        if side == "buy":
            max_volume = self.wealth / max(price, config.price_tick)
            max_volume = min(max_volume, config.max_daily_volume * self.base_volume_multiplier)
        else:
            max_volume = min(self.holdings, config.max_daily_volume * self.base_volume_multiplier)

        if max_volume <= 0:
            return None

        volume = min(layer_volume, max_volume)
        if volume <= 0:
            return None

        # Create layer order
        order = Order(
            trader_id=f"{self.trader_id}_layer_{self._cycle_counter}_{layer_index}",
            side=side,
            price=price,
            volume=volume
        )

        # Track this layer
        self._active_layers.append((layer_index, order))

        return order

    def _maintain_layers(
        self,
        *,
        last_price: float,
        config: MarketConfig,
    ) -> Order | None:
        """Maintain existing layers, occasionally refreshing them.

        Args:
            last_price: Current market price.
            config: Market configuration parameters.

        Returns:
            Refreshed layer order or None.
        """
        if not self._active_layers:
            return None

        # Occasionally refresh a random layer to keep it visible
        if self.rng.random() < self.layer_probability * 0.5:
            # Pick a random layer to refresh
            layer_idx = self.rng.randrange(len(self._active_layers))
            _, old_order = self._active_layers[layer_idx]

            # Create refreshed order with slight price/volume variation
            price_variation = self.rng.gauss(1.0, 0.001)
            volume_variation = self.rng.gauss(1.0, 0.05)

            new_price = max(old_order.price * price_variation, config.price_tick)
            new_volume = max(old_order.volume * volume_variation, 0.1)

            new_order = Order(
                trader_id=f"{old_order.trader_id}_refresh",
                side=old_order.side,
                price=new_price,
                volume=new_volume
            )

            # Update the layer
            self._active_layers[layer_idx] = (layer_idx, new_order)

            return new_order

        return None

    def _remove_layer(self) -> Order | None:
        """Systematically remove layers (simulates cancellation).

        Returns:
            None (layers are cancelled, not new orders generated).
        """
        if not self._active_layers:
            return None

        # Remove layers with some probability
        if self.rng.random() < self.removal_rate and self._active_layers:
            # Remove from outermost layer first
            self._active_layers.pop()

        return None

    def _generate_profit_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        """Generate genuine order on opposite side to profit from manipulation.

        Args:
            last_price: Current market price.
            sentiment_value: Market sentiment indicator.
            config: Market configuration parameters.

        Returns:
            Profit-taking order or None.
        """
        if self._current_side is None:
            return None

        # Trade on opposite side of the layers
        profit_side = "sell" if self._current_side == "buy" else "buy"

        # Calculate favorable price based on manipulation direction
        if profit_side == "sell":
            # If we layered buy orders, sell at elevated price
            price = last_price * 1.01
        else:
            # If we layered sell orders, buy at depressed price
            price = max(last_price * 0.99, config.price_tick)

        # Use moderate volume for profit orders
        volume = self._draw_volume(config)

        # Apply wealth constraints
        if profit_side == "buy":
            max_volume = self.wealth / max(price, config.price_tick)
            max_volume = min(max_volume, config.max_daily_volume)
        else:
            max_volume = min(self.holdings, config.max_daily_volume)

        if max_volume <= 0:
            return None

        volume = min(volume, max_volume)
        if volume <= 0:
            return None

        return Order(
            trader_id=f"{self.trader_id}_profit_{self._cycle_counter}",
            side=profit_side,
            price=price,
            volume=volume
        )


__all__ = ["LayeringManipulator"]
