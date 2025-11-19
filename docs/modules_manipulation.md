# Módulos de Manipulação

Este documento detalha `src/market_lab/manipulation`.

---

## 1. `manipulator.py`

### Objetivo

Implementar um agente especial que:

- possui mais capital que os demais,
- pode coordenar ordens de compra/venda,
- tenta empurrar o preço em determinada direção.

### Estrutura sugerida

```python
class Manipulator:
    def __init__(self, wealth: float, holdings: float, strategy: str, params: dict):
        self.wealth = wealth
        self.holdings = holdings
        self.strategy = strategy
        self.params = params
        self.phase = "accumulate"  # "accumulate" | "pump" | "dump"
```

Métodos:

* `generate_orders(market_state, config) -> list[Order]`

  * Decide, com base na `phase`, quais ordens gerar:

    * **accumulate**:

      * compras gradativas abaixo/próximo do preço;
    * **pump**:

      * self-trading (comprar e vender ao mesmo preço) para inflar volume e puxar preço;
    * **dump**:

      * vender grandes volumes próximos ao topo.

* `update_phase(market_state, day)`

  * Lógica para transitar entre fases:

    * por tempo,
    * por lucro alvo,
    * por nível de preço.

---

## 2. `detection.py`

### Objetivo

Definir funções que, dado um estado diário ou série de estados, produzem **indicadores de manipulação**.

Exemplos de funções:

```python
def compute_order_curve_deviation(order_curves: OrderCurves, reference_band: ReferenceBand) -> float:
    """Retorna um score numérico de quão fora do padrão estão as curvas."""
```

```python
def compute_price_volume_anomaly(price_series, volume_series) -> np.ndarray:
    """Retorna um array de scores diários."""
```

---

## 3. `metrics.py`

### Objetivo

Implementar métricas atômicas e reusáveis.

Exemplos:

* `kl_divergence(curve, reference_curve)`
* `max_deviation(curve, upper_band, lower_band)`
* `count_sharp_dents(curve)` – detectar “dentes” estranhos nas curvas

Essas funções podem ser combinadas em `detection.py` para produzir métricas mais compostas.

---

## Referências conceituais

* Manipulação baseada em ordens (trade-based manipulation).
* Self-trading e wash trading.
* Pump-and-dump.
* Uso de séries de preço e volume para detecção de outliers em mercados reais.
