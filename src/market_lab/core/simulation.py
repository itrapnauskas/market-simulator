"""Simulation runner that orchestrates traders and the market."""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Dict, Iterable, List

from .market import MarketConfig, MarketState, find_equilibrium_price
from .orders import Order, build_order_curves, allocate_fills
from .sentiment import NoSentiment, SentimentCurve
from .traders import Trader


@dataclass
class SimulationRunner:
    """Coordinates the simulation loop for a configured market."""

    config: MarketConfig
    traders: List[Trader]
    manipulator: Trader | None = None
    sentiment: SentimentCurve = field(default_factory=NoSentiment)
    rng: Random | None = None

    def run(self, n_days: int) -> list[MarketState]:
        rng = self.rng or Random(self.config.seed)
        sentiment = self.sentiment or NoSentiment()

        last_price = self.config.initial_price
        states: list[MarketState] = []

        for day in range(n_days):
            sentiment_value = sentiment.value_at(day)
            buy_orders: list[Order] = []
            sell_orders: list[Order] = []
            owner_lookup: Dict[int, Trader] = {}

            def collect_order(order: Order, owner: Trader) -> None:
                owner_lookup[id(order)] = owner
                if order.side == "buy":
                    buy_orders.append(order)
                else:
                    sell_orders.append(order)

            for trader in self.traders:
                order = trader.maybe_generate_order(
                    last_price=last_price,
                    sentiment_value=sentiment_value,
                    config=self.config,
                )
                if order:
                    collect_order(order, trader)

            if self.manipulator is not None:
                manip_orders = self.manipulator.maybe_generate_order_batch(
                    day=day,
                    last_price=last_price,
                    sentiment_value=sentiment_value,
                    config=self.config,
                    rng=rng,
                )
                for order in manip_orders:
                    collect_order(order, self.manipulator)

            if not buy_orders and not sell_orders:
                state = MarketState(day=day, price=last_price, volume=0.0, sentiment_value=sentiment_value)
                states.append(state)
                continue

            order_curves = build_order_curves(buy_orders, sell_orders, price_tick=self.config.price_tick)
            price, volume = find_equilibrium_price(order_curves)

            executed_volume = volume
            buy_fill_candidates = sorted((order for order in buy_orders if order.price >= price), key=lambda o: o.price, reverse=True)
            sell_fill_candidates = sorted((order for order in sell_orders if order.price <= price), key=lambda o: o.price)

            buy_fills = allocate_fills(buy_fill_candidates, executed_volume)
            sell_fills = allocate_fills(sell_fill_candidates, executed_volume)

            for order, fill_volume in buy_fills + sell_fills:
                owner = owner_lookup.get(id(order))
                if owner is not None and fill_volume > 0:
                    owner.apply_fill(order, price=price, volume=fill_volume)

            state = MarketState(
                day=day,
                price=price,
                volume=volume,
                sentiment_value=sentiment_value,
                order_curves=order_curves,
            )
            states.append(state)
            last_price = price

        return states


__all__ = ["SimulationRunner"]
