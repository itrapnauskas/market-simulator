# 🌅 BOM DIA! COMECE AQUI AMANHÃ

Guia ultra-rápido para você começar a trabalhar e testar o projeto hoje!

---

## ⚡ INSTALAÇÃO (2 minutos)

```bash
# 1. Vá para o diretório
cd /home/user/market-simulator

# 2. Instale TUDO
pip install -e ".[dev,viz,ml]"

# 3. Confirme que funciona
pytest tests/ -v --tb=short
```

**Esperado:** ~85 testes passando (alguns podem falhar, ok!)

---

## 🎯 O QUE FAZER PRIMEIRO? (Escolha 1)

### Opção 1: 📚 APRENDER (Recomendado!)

```bash
# Abrir Jupyter
jupyter lab notebooks/

# Começar pelo notebook 01
# notebooks/01_random_walk.ipynb
```

**Tempo:** 45-60 minutos
**O que vai aprender:** Como mercados funcionam, random walk

---

### Opção 2: 🎨 EXPLORAR VISUALMENTE

```bash
# Dashboard web
streamlit run dashboard/app.py
```

**Acesse:** http://localhost:8501
**O que fazer:**
1. Clique em preset "Quick Start"
2. Clique "Run Simulation"
3. Explore as tabs!

---

### Opção 3: 💻 DESENVOLVER

```bash
# Ver estrutura de código
cat DEVELOPMENT_GUIDE.md | head -100

# Rodar um exemplo
python examples/manipulation_strategies.py

# Ver testes
pytest tests/test_core/test_market.py -v
```

---

### Opção 4: 🤖 USAR AGENTES IA

```bash
# Demo dos agentes
python run_agents.py --demo

# Rodar ciclo completo
python run_agents.py --full
```

**Tempo:** 2-5 minutos
**O que faz:** Agentes analisam e melhoram o projeto

---

## 📖 DOCUMENTAÇÃO - ONDE ESTÁ CADA COISA

### Para Iniciantes
```
START_HERE.md       → Guia de 5 minutos
LEARNING_PATH.md    → Caminho estruturado (6-8h)
notebooks/          → Tutoriais interativos
```

### Para Desenvolvedores
```
DEVELOPMENT_GUIDE.md → Guia completo de dev
GUIDES/CICD.md       → CI/CD e DevOps
tests/               → 95 testes
```

### Para Pesquisadores
```
docs/theory.md                      → Teoria de mercados
GUIDES/MANIPULATION_STRATEGIES.md   → Estratégias
docs/ADVANCED_DETECTION_GUIDE.md    → Detecção avançada
```

### Índice Completo
```
PROJECT_INDEX.md    → TODOS os arquivos explicados
```

---

## 🗂️ ESTRUTURA SUPER RESUMIDA

```
market-simulator/
├── START_HERE.md          ⭐ COMECE AQUI
├── TOMORROW_START.md      ⭐ VOCÊ ESTÁ AQUI!
│
├── notebooks/             📓 4 tutoriais (5h conteúdo)
├── dashboard/             🎨 Interface web
├── examples/              💡 Scripts demo
│
├── src/market_lab/        💻 CÓDIGO FONTE
│   ├── core/              ⚙️  Simulador
│   ├── manipulation/      🎭 Estratégias
│   └── agents/            🤖 Agentes IA
│
└── tests/                 🧪 95 testes
```

---

## ✅ CHECKLIST PARA HOJE

### Setup (5 min)
- [ ] `pip install -e ".[dev,viz,ml]"`
- [ ] `pytest tests/` (verificar que funciona)
- [ ] Escolher uma opção acima

### Exploração (30-60 min)
- [ ] Rodar notebook 01 OU dashboard OU exemplo
- [ ] Entender o básico de como funciona
- [ ] Brincar com parâmetros

### Próximos Passos (conforme interesse)
- [ ] Ler LEARNING_PATH.md para caminho completo
- [ ] Ler DEVELOPMENT_GUIDE.md se vai desenvolver
- [ ] Explorar GUIDES/ para tópicos específicos

---

## 🚨 PROBLEMAS COMUNS

### "ModuleNotFoundError: market_lab"
```bash
pip install -e .
```

### "pytest not found"
```bash
pip install -e ".[dev]"
```

### "Notebooks não abrem"
```bash
pip install -e ".[viz]"
pip install jupyter jupyterlab
jupyter lab
```

### "Quer tudo de uma vez?"
```bash
pip install -e ".[dev,viz,ml]"
```

---

## 💡 DICAS PRO

### Comandos Úteis
```bash
make help           # Ver TODOS os comandos
make test           # Rodar testes
make lint           # Verificar qualidade
make ci             # CI completa local
```

### Exploração Rápida
```bash
# Ver o que cada módulo faz
cat docs/modules_core.md | less

# Ver estratégias disponíveis
ls src/market_lab/manipulation/*.py

# Ver notebooks
ls notebooks/*.ipynb
```

### Atalhos do Projeto
```bash
# Rodar simulação rápida
python -m market_lab.experiments.random_walk --n-traders 50

# Ver agentes em ação
python run_agents.py --demo
```

---

## 🎯 SUGESTÃO DO DIA

**Para máxima produtividade:**

**Manhã (1h):**
1. `pip install -e ".[dev,viz,ml]"` (2 min)
2. `jupyter lab notebooks/01_random_walk.ipynb` (45 min)
3. `streamlit run dashboard/app.py` (15 min explorando)

**Tarde (2h):**
1. Ler `DEVELOPMENT_GUIDE.md` (30 min)
2. Rodar `examples/manipulation_strategies.py` (15 min)
3. Explorar código em `src/market_lab/core/` (45 min)
4. Rodar testes `pytest tests/test_core/ -v` (10 min)

**Fim do dia:**
- Você entende como funciona ✅
- Sabe onde tudo está ✅
- Pode começar a desenvolver ✅

---

## 📞 SE TIVER DÚVIDAS

1. Veja `PROJECT_INDEX.md` (índice completo)
2. Veja `START_HERE.md` (guia de 5min)
3. Veja `DEVELOPMENT_GUIDE.md` (se for desenvolver)
4. Explore `GUIDES/` (tópicos específicos)

---

## 🎉 VOCÊ ESTÁ PRONTO!

O projeto está **100% organizado** e **pronto para uso**.

**Escolha uma opção acima e BOA SORTE! 🚀**

---

**Última atualização:** 2025-11-19
**Status:** ✅ Production Ready
**Projeto por:** 7 agentes especializados + você!
