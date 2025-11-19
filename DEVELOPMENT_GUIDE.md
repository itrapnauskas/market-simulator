# 💻 DEVELOPMENT GUIDE - Market Manipulation Lab

Guia completo para desenvolver, estender e contribuir com o projeto.

---

## 🎯 QUICK START PARA DESENVOLVEDORES

```bash
# 1. Clone e entre no diretório
cd /home/user/market-simulator

# 2. Instale em modo desenvolvimento
pip install -e ".[dev,viz,ml]"

# 3. Rode testes para validar
pytest tests/ -v

# 4. Configure git hooks (opcional)
pre-commit install

# 5. Pronto! Comece a desenvolver
```

---

## 📁 ESTRUTURA DO CÓDIGO

```
src/market_lab/
├── core/                    # ⚙️ NÚCLEO DO SIMULADOR
│   ├── market.py           # MarketConfig, MarketState, auction pricing
│   ├── traders.py          # RandomTrader, WealthLimitedTrader
│   ├── orders.py           # Order, OrderCurves, aggregation
│   ├── sentiment.py        # SentimentCurve, NoSentiment, etc
│   └── simulation.py       # SimulationRunner (loop principal)
│
├── manipulation/            # 🎭 ESTRATÉGIAS E DETECÇÃO
│   ├── manipulator.py      # Pump-and-dump (base class)
│   ├── spoofing.py         # Spoofing/layering
│   ├── wash_trading.py     # Self-trading
│   ├── layering.py         # Quote stuffing
│   ├── detection.py        # Detectores básicos
│   ├── advanced_detection.py # ML e estatísticas avançadas
│   └── metrics.py          # Métricas auxiliares
│
├── viz/                     # 📊 VISUALIZAÇÃO
│   ├── plots.py            # Gráficos matplotlib
│   └── animation.py        # Animações
│
├── agents/                  # 🤖 SISTEMA DE AGENTES IA
│   ├── core.py             # Agent, Message, CommunicationBus
│   ├── specialists.py      # 13 agentes especializados
│   ├── organization.py     # Orquestração
│   └── actions.py          # Ações concretas
│
└── experiments/             # 🔬 EXPERIMENTOS PRONTOS
    └── random_walk.py      # Experimento baseline
```

---

## 🛠️ FERRAMENTAS DE DESENVOLVIMENTO

### Makefile Commands

```bash
# Setup
make dev-setup          # Instala deps + pre-commit

# Qualidade
make format             # Formata código com ruff
make lint               # Verifica qualidade (ruff check)
make type-check         # Type checking com mypy
make test               # Roda pytest
make test-cov           # Testes com coverage
make ci                 # Roda CI completa localmente

# Docker
make docker-build       # Build todas as images
make docker-jupyter     # Jupyter em container
make docker-dashboard   # Dashboard em container

# Limpeza
make clean              # Remove artifacts
make clean-all          # Remove tudo (incluindo .venv)

# Ajuda
make help               # Lista todos os comandos
```

---

## 🧪 TESTES

### Estrutura de Testes

```
tests/
├── conftest.py                  # Fixtures compartilhadas
├── test_core/
│   ├── test_market.py          # Testes de auction pricing
│   ├── test_traders.py         # Testes de traders
│   ├── test_orders.py          # Testes de ordens
│   └── test_simulation.py      # Testes de integração
└── test_manipulation/
    ├── test_manipulator.py     # Pump-and-dump
    ├── test_spoofing.py        # (TODO)
    └── test_advanced_detection.py
```

### Como Rodar Testes

```bash
# Todos os testes
pytest tests/

# Com verbosidade
pytest tests/ -v

# Com coverage
pytest tests/ --cov=market_lab --cov-report=html

# Teste específico
pytest tests/test_core/test_market.py::test_equilibrium_price

# Com output
pytest tests/ -s

# Parallel (mais rápido)
pytest tests/ -n auto
```

### Escrevendo Testes

**Template:**
```python
"""Tests for new feature."""

import pytest
from market_lab.core.market import MarketConfig


def test_basic_functionality():
    """Test basic functionality works."""
    config = MarketConfig(n_traders=10)
    assert config.n_traders == 10


def test_edge_case():
    """Test edge case with zero traders."""
    with pytest.raises(ValueError):
        MarketConfig(n_traders=0)


@pytest.fixture
def sample_data(rng):
    """Fixture for sample data."""
    return [1, 2, 3, 4, 5]


def test_with_fixture(sample_data):
    """Test using fixture."""
    assert len(sample_data) == 5
```

**Boas Práticas:**
- Um teste por comportamento
- Nome descritivo (test_what_when_then)
- Use fixtures para setup complexo
- Mock quando necessário
- Teste edge cases!

---

## 📝 STYLE GUIDE

### Code Style

**Configurado via ruff + mypy:**

