"""
Actions - Ações concretas que os agentes podem executar no projeto.

Este módulo permite que os agentes realmente implementem melhorias,
criando arquivos, configurações e código.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)


class AgentActions:
    """
    Ações concretas que agentes podem executar no projeto.

    Cada método aqui representa uma ação tangível que melhora o codebase.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src" / "market_lab"
        self.tests_dir = project_root / "tests"
        self.docs_dir = project_root / "docs"
        self.notebooks_dir = project_root / "notebooks"

    def create_test_structure(self) -> dict[str, Any]:
        """
        QA Engineer: Cria estrutura de testes com pytest.

        Returns:
            Resultado da ação
        """
        logger.info("Creating test structure...")

        # Criar diretório de testes
        self.tests_dir.mkdir(exist_ok=True)

        # Criar __init__.py
        (self.tests_dir / "__init__.py").write_text(
            '"""Test suite for Market Manipulation Lab."""\n'
        )

        # Criar conftest.py com fixtures
        conftest_content = '''"""
Pytest configuration and shared fixtures.
"""

import pytest
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
import random


@pytest.fixture
def rng():
    """Provides a seeded random number generator for reproducible tests."""
    return random.Random(42)


@pytest.fixture
def basic_config():
    """Provides a basic market configuration for tests."""
    return MarketConfig(
        n_traders=10,
        initial_price=100.0,
        initial_cash=10000.0,
        initial_holdings=100,
        min_price=50.0,
        max_price=200.0,
        n_price_points=50
    )


@pytest.fixture
def traders(basic_config, rng):
    """Provides a list of traders for tests."""
    return build_traders(basic_config, rng)
'''

        (self.tests_dir / "conftest.py").write_text(conftest_content)

        # Criar estrutura de diretórios para testes
        test_dirs = ["test_core", "test_manipulation", "test_viz"]
        for test_dir in test_dirs:
            dir_path = self.tests_dir / test_dir
            dir_path.mkdir(exist_ok=True)
            (dir_path / "__init__.py").write_text("")

        # Criar exemplo de teste para core/orders.py
        test_orders_content = '''"""
Tests for core.orders module.
"""

import pytest
from market_lab.core.orders import Order, aggregate_orders, allocate_fills


def test_order_creation():
    """Test that orders are created correctly."""
    order = Order(
        trader_id=1,
        is_buy=True,
        price_limit=100.0,
        volume=10
    )

    assert order.trader_id == 1
    assert order.is_buy is True
    assert order.price_limit == 100.0
    assert order.volume == 10


def test_order_validation():
    """Test that invalid orders raise ValueError."""
    with pytest.raises(ValueError, match="volume must be positive"):
        Order(trader_id=1, is_buy=True, price_limit=100.0, volume=0)

    with pytest.raises(ValueError, match="price_limit must be positive"):
        Order(trader_id=1, is_buy=True, price_limit=-10.0, volume=10)


def test_aggregate_orders_empty():
    """Test aggregation with no orders."""
    curves = aggregate_orders([], n_price_points=10, min_price=50, max_price=150)

    assert len(curves.price_grid) == 10
    assert all(v == 0 for v in curves.buy_volume)
    assert all(v == 0 for v in curves.sell_volume)


def test_aggregate_orders_single_buy():
    """Test aggregation with single buy order."""
    orders = [Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10)]
    curves = aggregate_orders(orders, n_price_points=10, min_price=50, max_price=150)

    # Buy volume should be non-zero at prices <= 100
    assert any(v > 0 for v in curves.buy_volume)


def test_allocate_fills_no_volume():
    """Test allocation when no volume is cleared."""
    orders = [Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10)]
    fills = allocate_fills(orders, cleared_volume=0.0, is_buy=True)

    assert all(f == 0.0 for f in fills)


def test_allocate_fills_partial():
    """Test partial fills are distributed proportionally."""
    orders = [
        Order(trader_id=1, is_buy=True, price_limit=100.0, volume=10),
        Order(trader_id=2, is_buy=True, price_limit=100.0, volume=20),
    ]
    fills = allocate_fills(orders, cleared_volume=15.0, is_buy=True)

    # Should fill proportionally: 5 and 10
    assert abs(fills[0] - 5.0) < 0.01
    assert abs(fills[1] - 10.0) < 0.01
'''

        (self.tests_dir / "test_core" / "test_orders.py").write_text(test_orders_content)

        logger.info("Test structure created successfully")

        return {
            "status": "completed",
            "tests_created": 6,
            "test_dirs": test_dirs,
            "fixtures_added": 3
        }

    def create_github_actions_ci(self) -> dict[str, Any]:
        """
        DevOps Engineer: Cria workflow de CI/CD com GitHub Actions.

        Returns:
            Resultado da ação
        """
        logger.info("Creating GitHub Actions CI workflow...")

        # Criar diretório .github/workflows
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Criar workflow de CI
        ci_workflow = '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev,viz]"

    - name: Lint with ruff
      run: |
        ruff check src/

    - name: Type check with mypy
      run: |
        mypy src/market_lab/

    - name: Test with pytest
      run: |
        pytest tests/ --cov=market_lab --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
