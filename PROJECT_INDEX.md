# 📑 PROJECT INDEX - Market Manipulation Lab

Índice completo de TODOS os arquivos e pastas do projeto com descrições.

---

## 📖 DOCUMENTAÇÃO PRINCIPAL (Raiz)

| Arquivo | Descrição | Para Quem | Prioridade |
|---------|-----------|-----------|------------|
| **START_HERE.md** | 🚀 **COMECE AQUI!** Guia de 5 minutos | Todos | ⭐⭐⭐⭐⭐ |
| **README.md** | Overview do projeto, badges, objetivos | Todos | ⭐⭐⭐⭐⭐ |
| **LEARNING_PATH.md** | Caminho estruturado 4 níveis (6-8h) | Iniciantes/Estudantes | ⭐⭐⭐⭐ |
| **DEVELOPMENT_GUIDE.md** | Guia completo para desenvolvedores | Desenvolvedores | ⭐⭐⭐⭐ |
| **PROJECT_INDEX.md** | Este arquivo - índice completo | Todos | ⭐⭐⭐ |

---

## 📚 GUIDES/ - Guias Especializados

| Arquivo | Descrição | Para Quem |
|---------|-----------|-----------|
| **README.md** | Índice dos guias | Todos |
| **MANIPULATION_STRATEGIES.md** | Guia de estratégias (spoofing, wash trading) | Usuários/Pesquisadores |
| **AGENTS.md** | Sistema de 13 agentes IA para dev autônomo | Desenvolvedores |
| **CICD.md** | CI/CD completo (GitHub Actions, Docker) | DevOps |
| **DEVOPS_SUMMARY.md** | Resumo executivo de infraestrutura | DevOps/Gestores |
| **ADVANCED_DETECTION_SUMMARY.md** | Resumo de algoritmos de detecção | Cientistas de Dados |
| **QUICK_START_ADVANCED_DETECTION.md** | Quick start para detectores | Cientistas de Dados |

---

## 📖 docs/ - Documentação Técnica Detalhada

| Arquivo | Descrição | Conteúdo |
|---------|-----------|----------|
| **overview.md** | Visão geral e motivação | Por que este projeto existe |
| **theory.md** | Fundamentos teóricos | Microestrutura, auction pricing, random walk |
| **architecture.md** | Arquitetura do código | Módulos, design patterns, fluxo |
| **simulation_flow.md** | Fluxo de simulação detalhado | Loop diário, formação de preço |
| **modules_core.md** | Documentação de core/ | market, traders, orders, sentiment |
| **modules_manipulation.md** | Documentação de manipulation/ | Estratégias e detecção |
| **modules_viz.md** | Documentação de viz/ | Plots e animações |
| **roadmap.md** | Roadmap de desenvolvimento | Features futuras |
| **ADVANCED_DETECTION_GUIDE.md** | Guia completo de detecção | 5 algoritmos, teoria, uso |

---

## 💻 src/market_lab/ - Código Fonte

### **src/market_lab/core/** - Simulador Base

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `market.py` | 57 | MarketConfig, MarketState, auction pricing |
| `traders.py` | 130 | RandomTrader, WealthLimitedTrader |
| `orders.py` | 103 | Order, OrderCurves, aggregation |
| `sentiment.py` | 55 | NoSentiment, StepSentiment, PulseSentiment |
| `simulation.py` | 99 | SimulationRunner (loop principal) |

**Total core:** ~444 LOC

---

### **src/market_lab/manipulation/** - Manipulação e Detecção

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `manipulator.py` | 65 | Pump-and-dump base class |
| `spoofing.py` | 235 | Spoofing/layering strategy |
| `wash_trading.py` | 281 | Self-trading strategy |
| `layering.py` | ~200 | Quote stuffing |
| `detection.py` | 49 | Detectores básicos (z-score, imbalance) |
| `advanced_detection.py` | 957 | 5 algoritmos avançados (ML, Benford, etc) |
| `metrics.py` | 51 | Métricas auxiliares |

**Total manipulation:** ~1,838 LOC

---

### **src/market_lab/viz/** - Visualização

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `plots.py` | 84 | Gráficos matplotlib |
| `animation.py` | 49 | Animações |