```python
# ✅ BOM
def calculate_price(
    buy_volume: float,
    sell_volume: float,
    price_grid: list[float]
) -> float:
    """
    Calculate equilibrium price.

    Args:
        buy_volume: Total buy volume
        sell_volume: Total sell volume
        price_grid: Price points to evaluate

    Returns:
        Equilibrium price
    """
    if buy_volume <= 0:
        return price_grid[0]

    # ... implementation
    return equilibrium


# ❌ RUIM
def calc(b,s,p):  # Sem type hints, sem docstring
    if b<=0:return p[0]  # Sem espaços, inline
    return e  # Nome não descritivo
```

### Docstrings

**Formato:**
```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    Short description (one line).

    Longer description if needed, explaining what the function does,
    why it exists, and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is negative

    Example:
        >>> function_name(10, 20)
        30
    """
```

### Type Hints

**Sempre use type hints:**
```python
from typing import Sequence, Optional

# ✅ BOM
def process_states(
    states: Sequence[MarketState],
    window: int = 10
) -> list[float]:
    ...

# ❌ RUIM
def process_states(states, window=10):
    ...
```

---

## 🎨 CRIANDO NOVA ESTRATÉGIA DE MANIPULAÇÃO

### Passo 1: Criar Arquivo

```bash
touch src/market_lab/manipulation/my_strategy.py
```

### Passo 2: Implementar Classe

```python
"""My custom manipulation strategy."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Optional

from market_lab.core.market import MarketConfig
from market_lab.core.orders import Order
from market_lab.core.traders import WealthLimitedTrader


@dataclass
class MyStrategyManipulator(WealthLimitedTrader):
    """
    My custom manipulation strategy.

    Brief description of what this strategy does and how it works.

    Attributes:
        param1: Description of parameter 1
        param2: Description of parameter 2
    """

    # Custom parameters
    param1: float = 1.5
    param2: int = 10

    def maybe_generate_order(
        self,
        last_price: float,
        sentiment_value: float,
        config: MarketConfig
    ) -> Optional[Order]:
        """
        Generate order based on strategy logic.

        Args:
            last_price: Current market price
            sentiment_value: Market sentiment (-1 to 1)
            config: Market configuration

        Returns:
            Order if strategy decides to trade, None otherwise
        """
        # Your logic here
        if self._should_trade():
            return self._create_order(last_price, config)
        return None

    def _should_trade(self) -> bool:
        """Check if should trade this turn."""
        # Implementation
        return True

    def _create_order(
        self,
        price: float,
        config: MarketConfig
    ) -> Order:
        """Create order with strategy-specific logic."""
        # Implementation
        return Order(
            trader_id=self.trader_id,
            side="buy",
            price=price,
            volume=10.0
        )
```

### Passo 3: Adicionar Export

```python
# src/market_lab/manipulation/__init__.py

from .my_strategy import MyStrategyManipulator

__all__ = [
    # ... existing exports
    "MyStrategyManipulator",
]
```

### Passo 4: Criar Testes

```python
# tests/test_manipulation/test_my_strategy.py

"""Tests for my custom strategy."""

import pytest
from random import Random
from market_lab.core.market import MarketConfig
from market_lab.manipulation.my_strategy import MyStrategyManipulator


@pytest.fixture
def manipulator():
    """Create test manipulator."""
    return MyStrategyManipulator(
        trader_id="test_manip",
        rng=Random(42),
        wealth=10000.0,
        holdings=100.0,
        param1=2.0,
        param2=20
    )


def test_creation(manipulator):
    """Test manipulator is created correctly."""
    assert manipulator.trader_id == "test_manip"
    assert manipulator.param1 == 2.0
    assert manipulator.param2 == 20


def test_generates_order(manipulator):
    """Test order generation."""
    config = MarketConfig()
    order = manipulator.maybe_generate_order(100.0, 0.0, config)

    assert order is not None
    assert order.trader_id == "test_manip"
    # Add more assertions
```

### Passo 5: Criar Exemplo

```python
# examples/my_strategy_demo.py

"""Demo of my custom strategy."""

from random import Random
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
from market_lab.core.simulation import SimulationRunner
from market_lab.core.sentiment import NoSentiment
from market_lab.manipulation.my_strategy import MyStrategyManipulator


def main():
    """Run my strategy demo."""
    # Setup
    config = MarketConfig(n_traders=100)
    rng = Random(42)
    traders = build_traders(config, rng)

    # Create manipulator
    manipulator = MyStrategyManipulator(
        trader_id="my_manip",
        rng=rng,
        wealth=50000.0,
        holdings=100.0,
        param1=2.5,
        param2=15
    )

    # Run simulation
    runner = SimulationRunner(
        config=config,
        traders=traders,
        sentiment=NoSentiment(),
        manipulator=manipulator
    )

    states = runner.run(n_days=120)

    print(f"Ran {len(states)} days")
    print(f"Final price: ${states[-1].price:.2f}")


if __name__ == "__main__":
    main()
```