'''

        (workflows_dir / "ci.yml").write_text(ci_workflow)

        logger.info("GitHub Actions CI workflow created")

        return {
            "status": "completed",
            "workflows_created": ["ci.yml"],
            "ci_checks": ["lint", "type-check", "test", "coverage"]
        }

    def create_dev_dependencies(self) -> dict[str, Any]:
        """
        DevOps Engineer: Adiciona dependências de desenvolvimento ao pyproject.toml.

        Returns:
            Resultado da ação
        """
        logger.info("Adding dev dependencies to pyproject.toml...")

        pyproject_path = self.project_root / "pyproject.toml"
        current_content = pyproject_path.read_text()

        # Adicionar dependências de dev se ainda não existirem
        if "[project.optional-dependencies]" in current_content and '"dev"' not in current_content:
            # Encontrar a seção e adicionar dev
            lines = current_content.split("\n")
            new_lines = []
            in_optional_deps = False

            for line in lines:
                new_lines.append(line)
                if line.strip() == "[project.optional-dependencies]":
                    in_optional_deps = True
                elif in_optional_deps and line.startswith("viz = "):
                    # Adicionar dev logo após viz
                    new_lines.append('dev = [')
                    new_lines.append('    "pytest>=7.4",')
                    new_lines.append('    "pytest-cov>=4.1",')
                    new_lines.append('    "ruff>=0.1.0",')
                    new_lines.append('    "mypy>=1.7",')
                    new_lines.append(']')
                    in_optional_deps = False

            pyproject_path.write_text("\n".join(new_lines))

            logger.info("Dev dependencies added to pyproject.toml")

            return {
                "status": "completed",
                "dependencies_added": ["pytest", "pytest-cov", "ruff", "mypy"]
            }

        return {"status": "skipped", "reason": "Dependencies already exist or structure unexpected"}

    def create_ruff_config(self) -> dict[str, Any]:
        """
        CTO: Cria configuração do ruff para linting.

        Returns:
            Resultado da ação
        """
        logger.info("Creating ruff configuration...")

        pyproject_path = self.project_root / "pyproject.toml"
        current_content = pyproject_path.read_text()

        ruff_config = '''

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
    "UP", # pyupgrade
]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["market_lab"]
'''

        if "[tool.ruff]" not in current_content:
            current_content += ruff_config
            pyproject_path.write_text(current_content)

            logger.info("Ruff configuration added")

            return {
                "status": "completed",
                "config_added": "ruff"
            }

        return {"status": "skipped", "reason": "Ruff config already exists"}

    def create_mypy_config(self) -> dict[str, Any]:
        """
        CTO: Cria configuração do mypy para type checking.

        Returns:
            Resultado da ação
        """
        logger.info("Creating mypy configuration...")

        pyproject_path = self.project_root / "pyproject.toml"
        current_content = pyproject_path.read_text()

        mypy_config = '''

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
'''

        if "[tool.mypy]" not in current_content:
            current_content += mypy_config
            pyproject_path.write_text(current_content)

            logger.info("Mypy configuration added")

            return {
                "status": "completed",
                "config_added": "mypy"
            }

        return {"status": "skipped", "reason": "Mypy config already exists"}

    def create_notebooks_structure(self) -> dict[str, Any]:
        """
        Documentation Writer + Frontend Dev: Cria estrutura para notebooks Jupyter.

        Returns:
            Resultado da ação
        """
        logger.info("Creating notebooks structure...")

        # Criar diretório de notebooks
        self.notebooks_dir.mkdir(exist_ok=True)

        # Criar README para notebooks
        notebooks_readme = '''# Jupyter Notebooks - Market Manipulation Lab

Este diretório contém notebooks interativos para aprender sobre microestrutura de mercado
e manipulação através de simulações.

## Notebooks Disponíveis

1. **01_random_walk.ipynb** - Introdução aos mercados justos e random walks
2. **02_wealth_limits.ipynb** - Como restrições de riqueza criam bandas de preço
3. **03_pump_and_dump.ipynb** - Simulando manipulação pump-and-dump
4. **04_detection.ipynb** - Técnicas forenses para detectar manipulação

## Como Usar

```bash
# Instalar dependências de notebooks
pip install -e ".[notebooks,viz]"

# Iniciar Jupyter Lab
jupyter lab
```

## Pré-requisitos

