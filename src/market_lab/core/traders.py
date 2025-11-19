"""Trader definitions used by the simulation."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .market import MarketConfig
from .orders import Order


@dataclass(slots=True)
class Trader:
    """Base class for agents that can submit orders."""

    trader_id: str
    rng: Random

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        raise NotImplementedError

    def apply_fill(self, order: Order, *, price: float, volume: float) -> None:
        """Update internal state after execution. Default trader is unlimited."""

    def _draw_price(self, *, last_price: float, sentiment_value: float, config: MarketConfig) -> float:
        center = max(last_price + sentiment_value, config.price_tick)
        price = self.rng.gauss(center, config.price_volatility)
        return max(price, config.price_tick)

    def _draw_volume(self, config: MarketConfig) -> float:
        return self.rng.uniform(0.1, config.max_daily_volume)


@dataclass(slots=True)
class RandomTrader(Trader):
    """Trader that ignores wealth constraints."""

    active_probability: float = 0.8

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        if self.rng.random() > self.active_probability:
            return None

        side = "buy" if self.rng.random() < 0.5 else "sell"
        price = self._draw_price(last_price=last_price, sentiment_value=sentiment_value, config=config)
        volume = self._draw_volume(config)
        return Order(trader_id=self.trader_id, side=side, price=price, volume=volume)


@dataclass(slots=True)
class WealthLimitedTrader(RandomTrader):
    """Trader constrained by available cash and holdings."""

    wealth: float = 10_000.0
    holdings: float = 0.0

    def maybe_generate_order(
        self,
        *,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
    ) -> Order | None:
        order = super().maybe_generate_order(last_price=last_price, sentiment_value=sentiment_value, config=config)
        if order is None:
            return None

        if order.side == "buy":
            max_volume = self.wealth / max(order.price, config.price_tick)
            max_volume = min(max_volume, config.max_daily_volume)
        else:
            max_volume = min(self.holdings, config.max_daily_volume)

        if max_volume <= 0:
            return None

        volume = min(order.volume, max_volume)
        if volume <= 0:
            return None
        return Order(trader_id=order.trader_id, side=order.side, price=order.price, volume=volume)

    def apply_fill(self, order: Order, *, price: float, volume: float) -> None:
        if volume <= 0:
            return
        if order.side == "buy":
            cost = price * volume
            self.wealth -= cost
            self.holdings += volume
        else:
            proceeds = price * volume
            self.wealth += proceeds
            self.holdings -= volume


def build_traders(config: MarketConfig, rng: Random) -> list[Trader]:
    """Factory helper used by experiments to create default trader populations."""

    traders: list[Trader] = []
    for idx in range(config.n_traders):
        trader_rng = Random(rng.randrange(0, 10**9))
        trader_id = f"trader_{idx:04d}"
        if config.wealth_mode == "limited":
            wealth = trader_rng.uniform(5_000, 15_000)
            holdings = trader_rng.uniform(0, 20)
            trader = WealthLimitedTrader(trader_id=trader_id, rng=trader_rng, wealth=wealth, holdings=holdings)
        else:
            trader = RandomTrader(trader_id=trader_id, rng=trader_rng)
        traders.append(trader)
    return traders


__all__ = [
    "Trader",
    "RandomTrader",
    "WealthLimitedTrader",
    "build_traders",
]
