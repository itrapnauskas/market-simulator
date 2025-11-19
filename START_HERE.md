# 🚀 START HERE - Market Manipulation Lab

**Bem-vindo!** Este é seu guia de início rápido para começar a trabalhar com o Market Manipulation Lab.

---

## 📋 QUICK START (5 minutos)

### 1. Instalação
```bash
# Clone já está feito, então vamos instalar:
cd /home/user/market-simulator

# Instalar em modo desenvolvimento com TODAS as features
pip install -e ".[dev,viz,ml]"
```

### 2. Testar que Funciona
```bash
# Rodar testes
pytest tests/ -v

# Rodar exemplo básico
python examples/manipulation_strategies.py
```

### 3. Explorar Interativamente
```bash
# Opção 1: Jupyter Notebooks (RECOMENDADO para aprender)
jupyter lab notebooks/

# Opção 2: Dashboard Web
streamlit run dashboard/app.py

# Opção 3: Sistema de Agentes
python run_agents.py --demo
```

---

## 📁 ESTRUTURA DO PROJETO

```
market-simulator/
│
├── 📖 START_HERE.md              ← VOCÊ ESTÁ AQUI!
├── 📖 README.md                  ← Overview do projeto
│
├── 🎓 LEARNING_PATH.md           ← Caminho de aprendizado
├── 🔧 DEVELOPMENT_GUIDE.md       ← Guia para desenvolvedores
│
├── src/market_lab/               ← CÓDIGO FONTE PRINCIPAL
│   ├── core/                     ← Simulador de mercado
│   ├── manipulation/             ← Estratégias de manipulação
│   ├── viz/                      ← Visualizações
│   ├── agents/                   ← Sistema de agentes IA
│   └── experiments/              ← Experimentos prontos
│
├── 📓 notebooks/                 ← JUPYTER NOTEBOOKS (comece aqui!)
│   ├── 01_random_walk.ipynb
│   ├── 02_wealth_limits.ipynb
│   ├── 03_pump_and_dump.ipynb
│   └── 04_detection_forensics.ipynb
│
├── 🎨 dashboard/                 ← DASHBOARD STREAMLIT
│   ├── app.py                    ← App principal
│   ├── components/               ← Componentes UI
│   └── requirements.txt
│
├── 📚 examples/                  ← SCRIPTS DE EXEMPLO
│   ├── manipulation_strategies.py
│   ├── manipulation_simulation.py
│   └── advanced_detection_demo.py
│
├── 🧪 tests/                     ← TESTES (95 testes!)
│   ├── test_core/
│   └── test_manipulation/
│
├── 📖 docs/                      ← DOCUMENTAÇÃO TÉCNICA
│   ├── theory.md                 ← Teoria de mercados
│   ├── architecture.md           ← Arquitetura do código
│   └── ADVANCED_DETECTION_GUIDE.md
│
└── 🔧 GUIDES/                    ← GUIAS ESPECIALIZADOS
    ├── MANIPULATION_STRATEGIES.md
    ├── AGENTS.md
    ├── CICD.md
    └── DEVOPS_SUMMARY.md
```

---

## 🎯 O QUE VOCÊ QUER FAZER?

### Opção 1: 📚 **APRENDER** sobre manipulação de mercado
**→ Vá para:** `notebooks/01_random_walk.ipynb`

```bash
jupyter lab notebooks/01_random_walk.ipynb
```

Depois siga a sequência: 01 → 02 → 03 → 04

---

### Opção 2: 🎮 **BRINCAR** com simulações
**→ Use o Dashboard:**

```bash
streamlit run dashboard/app.py
```

Abra http://localhost:8501 e explore!

---

### Opção 3: 💻 **DESENVOLVER** novas features
**→ Leia:** `DEVELOPMENT_GUIDE.md`

```bash
# Setup ambiente de dev
make dev-setup

# Rodar testes
make test

# Criar nova estratégia
# (veja DEVELOPMENT_GUIDE.md)
```

---

