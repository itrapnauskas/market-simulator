# 🎓 LEARNING PATH - Market Manipulation Lab

Caminho estruturado para dominar simulação e detecção de manipulação de mercado.

---

## 🗺️ VISÃO GERAL

Este guia te leva do **zero ao herói** em manipulação de mercado financeiro através de 4 níveis progressivos.

**Tempo total:** 6-8 horas
**Pré-requisitos:** Python básico, conceitos básicos de finanças

---

## 📊 NÍVEIS DE APRENDIZADO

```
NÍVEL 1: Fundamentos      [⭐ Iniciante]      2h
    ↓
NÍVEL 2: Restrições       [⭐⭐ Intermediário] 1.5h
    ↓
NÍVEL 3: Manipulação      [⭐⭐⭐ Avançado]    2h
    ↓
NÍVEL 4: Detecção         [⭐⭐⭐⭐ Expert]     2.5h
```

---

## 🎯 NÍVEL 1: FUNDAMENTOS (⭐ Iniciante)

**Objetivo:** Entender como mercados funcionam e o que é um "mercado justo"

**Tempo:** ~2 horas

### 1.1 Teoria Básica (30 min)
📖 **Leia:** `docs/theory.md`

**Tópicos:**
- O que é microestrutura de mercado?
- Auction pricing (leilão de preços)
- Random walk hypothesis
- Eficiência de mercado

**Quiz:**
- [ ] O que é auction pricing?
- [ ] Por que mercados justos geram random walks?
- [ ] O que significa "mercado eficiente"?

---

### 1.2 Arquitetura do Simulador (20 min)
📖 **Leia:** `docs/architecture.md`

**Tópicos:**
- Módulos: core, manipulation, viz, experiments
- Fluxo de simulação
- MarketConfig, Traders, Orders

**Quiz:**
- [ ] Quais são os 4 módulos principais?
- [ ] Como funciona o loop de simulação?
- [ ] O que é um MarketState?

---

### 1.3 Hands-On: Random Walk (45 min)
💻 **Execute:** `notebooks/01_random_walk.ipynb`

**O que você vai fazer:**
- Configurar simulação com 150 traders
- Executar 120 dias de mercado
- Analisar distribuição de retornos
- Testar normalidade (Shapiro-Wilk)
- Verificar autocorrelação

**Exercícios:**
1. Rode com 50 traders. O que muda?
2. Rode com 500 traders. Fica mais "normal"?
3. Aumente volatility_scale. O que acontece?
4. Calcule Sharpe ratio dos retornos

---

### 1.4 Exploração Visual (25 min)
🎨 **Use:** Dashboard Streamlit

```bash
streamlit run dashboard/app.py
```

**Atividades:**
1. Use preset "Quick Start"
2. Rode 3 simulações diferentes
3. Compare resultados visualmente
4. Exporte dados em CSV

**Checkpoint:**
- [ ] Entendo o que é random walk
- [ ] Sei configurar simulações básicas
- [ ] Consigo analisar resultados estatisticamente

---

## 🎯 NÍVEL 2: RESTRIÇÕES DE RIQUEZA (⭐⭐ Intermediário)

**Objetivo:** Entender como limites de capital criam bandas de preço

**Tempo:** ~1.5 horas

### 2.1 Teoria de Wealth Limits (20 min)
📖 **Leia:** `docs/modules_core.md` (seção Traders)

**Tópicos:**
- RandomTrader vs WealthLimitedTrader
- Como cash e holdings limitam ordens
- Mean reversion em mercados limitados

**Quiz:**
- [ ] Por que wealth limits criam bandas?
- [ ] O que acontece quando todos ficam sem cash?
- [ ] Como se calcula fill parcial?

---

### 2.2 Hands-On: Wealth Limits (60 min)
💻 **Execute:** `notebooks/02_wealth_limits.ipynb`

**O que você vai fazer:**
- Comparar mercado sem limites vs com limites
- Visualizar formação de bandas
- Calcular bandas empíricas (μ ± 2σ)
- Testar mean reversion

**Exercícios:**
1. Dobre o initial_cash. Bandas ficam mais largas?
2. Reduza initial_holdings. O que muda?
3. Rode 500 dias. Bandas se estabilizam?
4. Calcule half-life de mean reversion

---

### 2.3 Experimento Prático (10 min)
🔬 **Execute:** `python -m market_lab.experiments.random_walk --n-traders 100 --use-wealth-limit`

**Atividades:**
1. Compare com/sem --use-wealth-limit
2. Salve resultados
3. Calcule estatísticas

**Checkpoint:**
- [ ] Entendo diferença entre traders limitados e ilimitados
- [ ] Sei como bandas de preço se formam
- [ ] Consigo prever comportamento de mercado limitado

---

## 🎯 NÍVEL 3: MANIPULAÇÃO DE MERCADO (⭐⭐⭐ Avançado)

**Objetivo:** Implementar e entender estratégias de manipulação

**Tempo:** ~2 horas

### 3.1 Teoria de Manipulação (30 min)
📖 **Leia:** `GUIDES/MANIPULATION_STRATEGIES.md`

**Tópicos:**
- Pump and Dump
- Spoofing (Layering)
- Wash Trading
- Regulação e ética

**Quiz:**
- [ ] Quais são as 3 fases de pump-and-dump?
- [ ] Como spoofing influencia preços?
- [ ] Por que wash trading é ilegal?

---

### 3.2 Hands-On: Pump and Dump (75 min)
💻 **Execute:** `notebooks/03_pump_and_dump.ipynb`

**O que você vai fazer:**
- Configurar manipulador rico (10x capital)
- Simular ataque completo
- Visualizar fases (accumulation, pump, dump)
- Comparar riqueza manipulador vs traders normais
- Calcular ROI do manipulador

