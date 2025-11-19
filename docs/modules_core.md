# Módulos Core

Este documento detalha o desenho dos módulos em `src/market_lab/core`.

---

## 1. `market.py`

### Objetivo

Definir:

- configurações do mercado,
- estado do mercado,
- funções de cálculo de curvas e preço.

### Estruturas sugeridas

```python
@dataclass
class MarketConfig:
    n_traders: int
    initial_price: float
    price_volatility: float
    wealth_mode: str  # "unlimited" | "limited"
    sentiment_mode: str  # "none" | "external_curve"
    max_daily_volume: float
    seed: int | None = None
```

```python
@dataclass
class MarketState:
    day: int
    price: float
    volume: float
    sentiment_value: float | None
    # Outros campos, se necessário:
    # order_curve_buy, order_curve_sell, manipulation_score, etc.
```

### Funções principais

* `build_order_curves(buy_orders, sell_orders) -> OrderCurves`

  * a partir de listas de `Order`, monta curvas agregadas discretizadas.

* `find_equilibrium_price(order_curves) -> tuple[float, float]`

  * aplica a lógica de auction pricing,
  * retorna `(price, volume)`.

---

## 2. `traders.py`

### Objetivo

Modelar os diferentes tipos de traders.

### Classe base

```python
class Trader:
    def __init__(self, trader_id: int, wealth: float, holdings: float):
        self.trader_id = trader_id
        self.wealth = wealth
        self.holdings = holdings

    def maybe_generate_order(self, market_state: MarketState, config: MarketConfig) -> Order | None:
        """Decide se vai gerar uma ordem e qual."""
        raise NotImplementedError
```

### `RandomTrader`

* Não considera riqueza (modo ilimitado).
* Preço de ordem:

  * `N(price_{t-1}, sigma)` ou ajustado por sentimento.
* Volume:

  * uniforme em `[0, max_daily_volume]`.
* Decide compra/venda com probabilidade 50/50 (pode ser ajustável).

### `WealthLimitedTrader`

* Usa a mesma lógica de sorteio de preço.
* Volume máximo limitado por:

  * compra: `wealth / price_max`,
  * venda: `holdings`.

---

## 3. `orders.py`

### Objetivo

Representar ordens e curvas agregadas.

### Estruturas

```python
@dataclass
class Order:
    trader_id: int
    side: str  # "buy" | "sell"
    price: float
    volume: float
```

```python
@dataclass
class OrderCurves:
    price_grid: np.ndarray
    buy_curve: np.ndarray  # volume acumulado de demanda
    sell_curve: np.ndarray # volume acumulado de oferta
```

### Funções principais

* `aggregate_orders(orders, price_grid) -> OrderCurves`

  * converte lista de ordens em curvas discretizadas.

---

## 4. `sentiment.py`

### Objetivo

Modelar eventos de notícia/sentimento.

### Exemplo de interface

```python
class SentimentCurve:
    def __init__(self, mode: str):
        self.mode = mode

    def value_at(self, day: int) -> float:
        """Retorna um valor de sentimento (ex.: deslocamento em relação ao preço)."""
        ...
```

Implementações possíveis:

* `NoSentiment` – sempre 0.
* `StepSentiment` – a partir de certo dia, adiciona um deslocamento constante.
* `PulseSentiment` – pulso de notícia em poucos dias.

---

## 5. `simulation.py`

### Objetivo

Orquestrar o loop de simulação, juntando traders, manipulador (opcional) e mercado.

### Estrutura sugerida

```python
class SimulationRunner:
    def __init__(self, config: MarketConfig, traders: list[Trader], manipulator: Manipulator | None, sentiment: SentimentCurve):
        ...

    def run(self, n_days: int) -> list[MarketState]:
        """Executa a simulação e retorna a lista de estados diários."""
        ...
```

Responsabilidades:

* Laço principal de `n_days`.
* Coleta de ordens:

  * chama `maybe_generate_order` de todos os traders,
  * chama métodos do `Manipulator` se existir.
* Construção de curvas:

  * usa `orders.aggregate_orders`.
* Cálculo de preço e volume:

  * usa `market.find_equilibrium_price`.
* Atualização de:

  * traders,
  * manipulador,
  * estado do mercado.
