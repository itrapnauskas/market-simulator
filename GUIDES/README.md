# 📚 GUIDES - Specialized Documentation

Esta pasta contém guias especializados para diferentes aspectos do Market Manipulation Lab.

---

## 📖 GUIAS DISPONÍVEIS

### Para Todos os Usuários

#### **MANIPULATION_STRATEGIES.md**
- **O que é:** Guia completo sobre estratégias de manipulação
- **Conteúdo:**
  - Spoofing (Layering)
  - Wash Trading
  - Pump and Dump
  - Parâmetros configuráveis
  - Exemplos de uso
- **Quando ler:** Depois de completar notebook 03

---

### Para Desenvolvedores

#### **AGENTS.md**
- **O que é:** Sistema de agentes IA para desenvolvimento autônomo
- **Conteúdo:**
  - 13 agentes especializados (CEO, CTO, QA, etc)
  - Communication bus
  - Pipeline Discovery → Planning → Execution
  - Como usar: `python run_agents.py --full`
- **Quando ler:** Quando quiser automatizar desenvolvimento

#### **CICD.md**
- **O que é:** Guia de CI/CD e DevOps
- **Conteúdo:**
  - GitHub Actions workflows
  - Docker e docker-compose
  - Makefile commands
  - Release process
- **Quando ler:** Ao contribuir com código

#### **DEVOPS_SUMMARY.md**
- **O que é:** Resumo executivo da infraestrutura
- **Conteúdo:**
  - Features de CI/CD
  - Métricas de infraestrutura
  - Comparação antes/depois
  - Quick start DevOps
- **Quando ler:** Overview rápido de infraestrutura

---

### Para Cientistas de Dados

#### **ADVANCED_DETECTION_SUMMARY.md**
- **O que é:** Resumo executivo dos algoritmos de detecção
- **Conteúdo:**
  - 5 algoritmos implementados
  - Métricas de accuracy
  - Comparação vs métodos básicos
  - Quick start
- **Quando ler:** Overview rápido de detecção

#### **QUICK_START_ADVANCED_DETECTION.md**
- **O que é:** Guia rápido para usar detectores avançados
- **Conteúdo:**
  - Como usar ensemble_detection
  - Exemplos de código
  - Interpretar resultados
- **Quando ler:** Ao usar detecção avançada
- **Complemento:** `docs/ADVANCED_DETECTION_GUIDE.md` (guia completo)

---

## 🗺️ NAVEGAÇÃO

### Iniciante
1. Comece em `../START_HERE.md`
2. Siga `../LEARNING_PATH.md`
3. Volte aos guias quando relevante

### Desenvolvedor
1. Leia `../DEVELOPMENT_GUIDE.md`
2. Consulte **CICD.md** e **DEVOPS_SUMMARY.md**
3. Use **AGENTS.md** para automatização

### Pesquisador
1. Leia **MANIPULATION_STRATEGIES.md**
2. Leia **ADVANCED_DETECTION_SUMMARY.md**
3. Veja guia completo em `../docs/ADVANCED_DETECTION_GUIDE.md`

---

## 📁 OUTROS RECURSOS

### Documentação Técnica Detalhada
Veja pasta `../docs/`:
- `theory.md` - Fundamentos teóricos
- `architecture.md` - Arquitetura do código
- `ADVANCED_DETECTION_GUIDE.md` - Guia completo de detecção
- `modules_*.md` - Documentação de cada módulo

### Tutoriais Interativos
Veja pasta `../notebooks/`:
- 01_random_walk.ipynb
- 02_wealth_limits.ipynb
- 03_pump_and_dump.ipynb
- 04_detection_forensics.ipynb

### Exemplos de Código
Veja pasta `../examples/`:
- manipulation_strategies.py
- manipulation_simulation.py
- advanced_detection_demo.py

---

## 🔍 BUSCA RÁPIDA

**Procurando por:**

- Como implementar manipulação? → **MANIPULATION_STRATEGIES.md**
- Como usar agentes IA? → **AGENTS.md**
- Como funciona CI/CD? → **CICD.md**
- Como detectar manipulação? → **ADVANCED_DETECTION_SUMMARY.md**
- Métricas de detecção? → `../docs/ADVANCED_DETECTION_GUIDE.md`
- Setup DevOps? → **DEVOPS_SUMMARY.md**

---

**Desenvolvido por um exército de agentes especializados! 🤖**
