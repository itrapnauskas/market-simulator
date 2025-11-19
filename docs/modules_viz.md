# Módulos de Visualização

Este documento detalha `src/market_lab/viz`.

---

## 1. `plots.py`

### Objetivo

Fornecer funções simples para visualizar:

- preço ao longo do tempo,
- volume ao longo do tempo,
- riqueza do manipulador vs outros,
- score de manipulação,
- curvas de ordens em um dia.

### Funções sugeridas

```python
def plot_price_series(states: list[MarketState]):
    """Plota preço ao longo do tempo."""


def plot_volume_series(states: list[MarketState]):
    """Plota volume ao longo do tempo."""


def plot_manipulator_wealth(manip_wealth: np.ndarray, others_wealth: np.ndarray):
    """Plota riqueza do manipulador vs média dos outros."""


def plot_order_curves(order_curves: OrderCurves, title: str = ""):
    """Plota curva de demanda e oferta para um dia específico."""


def plot_manipulation_score(scores: np.ndarray):
    """Plota um score de manipulação por dia."""
```

As implementações podem usar:

* `matplotlib` (mais simples),
* ou `plotly` (interativo).

---

## 2. `animation.py`

### Objetivo

Criar animações opcionais, por exemplo:

* evolução diária da curva de ordens,
* evolução do preço com marcadores de dias com manipulação.

Pode usar:

* `matplotlib.animation.FuncAnimation`,
* salvar como `.mp4` ou `.gif`.

Funções sugeridas:

```python
def animate_price_and_volume(states: list[MarketState], filepath: str):
    """Gera animação da série de preço e volume."""


def animate_order_curves_over_time(order_curves_sequence: list[OrderCurves], filepath: str):
    """Anima a evolução das curvas de ordens."""
```
