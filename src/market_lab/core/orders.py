"""Utilities for representing orders and aggregated curves."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(slots=True)
class Order:
    """Represents a single limit order."""

    trader_id: str
    side: str  # "buy" | "sell"
    price: float
    volume: float

    def __post_init__(self) -> None:
        """
        Valida os parâmetros da ordem após a inicialização.

        Raises:
            ValueError: Se side não for "buy" ou "sell"
            ValueError: Se price for menor ou igual a zero
            ValueError: Se volume for menor ou igual a zero
        """
        if self.side not in {"buy", "sell"}:
            raise ValueError(f"Invalid side '{self.side}'")
        if self.price <= 0:
            raise ValueError("Order price must be positive")
        if self.volume <= 0:
            raise ValueError("Order volume must be positive")


@dataclass(slots=True)
class OrderCurves:
    """Aggregated order book curves along a discrete price grid."""

    price_grid: list[float]
    buy_curve: list[float]
    sell_curve: list[float]

    def satisfaction(self) -> list[float]:
        """
        Calcula o volume executável em cada nível de preço.

        O volume executável em cada preço é o mínimo entre a demanda (buy_curve)
        e a oferta (sell_curve) naquele ponto.

        Returns:
            Lista com volume executável para cada preço no price_grid

        Example:
            >>> curves = OrderCurves([100, 101], [50, 30], [40, 60])
            >>> curves.satisfaction()
            [40, 30]
        """

        return [min(b, s) for b, s in zip(self.buy_curve, self.sell_curve, strict=False)]


def _ensure_price_grid(
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    *,
    price_tick: float,
) -> list[float]:
    """
    Cria uma grade de preços discreta cobrindo todas as ordens.

    Gera uma sequência de preços espaçados por price_tick, do menor preço
    menos um tick até o maior preço mais um tick.

    Args:
        buy_orders: Sequência de ordens de compra
        sell_orders: Sequência de ordens de venda
        price_tick: Incremento mínimo de preço na grade

    Returns:
        Lista de preços uniformemente espaçados cobrindo todas as ordens
    """
    prices: list[float] = [order.price for order in buy_orders] + [order.price for order in sell_orders]
    if not prices:
        return [price_tick]
    min_price = max(min(prices) - price_tick, price_tick)
    max_price = max(prices) + price_tick
    steps = int((max_price - min_price) / price_tick) + 1
    return [min_price + price_tick * idx for idx in range(steps)]


def aggregate_orders(
    *,
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    price_tick: float,
    price_grid: Sequence[float] | None = None,
) -> OrderCurves:
    """
    Converte ordens individuais em curvas agregadas de demanda e oferta.

    Para cada nível de preço na grade, calcula o volume total de compra
    (ordens com preço >= ao nível) e venda (ordens com preço <= ao nível).

    Args:
        buy_orders: Sequência de ordens de compra a serem agregadas
        sell_orders: Sequência de ordens de venda a serem agregadas
        price_tick: Incremento mínimo de preço
        price_grid: Grade de preços opcional; se None, será gerada automaticamente

    Returns:
        OrderCurves com curvas de demanda e oferta agregadas

    Example:
        >>> buy = [Order("t1", "buy", 100, 10), Order("t2", "buy", 101, 5)]
        >>> sell = [Order("t3", "sell", 99, 8)]
        >>> curves = aggregate_orders(buy_orders=buy, sell_orders=sell, price_tick=1.0)
    """

    grid = list(price_grid) if price_grid is not None else _ensure_price_grid(buy_orders, sell_orders, price_tick=price_tick)
    if not grid:
        grid = [price_tick]

    buy_curve: list[float] = []
    sell_curve: list[float] = []

    for price in grid:
        buy_curve.append(sum(order.volume for order in buy_orders if order.price >= price))
        sell_curve.append(sum(order.volume for order in sell_orders if order.price <= price))

    return OrderCurves(price_grid=grid, buy_curve=buy_curve, sell_curve=sell_curve)


def build_order_curves(
    buy_orders: Sequence[Order],
    sell_orders: Sequence[Order],
    *,
    price_tick: float,
) -> OrderCurves:
    """
    Wrapper público para construção de curvas de ordens.

    Função conveniente compatível com o módulo market_lab.core.market para
    criar curvas agregadas a partir de listas de ordens.

    Args:
        buy_orders: Sequência de ordens de compra
        sell_orders: Sequência de ordens de venda
        price_tick: Incremento mínimo de preço na grade

    Returns:
        OrderCurves com curvas de demanda e oferta agregadas
    """

    return aggregate_orders(buy_orders=buy_orders, sell_orders=sell_orders, price_tick=price_tick)


def allocate_fills(orders: Iterable[Order], volume: float) -> list[tuple[Order, float]]:
    """
    Distribui volume executado entre as ordens na sequência de chegada.

    Aloca o volume disponível às ordens seguindo a ordem FIFO (first-in-first-out),
    executando parcialmente a última ordem se necessário.

    Args:
        orders: Ordens elegíveis para execução, em ordem de prioridade
        volume: Volume total disponível para execução

    Returns:
        Lista de tuplas (ordem, volume_executado) para cada ordem preenchida

    Example:
        >>> orders = [Order("t1", "buy", 100, 10), Order("t2", "buy", 100, 5)]
        >>> fills = allocate_fills(orders, 12.0)
        >>> [(o.trader_id, v) for o, v in fills]
        [('t1', 10.0), ('t2', 2.0)]
    """

    remaining = max(volume, 0.0)
    fills: list[tuple[Order, float]] = []
    for order in orders:
        if remaining <= 0:
            break
        fill_volume = min(order.volume, remaining)
        if fill_volume > 0:
            fills.append((order, fill_volume))
            remaining -= fill_volume
    return fills
