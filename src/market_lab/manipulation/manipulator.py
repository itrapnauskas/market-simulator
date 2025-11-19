"""Implementation of a simple pump-and-dump manipulator."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List

from ..core.market import MarketConfig
from ..core.orders import Order
from ..core.traders import WealthLimitedTrader


@dataclass
class Manipulator(WealthLimitedTrader):
    """Wealthy agent capable of coordinating orders across phases."""

    accumulation_days: int = 30
    pump_days: int = 10
    dump_days: int = 15

    def current_phase(self, day: int) -> str:
        """
        Determina a fase atual da estratégia pump-and-dump.

        A estratégia possui três fases sequenciais:
        - accumulate: acumula posição comprando abaixo do preço
        - pump: infla artificialmente o preço com ordens coordenadas
        - dump: vende toda a posição rapidamente

        Args:
            day: Número do dia da simulação

        Returns:
            String indicando a fase: "accumulate", "pump" ou "dump"

        Example:
            >>> manip = Manipulator("m1", rng, accumulation_days=30, pump_days=10)
            >>> manip.current_phase(15)
            'accumulate'
            >>> manip.current_phase(35)
            'pump'
            >>> manip.current_phase(45)
            'dump'
        """
        if day < self.accumulation_days:
            return "accumulate"
        if day < self.accumulation_days + self.pump_days:
            return "pump"
        return "dump"

    def maybe_generate_order_batch(
        self,
        *,
        day: int,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig,
        rng: Random,
    ) -> List[Order]:
        """
        Gera um conjunto de ordens coordenadas baseadas na fase de manipulação.

        Implementa a estratégia pump-and-dump:
        - Fase accumulate: compra gradual abaixo do preço de mercado (0.98x)
        - Fase pump: ordens simultâneas de compra/venda para criar movimento
          artificial de preço (compra a 1.02x, vende a 1.021x)
        - Fase dump: vende rapidamente toda a posição (0.99x)

        Args:
            day: Número do dia da simulação
            last_price: Último preço de fechamento do mercado
            sentiment_value: Valor de sentimento atual (ignorado na manipulação)
            config: Configuração do mercado
            rng: Gerador de números aleatórios (não usado atualmente)

        Returns:
            Lista de ordens a serem submetidas, pode estar vazia se não houver
            capital/holdings suficientes

        Example:
            >>> manip = Manipulator("m1", rng, wealth=100000, holdings=0)
            >>> orders = manip.maybe_generate_order_batch(day=5, last_price=100, ...)
            >>> orders[0].side
            'buy'
            >>> orders[0].price < 100
            True
        """
        phase = self.current_phase(day)
        orders: list[Order] = []
        if phase == "accumulate":
            base_order = super().maybe_generate_order(
                last_price=last_price * 0.98,
                sentiment_value=sentiment_value,
                config=config,
            )
            if base_order:
                orders.append(base_order)
        elif phase == "pump":
            price = max(last_price * 1.02, config.price_tick)
            volume = min(self.wealth / max(price, config.price_tick), config.max_daily_volume * 2)
            volume = max(volume, 0.0)
            if volume > 0:
                buy = Order(trader_id=f"{self.trader_id}_pump_buy", side="buy", price=price, volume=volume)
                sell = Order(trader_id=f"{self.trader_id}_pump_sell", side="sell", price=price * 1.001, volume=volume)
                orders.extend([buy, sell])
        else:  # dump phase
            price = max(last_price * 0.99, config.price_tick)
            volume = min(self.holdings, config.max_daily_volume * 3)
            if volume > 0:
                orders.append(Order(trader_id=f"{self.trader_id}_dump", side="sell", price=price, volume=volume))
        return orders


__all__ = ["Manipulator"]