### Opção 4: 🔬 **PESQUISAR** detecção de manipulação
**→ Vá para:** `examples/advanced_detection_demo.py`

```bash
python examples/advanced_detection_demo.py
```

Leia depois: `docs/ADVANCED_DETECTION_GUIDE.md`

---

### Opção 5: 🤖 **USAR AGENTES IA** para desenvolvimento
**→ Execute:**

```bash
python run_agents.py --full
```

Leia depois: `GUIDES/AGENTS.md`

---

## 🎓 CAMINHO DE APRENDIZADO RECOMENDADO

**Para iniciantes em finanças:**
1. Leia `docs/theory.md` (20 min)
2. Notebook `01_random_walk.ipynb` (45 min)
3. Notebook `02_wealth_limits.ipynb` (60 min)
4. Dashboard para explorar visualmente (30 min)

**Para desenvolvedores Python:**
1. Leia `docs/architecture.md` (15 min)
2. Leia `DEVELOPMENT_GUIDE.md` (20 min)
3. Rode `pytest tests/` (2 min)
4. Explore `examples/manipulation_strategies.py` (15 min)

**Para cientistas de dados:**
1. Notebook `04_detection_forensics.ipynb` (90 min)
2. Leia `docs/ADVANCED_DETECTION_GUIDE.md` (30 min)
3. Rode `examples/advanced_detection_demo.py` (5 min)
4. Experimente com seus próprios algoritmos!

---

## 🛠️ COMANDOS ÚTEIS

### Desenvolvimento
```bash
make help              # Ver todos os comandos disponíveis
make test              # Rodar testes
make format            # Formatar código com ruff
make lint              # Verificar qualidade
make ci                # Rodar CI localmente
```

### Exploração
```bash
# Rodar experimento básico
python -m market_lab.experiments.random_walk

# Ver estratégias de manipulação
python examples/manipulation_strategies.py

# Detectores avançados
python examples/advanced_detection_demo.py
```

### Docker (se preferir)
```bash
make docker-jupyter      # Jupyter em container
make docker-dashboard    # Dashboard em container
```

---

## 📚 DOCUMENTAÇÃO PRINCIPAL

### Para Usuários
- **README.md** - Overview geral do projeto
- **LEARNING_PATH.md** - Caminho de aprendizado estruturado
- **notebooks/** - Tutoriais interativos
- **docs/theory.md** - Fundamentos teóricos

### Para Desenvolvedores
- **DEVELOPMENT_GUIDE.md** - Como desenvolver
- **docs/architecture.md** - Arquitetura do código
- **GUIDES/CICD.md** - CI/CD e DevOps

### Guias Especializados
- **GUIDES/MANIPULATION_STRATEGIES.md** - Estratégias de manipulação
- **GUIDES/AGENTS.md** - Sistema de agentes IA
- **docs/ADVANCED_DETECTION_GUIDE.md** - Detecção avançada

---

## ❓ PROBLEMAS COMUNS

### "ModuleNotFoundError: No module named 'market_lab'"
```bash
pip install -e .
```

### "pytest not found"
```bash
pip install -e ".[dev]"
```

### "matplotlib not working"
```bash
pip install -e ".[viz]"
```

### "Quer tudo?"
```bash
pip install -e ".[dev,viz,ml]"
```

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Escolha uma opção acima (Aprender, Brincar, Desenvolver, etc)
2. ✅ Siga o caminho recomendado
3. ✅ Consulte a documentação conforme necessário
4. ✅ Divirta-se explorando manipulação de mercado! 🚀

---

## 💡 DICAS

- 🔥 **Comece pelos notebooks** - são interativos e educacionais
- 🎨 **Use o dashboard** - para visualizar rapidamente
- 🧪 **Rode os testes** - para entender o código
- 🤖 **Experimente os agentes** - para ver IA em ação
- 📖 **Leia a teoria** - para entender o "porquê"

---

**Desenvolvido com ❤️ por um exército de agentes especializados**

**Versão:** 0.2.0
**Última atualização:** 2025-11-19
**Status:** 🟢 Production Ready