---

## 🔍 CRIANDO NOVO DETECTOR

Similar ao processo de estratégia, mas em `advanced_detection.py`:

```python
def my_custom_detector(
    states: Sequence[MarketState],
    window: int = 20
) -> DetectionResult:
    """
    My custom detection algorithm.

    Brief description of detection methodology.

    Args:
        states: Market states to analyze
        window: Rolling window size

    Returns:
        DetectionResult with scores and metadata
    """
    scores = []

    for i in range(len(states)):
        # Your detection logic
        score = _calculate_score(states[i])
        scores.append(score)

    return DetectionResult(
        scores=scores,
        confidence=0.85,
        method="my_custom",
        metadata={"window": window}
    )
```

---

## 📊 CRIANDO NOVO NOTEBOOK

```bash
# Criar arquivo
jupyter notebook notebooks/05_my_topic.ipynb
```

**Template:**

```markdown
# Notebook 5: My Topic

Brief description of what this notebook teaches.

## Learning Objectives

1. Understand X
2. Learn Y
3. Implement Z

## Setup
```

```python
# Imports
import random
from market_lab.core import *
import matplotlib.pyplot as plt
%matplotlib inline
```

```markdown
## Section 1: Theory

Explain concept with text, math, diagrams.

## Section 2: Implementation

Show code with explanations.
```

```python
# Code cell
config = MarketConfig(...)
# ...
```

```markdown
## Section 3: Exercises

1. Exercise 1: Do X
2. Exercise 2: Do Y

## Conclusion

Summary of what was learned.
```

---

## 🐳 DOCKER DEVELOPMENT

```bash
# Build dev image
docker build --target development -t market-lab:dev .

# Run com volume mount
docker run -it -v $(pwd):/app market-lab:dev bash

# Dentro do container
pytest tests/
```

---

## 🔄 CI/CD

### GitHub Actions

Workflows em `.github/workflows/`:

- **ci.yml** - Testes em cada PR
- **release.yml** - Publica no PyPI
- **docs.yml** - Build documentação

### Pre-commit Hooks

```bash
# Instalar
pre-commit install

# Rodar manualmente
pre-commit run --all-files
```

---

## 📦 CRIANDO RELEASE

```bash
# 1. Bump version em pyproject.toml
vim pyproject.toml  # version = "0.3.0"

# 2. Update CHANGELOG
vim CHANGELOG.md

# 3. Commit
git add .
git commit -m "chore: bump to v0.3.0"
git push

# 4. Tag
git tag v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0

# GitHub Actions faz o resto!
```

---

## 🤝 CONTRIBUINDO

### Flow de Trabalho

```bash
# 1. Fork no GitHub

# 2. Clone seu fork
git clone https://github.com/SEU-USER/market-simulator

# 3. Crie branch
git checkout -b feature/my-feature

# 4. Desenvolva
# ... faça mudanças

# 5. Teste
make test
make lint

# 6. Commit
git add .
git commit -m "feat: add my feature"

# 7. Push
git push origin feature/my-feature

# 8. Abra PR no GitHub
```

### Checklist de PR

- [ ] Testes passando (pytest)
- [ ] Lint passando (ruff)
- [ ] Type check passando (mypy)
- [ ] Docstrings adicionadas
- [ ] Testes para novo código
- [ ] CHANGELOG atualizado
- [ ] Exemplos criados (se aplicável)

---

## 🐛 DEBUGGING

### Pytest com PDB

```bash
# Break on failure
pytest --pdb

# Break on first failure
pytest -x --pdb
```

### Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug info")
logger.info("Info message")
```

### VS Code

```json
// .vscode/launch.json
{
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"]
        }
    ]
}
```

---

## 📚 RECURSOS

### Documentação
- `docs/architecture.md` - Arquitetura detalhada
- `GUIDES/` - Guias especializados
- Type hints - Use mypy para validar

### Exemplos
- `examples/` - Scripts de exemplo
- `tests/` - Exemplos de uso nas fixtures

### Comunidade
- GitHub Issues - Bugs e features
- GitHub Discussions - Perguntas

---

## ✅ CHECKLIST DO DESENVOLVEDOR

### Antes de Começar
- [ ] Fork do repositório
- [ ] pip install -e ".[dev,viz,ml]"
- [ ] pytest tests/ passa
- [ ] make lint passa

### Ao Desenvolver
- [ ] Testes criados
- [ ] Docstrings escritas
- [ ] Type hints adicionadas
- [ ] Exemplo criado (se aplicável)

### Antes do PR
- [ ] make ci passa
- [ ] CHANGELOG atualizado
- [ ] Branch atualizada com main
- [ ] Descrição de PR clara

---

**Happy Coding! 🚀**