**Total viz:** ~133 LOC

---

### **src/market_lab/agents/** - Sistema de Agentes IA

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `core.py` | 8,207 | Agent, Message, CommunicationBus |
| `specialists.py` | 25,095 | 13 agentes especializados |
| `organization.py` | 15,668 | Orquestração Discovery→Planning→Execution |
| `runner.py` | 3,587 | CLI para rodar agentes |
| `actions.py` | 22,622 | Ações concretas (criar arquivos, etc) |

**Total agents:** ~75,179 LOC

---

### **src/market_lab/experiments/** - Experimentos Prontos

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `random_walk.py` | 47 | Experimento baseline com CLI |

---

## 🧪 tests/ - Testes (95 testes, 2,288 LOC)

### **tests/test_core/**

| Arquivo | Testes | LOC | Descrição |
|---------|--------|-----|-----------|
| `test_orders.py` | 6 | 70 | Testes de Order e aggregation |
| `test_market.py` | 19 | 309 | Testes de auction pricing |
| `test_traders.py` | 34 | 539 | Testes de traders (Random, WealthLimited) |
| `test_simulation.py` | 26 | ~400 | Testes de integração completa |

**Total test_core:** 85 testes

---

### **tests/test_manipulation/**

| Arquivo | Testes | LOC | Descrição |
|---------|--------|-----|-----------|
| `test_manipulator.py` | 28 | ~700 | Testes de pump-and-dump |
| `test_advanced_detection.py` | 37 | 561 | Testes de detectores avançados |

**Total test_manipulation:** 65 testes

---

### **tests/conftest.py**

Fixtures compartilhadas:
- `rng` - Random com seed fixa
- `basic_config` - MarketConfig padrão
- `traders` - Lista de traders

---

## 📓 notebooks/ - Jupyter Notebooks Educacionais

| Notebook | Tamanho | Dificuldade | Tempo | Descrição |
|----------|---------|-------------|-------|-----------|
| `01_random_walk.ipynb` | 8.4KB | ⭐ Iniciante | 45-60min | Introdução aos mercados justos |
| `02_wealth_limits.ipynb` | 14KB | ⭐⭐ Intermediário | 60-75min | Formação de bandas de preço |
| `03_pump_and_dump.ipynb` | 19KB | ⭐⭐⭐ Avançado | 75-90min | Anatomia de pump-and-dump |
| `04_detection_forensics.ipynb` | 28KB | ⭐⭐⭐⭐ Expert | 90-120min | Técnicas de detecção forense |
| **README.md** | - | - | - | Como usar os notebooks |

**Total:** 69.4KB, 4 notebooks, ~5h de conteúdo

---

## 🎨 dashboard/ - Dashboard Streamlit

### **dashboard/app.py** (145 LOC)
Dashboard principal

### **dashboard/components/** - Componentes Modulares

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `theme.py` | 228 | Paleta de cores, CSS customizado |
| `charts.py` | 447 | 8 visualizações Plotly |
| `config.py` | 415 | UI de configuração, presets, save/load |
| `utils.py` | 455 | Export, métricas, tabelas |
| `layout.py` | 439 | Header, footer, help, tutorial |

**Total dashboard:** 2,129 LOC

### **dashboard/IMPROVEMENTS.md**
Documentação das melhorias UX

### **dashboard/README.md**
Como usar o dashboard

### **dashboard/requirements.txt**
Dependências específicas

---

## 📚 examples/ - Scripts de Exemplo

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `manipulation_strategies.py` | ~250 | Demo de 3 estratégias |
| `manipulation_simulation.py` | ~200 | Simulação completa |
| `advanced_detection_demo.py` | ~250 | Demo de detectores |

**Total examples:** ~700 LOC

---

## 🔧 .github/ - CI/CD e Automação

### **.github/workflows/**

| Arquivo | Descrição |
|---------|-----------|
| `ci.yml` | CI completo (3 Python × 3 OS = 9 configs) |
| `release.yml` | Automação de release para PyPI |
| `docs.yml` | Build docs + GitHub Pages |
| `README.md` | Documentação dos workflows |

### **.github/dependabot.yml**
Auto-update de dependências semanais

---

## 🐳 Docker