- Python 3.11+
- Jupyter Lab ou Jupyter Notebook
- Market Lab instalado em modo editable
'''

        (self.notebooks_dir / "README.md").write_text(notebooks_readme)

        # Criar template de notebook básico
        notebook_01_template = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Notebook 1: Random Walk e Mercados Justos\\n",
    "\\n",
    "Este notebook introduz o conceito de **mercados justos** que geram random walks gaussianos.\\n",
    "\\n",
    "## Objetivos de Aprendizado\\n",
    "\\n",
    "1. Entender como mercados funcionam através de auction pricing\\n",
    "2. Observar um random walk puro em ação\\n",
    "3. Explorar propriedades estatísticas dos retornos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Imports\\n",
    "import random\\n",
    "from market_lab.core.market import MarketConfig\\n",
    "from market_lab.core.traders import build_traders\\n",
    "from market_lab.core.sentiment import NoSentiment\\n",
    "from market_lab.core.simulation import SimulationRunner\\n",
    "from market_lab.viz.plots import plot_price_series\\n",
    "\\n",
    "import matplotlib.pyplot as plt\\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Configuração da Simulação\\n",
    "\\n",
    "Vamos criar um mercado simples com 150 traders aleatórios."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Configurar mercado\\n",
    "config = MarketConfig(\\n",
    "    n_traders=150,\\n",
    "    initial_price=100.0,\\n",
    "    initial_cash=10_000.0,\\n",
    "    initial_holdings=100,\\n",
    "    min_price=50.0,\\n",
    "    max_price=200.0,\\n",
    "    n_price_points=50\\n",
    ")\\n",
    "\\n",
    "# Criar traders\\n",
    "rng = random.Random(42)\\n",
    "traders = build_traders(config, rng, use_wealth_limit=False)\\n",
    "\\n",
    "print(f\\"Mercado configurado com {len(traders)} traders\\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Executar simulação\\n",
    "runner = SimulationRunner(\\n",
    "    config=config,\\n",
    "    traders=traders,\\n",
    "    sentiment=NoSentiment(),\\n",
    "    manipulator=None\\n",
    ")\\n",
    "\\n",
    "states = runner.run(n_days=120)\\n",
    "print(f\\"Simulação concluída: {len(states)} dias\\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visualizar\\n",
    "plot_price_series(states)\\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
'''

        (self.notebooks_dir / "01_random_walk.ipynb").write_text(notebook_01_template)

        logger.info("Notebooks structure created")

        return {
            "status": "completed",
            "notebooks_created": ["01_random_walk.ipynb"],
            "readme_added": True
        }

    def create_streamlit_dashboard_skeleton(self) -> dict[str, Any]:
        """
        Frontend Developer: Cria esqueleto de dashboard Streamlit.

        Returns:
            Resultado da ação
        """
        logger.info("Creating Streamlit dashboard skeleton...")

        # Criar diretório dashboard
        dashboard_dir = self.project_root / "dashboard"
        dashboard_dir.mkdir(exist_ok=True)

        dashboard_code = '''"""
Market Manipulation Lab - Interactive Dashboard

Streamlit dashboard for exploring market simulations visually.
"""

import streamlit as st
import random
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
from market_lab.core.sentiment import NoSentiment, StepSentiment
from market_lab.core.simulation import SimulationRunner
from market_lab.manipulation.manipulator import Manipulator
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Market Manipulation Lab",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Manipulation Lab")
st.markdown("Explore market microstructure and manipulation through interactive simulations")

# Sidebar - Configuration
st.sidebar.header("⚙️ Simulation Configuration")

n_traders = st.sidebar.slider("Number of Traders", 10, 500, 150)
n_days = st.sidebar.slider("Simulation Days", 30, 365, 120)
initial_price = st.sidebar.number_input("Initial Price", 50.0, 200.0, 100.0)

use_manipulator = st.sidebar.checkbox("Enable Manipulator", value=False)

if use_manipulator:
    st.sidebar.subheader("Manipulator Settings")
    manip_cash = st.sidebar.number_input("Manipulator Cash", 1000, 100000, 50000)
    pump_volume = st.sidebar.slider("Pump Volume Multiplier", 1, 10, 5)

# Run simulation button
if st.sidebar.button("🚀 Run Simulation"):
    with st.spinner("Running simulation..."):
        # Setup
        config = MarketConfig(
            n_traders=n_traders,
            initial_price=initial_price,
            initial_cash=10_000.0,
            initial_holdings=100,
            min_price=initial_price * 0.5,
            max_price=initial_price * 2.0,
            n_price_points=50
        )

        rng = random.Random(42)
        traders = build_traders(config, rng, use_wealth_limit=True)

        manipulator = None
        if use_manipulator:
            manipulator = Manipulator(
                trader_id=-1,
                initial_cash=float(manip_cash),
                initial_holdings=100,
                accumulate_days=30,
                pump_days=10,
                dump_days=15,
                pump_volume=pump_volume
            )

        runner = SimulationRunner(
            config=config,
            traders=traders,
            sentiment=NoSentiment(),
            manipulator=manipulator
        )

        states = runner.run(n_days=n_days)

        # Store in session state
        st.session_state['states'] = states
        st.session_state['manipulator'] = manipulator

    st.success("✅ Simulation completed!")

# Display results
if 'states' in st.session_state:
    states = st.session_state['states']

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Days Simulated", len(states))

    with col2:
        start_price = states[0].price
        end_price = states[-1].price
        price_change = ((end_price - start_price) / start_price) * 100
        st.metric("Price Change", f"{price_change:.2f}%")

    with col3:
        avg_volume = sum(s.cleared_volume for s in states) / len(states)
        st.metric("Avg Volume", f"{avg_volume:.0f}")

    with col4:
        max_price = max(s.price for s in states)
        min_price = min(s.price for s in states)
        volatility = ((max_price - min_price) / start_price) * 100
        st.metric("Volatility Range", f"{volatility:.2f}%")

    # Price chart
    st.subheader("📊 Price Evolution")

    fig, ax = plt.subplots(figsize=(12, 6))
    days = range(len(states))
    prices = [s.price for s in states]

    ax.plot(days, prices, linewidth=2)
    ax.set_xlabel("Day")
    ax.set_ylabel("Price")
    ax.set_title("Market Price Over Time")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    # Volume chart
    st.subheader("📊 Volume Evolution")

    fig, ax = plt.subplots(figsize=(12, 4))
    volumes = [s.cleared_volume for s in states]

    ax.bar(days, volumes, alpha=0.6)
    ax.set_xlabel("Day")
    ax.set_ylabel("Volume")
    ax.set_title("Trading Volume Over Time")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

else:
    st.info("👈 Configure parameters in the sidebar and click 'Run Simulation'")

# Footer
st.markdown("---")
st.markdown("**Market Manipulation Lab** - Educational simulator for market microstructure")
'''

        (dashboard_dir / "app.py").write_text(dashboard_code)

        # Criar README para dashboard
        dashboard_readme = '''# Streamlit Dashboard

Interactive web dashboard for Market Manipulation Lab.

## Running the Dashboard

```bash
# Install with dashboard dependencies
pip install -e ".[viz]"
pip install streamlit

# Run dashboard
cd dashboard
streamlit run app.py
```

The dashboard will open in your browser at http://localhost:8501

## Features

- Interactive configuration of simulations
- Real-time visualization of results
- Manipulator toggle and settings
- Export simulation data
'''

        (dashboard_dir / "README.md").write_text(dashboard_readme)

        logger.info("Streamlit dashboard created")

        return {
            "status": "completed",
            "files_created": ["app.py", "README.md"]
        }


