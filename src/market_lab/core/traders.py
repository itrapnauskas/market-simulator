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
        """
        Gera uma ordem de compra ou venda baseada no estado do mercado.

        Args:
            last_price: Último preço de fechamento do mercado
            sentiment_value: Valor de sentimento atual do mercado
            config: Configuração do mercado contendo parâmetros de simulação

        Returns:
            Uma ordem de compra/venda ou None se o trader não negociar neste dia
        """
        raise NotImplementedError

    def apply_fill(self, order: Order, *, price: float, volume: float) -> None:
        """
        Atualiza o estado interno do trader após a execução de uma ordem.

        Args:
            order: A ordem que foi executada
            price: Preço de execução da ordem
            volume: Volume executado da ordem
        """

    def _draw_price(self, *, last_price: float, sentiment_value: float, config: MarketConfig) -> float:
        """
        Sorteia um preço para a ordem usando distribuição gaussiana.

        O preço é centrado no último preço de mercado ajustado pelo sentimento,
        com volatilidade definida pela configuração.

        Args:
            last_price: Último preço de fechamento do mercado
            sentiment_value: Ajuste de sentimento a ser aplicado ao preço
            config: Configuração contendo volatilidade e tick mínimo

        Returns:
            Preço sorteado, garantido ser no mínimo igual ao price_tick
        """
        center = max(last_price + sentiment_value, config.price_tick)
        price = self.rng.gauss(center, config.price_volatility)
        return max(price, config.price_tick)

    def _draw_volume(self, config: MarketConfig) -> float:
        """
        Sorteia um volume aleatório para a ordem.

        Args:
            config: Configuração contendo o volume máximo diário permitido

        Returns:
            Volume sorteado entre 0.1 e max_daily_volume
        """
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
        """
        Gera uma ordem aleatória de compra ou venda sem restrições de capital.

        O trader tem uma probabilidade (active_probability) de negociar em cada dia.
        Quando ativo, escolhe aleatoriamente entre compra e venda com 50% de chance.

        Args:
            last_price: Último preço de fechamento do mercado
            sentiment_value: Valor de sentimento atual do mercado
            config: Configuração do mercado contendo parâmetros de simulação

        Returns:
            Uma ordem de compra/venda ou None se o trader estiver inativo
        """
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
        """
        Gera uma ordem respeitando limites de capital e posição.

        Este trader estende RandomTrader mas verifica se tem capital suficiente
        para compras ou holdings suficientes para vendas antes de submeter a ordem.

        Args:
            last_price: Último preço de fechamento do mercado
            sentiment_value: Valor de sentimento atual do mercado
            config: Configuração do mercado contendo parâmetros de simulação

        Returns:
            Uma ordem ajustada aos limites de capital/posição ou None se não houver
            capital/holdings suficientes
        """
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
        """
        Atualiza capital e posição do trader após execução de ordem.

        Para ordens de compra, deduz o custo do capital e aumenta os holdings.
        Para ordens de venda, adiciona o valor ao capital e reduz os holdings.

        Args:
            order: A ordem que foi executada
            price: Preço de execução da ordem
            volume: Volume executado da ordem
        """
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
    """
    Cria uma população de traders baseada na configuração do mercado.

    Factory que gera n_traders conforme especificado em config. Se wealth_mode
    for "limited", cria WealthLimitedTraders com capital e holdings aleatórios.
    Caso contrário, cria RandomTraders sem restrições.

    Args:
        config: Configuração do mercado especificando número e tipo de traders
        rng: Gerador de números aleatórios para criar seeds individuais

    Returns:
        Lista de traders prontos para participar da simulação

    Example:
        >>> config = MarketConfig(n_traders=100, wealth_mode="limited", ...)
        >>> traders = build_traders(config, Random(42))
        >>> len(traders)
        100
    """

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
