# Roadmap

Este documento lista ideias de evolução do projeto.

---

## Versão 0.1 – Núcleo mínimo

- [ ] Implementar `MarketConfig`, `MarketState`.
- [ ] Implementar `RandomTrader` sem wealth-limit.
- [ ] Implementar geração de ordens e auction pricing.
- [ ] Implementar experimento `random_walk.py`.
- [ ] Adicionar notebook `01_random_market.ipynb`.
- [ ] Criar gráficos básicos: preço, volume.

---

## Versão 0.2 – Wealth-Limited e bandas

- [ ] Implementar `WealthLimitedTrader`.
- [ ] Adicionar experimento `wealth_limits.py`.
- [ ] Notebook `02_wealth_limits.ipynb` com comparação:
  - random walk puro vs wealth-limited.
- [ ] Gráficos mostrando canais/bandas emergentes.

---

## Versão 0.3 – Manipulador simples

- [ ] Implementar classe `Manipulator`.
- [ ] Adicionar estratégia básica de pump-and-dump.
- [ ] Experimento `pump_and_dump.py`.
- [ ] Notebook `03_manipulation_cycle.ipynb`.
- [ ] Gráficos:
  - riqueza do manipulador vs outros,
  - preço com fases do ciclo destacadas.

---

## Versão 0.4 – Métricas de detecção

- [ ] Implementar `metrics.py` com métricas atômicas.
- [ ] Implementar `detection.py` com score composto.
- [ ] Experimento `detection_demo.py`.
- [ ] Notebook `04_detection_metrics.ipynb`.

---

## Versão 0.5 – Visualização avançada

- [ ] Funções de animação em `animation.py`.
- [ ] (Opcional) Início de um dashboard `streamlit` em `app.py`.

---

## Ideias futuras

- Simular **múltiplos ativos**.
- Adicionar diferentes tipos de traders:
  - market makers,
  - trend followers,
  - fundamentalistas.
- Simular um **order book contínuo** (alta frequência).
- Integrar modelos de IA:
  - agentes de RL que tentam explorar a estrutura do mercado.
- Conectar com dados reais para:
  - calibrar parâmetros,
  - comparar simulações com séries reais.