def demonstrate_agent_actions(project_root: Path) -> dict[str, Any]:
    """
    Demonstra ações concretas que os agentes podem executar.

    Args:
        project_root: Raiz do projeto

    Returns:
        Resultados de todas as ações
    """
    actions = AgentActions(project_root)

    results = {}

    print("\n🤖 AGENTES EXECUTANDO AÇÕES CONCRETAS...\n")

    # QA Engineer: Criar testes
    print("🧪 QA Engineer: Creating test structure...")
    results["tests"] = actions.create_test_structure()
    print(f"   ✓ Created {results['tests']['tests_created']} test files\n")

    # DevOps Engineer: CI/CD
    print("⚙️  DevOps Engineer: Setting up CI/CD...")
    results["ci_cd"] = actions.create_github_actions_ci()
    print(f"   ✓ Created GitHub Actions workflow\n")

    # DevOps Engineer: Dev dependencies
    print("📦 DevOps Engineer: Adding dev dependencies...")
    results["dev_deps"] = actions.create_dev_dependencies()
    print(f"   ✓ Added development dependencies\n")

    # CTO: Ruff config
    print("📏 CTO: Configuring ruff linter...")
    results["ruff"] = actions.create_ruff_config()
    print(f"   ✓ Ruff configuration added\n")

    # CTO: Mypy config
    print("🔍 CTO: Configuring mypy type checker...")
    results["mypy"] = actions.create_mypy_config()
    print(f"   ✓ Mypy configuration added\n")

    # Doc Writer + Frontend: Notebooks
    print("📓 Documentation Writer + Frontend Dev: Creating notebooks...")
    results["notebooks"] = actions.create_notebooks_structure()
    print(f"   ✓ Created Jupyter notebooks structure\n")

    # Frontend Dev: Dashboard
    print("🎨 Frontend Developer: Creating Streamlit dashboard...")
    results["dashboard"] = actions.create_streamlit_dashboard_skeleton()
    print(f"   ✓ Streamlit dashboard created\n")

    return results