| Arquivo | Descrição |
|---------|-----------|
| **Dockerfile** | Multi-stage build (5 stages) |
| **docker-compose.yml** | 6 serviços orquestrados |
| **.dockerignore** | Otimização de build |

**Stages:**
1. builder - Build dependencies
2. runtime - Minimal production
3. development - Dev tools
4. jupyter - Jupyter Lab
5. dashboard - Streamlit

---

## 🛠️ Configuração e Build

| Arquivo | Descrição |
|---------|-----------|
| **pyproject.toml** | Configuração do projeto, deps, ruff, mypy |
| **Makefile** | 40+ comandos úteis |
| **.gitignore** | Git ignore rules |
| **run_agents.py** | CLI para sistema de agentes |

---

## 📊 ESTATÍSTICAS DO PROJETO

### Código
- **Total LOC:** ~80,000 linhas
  - Fonte (src/): ~77,594 LOC
  - Testes: ~2,288 LOC
  - Exemplos: ~700 LOC
  - Dashboard: ~2,129 LOC

### Documentação
- **Total DOC:** ~3,000 linhas
  - Guias: ~1,000 linhas
  - docs/: ~1,500 linhas
  - README/START_HERE/etc: ~500 linhas

### Testes
- **95 test cases**
- **Test coverage:** ~85% (core), ~30% (geral)

### Notebooks
- **4 notebooks completos**
- **~5 horas** de conteúdo educacional

---

## 🗺️ NAVEGAÇÃO RÁPIDA

### Primeiro Dia
```
START_HERE.md → notebooks/01_*.ipynb → dashboard/app.py
```

### Aprendizado Completo
```
LEARNING_PATH.md → (4 níveis) → Projeto final
```

### Desenvolvimento
```
DEVELOPMENT_GUIDE.md → tests/ → src/market_lab/
```

### Pesquisa
```
docs/theory.md → notebooks/04_*.ipynb → GUIDES/MANIPULATION_STRATEGIES.md
```

---

## 🎯 ARQUIVOS MAIS IMPORTANTES

**Top 10 por importância:**

1. **START_HERE.md** - Ponto de entrada
2. **README.md** - Overview
3. **notebooks/01_random_walk.ipynb** - Primeiro tutorial
4. **src/market_lab/core/simulation.py** - Loop principal
5. **DEVELOPMENT_GUIDE.md** - Para desenvolvedores
6. **tests/conftest.py** - Fixtures de teste
7. **dashboard/app.py** - Interface visual
8. **GUIDES/MANIPULATION_STRATEGIES.md** - Guia de estratégias
9. **docs/theory.md** - Fundamentação teórica
10. **pyproject.toml** - Configuração do projeto

---

## 📁 ESTRUTURA VISUAL

```
market-simulator/
│
├── 📄 START_HERE.md ⭐⭐⭐⭐⭐
├── 📄 README.md
├── 📄 LEARNING_PATH.md
├── 📄 DEVELOPMENT_GUIDE.md
├── 📄 PROJECT_INDEX.md (você está aqui!)
│
├── 📁 GUIDES/ (6 guias especializados)
├── 📁 docs/ (9 arquivos de documentação técnica)
│
├── 📁 src/market_lab/ ⚙️ CÓDIGO FONTE
│   ├── core/ (5 arquivos, 444 LOC)
│   ├── manipulation/ (7 arquivos, 1,838 LOC)
│   ├── viz/ (2 arquivos, 133 LOC)
│   ├── agents/ (5 arquivos, 75,179 LOC)
│   └── experiments/ (1 arquivo, 47 LOC)
│
├── 📁 tests/ 🧪 (7 arquivos, 95 testes)
├── 📁 notebooks/ 📓 (4 notebooks, 5h conteúdo)
├── 📁 dashboard/ 🎨 (6 arquivos, 2,129 LOC)
├── 📁 examples/ 📚 (3 arquivos, 700 LOC)
│
├── 📁 .github/ ⚙️ (4 workflows)
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
├── 🛠️ Makefile
├── ⚙️ pyproject.toml
└── 🤖 run_agents.py
```

---

**Última atualização:** 2025-11-19
**Total de arquivos:** ~100+
**Total de linhas:** ~85,000