**Exercícios:**
1. Reduza pump_volume. Manipulação ainda funciona?
2. Aumente número de traders normais. Fica mais difícil manipular?
3. Mude duração das fases. Qual é ótima?
4. Calcule lucro máximo teórico

---

### 3.3 Outras Estratégias (15 min)
🔬 **Execute:** `examples/manipulation_strategies.py`

**Atividades:**
1. Veja spoofing em ação
2. Veja wash trading
3. Compare lucratividade das 3 estratégias
4. Identifique padrões únicos de cada uma

**Checkpoint:**
- [ ] Entendo como pump-and-dump funciona
- [ ] Sei implementar manipuladores customizados
- [ ] Consigo comparar eficácia de estratégias

---

## 🎯 NÍVEL 4: DETECÇÃO FORENSE (⭐⭐⭐⭐ Expert)

**Objetivo:** Detectar manipulação usando técnicas estatísticas e ML

**Tempo:** ~2.5 horas

### 4.1 Teoria de Detecção (40 min)
📖 **Leia:** `docs/ADVANCED_DETECTION_GUIDE.md`

**Tópicos:**
- Z-score e anomaly detection
- Isolation Forest
- Lei de Benford
- Volume profile analysis
- Network analysis

**Quiz:**
- [ ] Como z-score detecta anomalias?
- [ ] O que é Isolation Forest?
- [ ] Por que Lei de Benford funciona para volumes?
- [ ] O que é ensemble detection?

---

### 4.2 Hands-On: Detecção Forense (90 min)
💻 **Execute:** `notebooks/04_detection_forensics.ipynb`

**O que você vai fazer:**
- Preparar dataset limpo vs manipulado
- Implementar 3 detectores
- Calcular ROC curves e AUC
- Criar ensemble detector
- Analisar falsos positivos/negativos

**Exercícios:**
1. Crie seu próprio detector customizado
2. Optimize threshold para 95% precision
3. Compare detectores: qual melhor para pump-dump?
4. Qual melhor para wash trading?

---

### 4.3 Algoritmos Avançados (20 min)
🔬 **Execute:** `examples/advanced_detection_demo.py`

**Atividades:**
1. Rode ensemble_detection
2. Veja scores para cada dia
3. Identifique dias de alta manipulação
4. Compare com ground truth

**Checkpoint:**
- [ ] Sei implementar detectores estatísticos
- [ ] Entendo trade-offs precision vs recall
- [ ] Consigo criar ensemble de detectores
- [ ] Posso avaliar qualidade de detecção (ROC, AUC)

---

## 🎓 CERTIFICAÇÃO (Opcional)

### Projeto Final: Detector Customizado

**Objetivo:** Criar detector próprio que supere ensemble padrão

**Requisitos:**
1. Precision > 90%
2. Recall > 85%
3. False Positive Rate < 5%
4. Funciona para pelo menos 2 estratégias

**Passos:**
1. Escolha features (preço, volume, imbalance, etc)
2. Implemente algoritmo em `advanced_detection.py`
3. Teste com dados sintéticos
4. Compare com ensemble_detection
5. Documente resultados

**Entrega:**
- Código documentado
- Notebook com análise
- Comparação de métricas

---

## 📚 RECURSOS ADICIONAIS

### Depois de Completar os 4 Níveis

**Para Desenvolvedores:**
- Leia `DEVELOPMENT_GUIDE.md`
- Implemente nova estratégia de manipulação
- Contribua com testes (veja `tests/`)

**Para Pesquisadores:**
- Experimente com parâmetros diferentes
- Teste em dados reais (se tiver acesso)
- Publique paper usando o simulador

**Para Educadores:**
- Use notebooks em aulas
- Customize para seu curso
- Crie exercícios adicionais

---

## 🗺️ ROADMAP ALTERNATIVO

### Track Rápido (3 horas)
Para quem tem pressa:
1. `docs/theory.md` (20 min)
2. `01_random_walk.ipynb` (30 min)
3. `03_pump_and_dump.ipynb` (60 min)
4. `04_detection_forensics.ipynb` (60 min)
5. Dashboard exploration (30 min)

### Track Profundo (12 horas)
Para quem quer dominar tudo:
1. Todos os 4 níveis acima
2. Leia TODA documentação em `docs/`
3. Leia código fonte completo
4. Implemente 2 estratégias novas
5. Crie 5 detectores customizados
6. Contribua com PR no GitHub

---

## ✅ CHECKLIST DE PROGRESSO

### Nível 1: Fundamentos
- [ ] Li teoria básica
- [ ] Entendo arquitetura
- [ ] Completei notebook 01
- [ ] Explorei dashboard

### Nível 2: Restrições
- [ ] Entendo wealth limits
- [ ] Completei notebook 02
- [ ] Rodei experimentos

### Nível 3: Manipulação
- [ ] Li teoria de manipulação
- [ ] Completei notebook 03
- [ ] Explorei 3 estratégias

### Nível 4: Detecção
- [ ] Li teoria de detecção
- [ ] Completei notebook 04
- [ ] Rodei algoritmos avançados

### Projeto Final
- [ ] Criei detector customizado
- [ ] Precision > 90%
- [ ] Documentei resultados

---

## 🎉 PARABÉNS!

Ao completar este learning path, você será capaz de:

✅ Simular mercados financeiros realisticamente
✅ Implementar estratégias de manipulação
✅ Detectar manipulação com alta precisão
✅ Analisar microestrutura de mercado
✅ Contribuir para o projeto

**Próximo passo:** Compartilhe seu conhecimento ou contribua com código!

---

**Dúvidas?** Abra issue no GitHub ou consulte `docs/` para detalhes técnicos.

**Boa sorte! 🚀**
