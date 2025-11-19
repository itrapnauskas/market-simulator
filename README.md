# Market Manipulation Lab

Simulador educacional e experimental de **microestrutura de mercado** e **manipulação baseada em ordens**.

Este repositório implementa, em Python, um laboratório para explorar:

- Como mercados “justos” geram **random walks gaussianos**.
- Como **restrições de riqueza** e regras de negociação geram **bandas de preço** e “gravidade” em torno de um centro.
- Como **manipuladores** podem distorcer preço e volume usando:
  - self-trading / wash-trading,
  - price-setting via ordens grandes,
  - ciclos de pump-and-dump.
- Como técnicas de **análise forense** podem ajudar a detectar manipulação olhando para:
  - formato das curvas de oferta/demanda,
  - volume e saltos de preço,
  - padrões repetidos de comportamento.

O foco não é prever mercado real, e sim **entender mecanismos**.

---

## Objetivos do projeto

1. **Criar um simulador de mercado simples, mas expressivo**, baseado em:
   - traders aleatórios,
   - regras claras de formação de preço (auction pricing),
   - restrições realistas (riqueza limitada, volume, etc.).

2. **Modelar manipuladores de mercado**:
   - mostrar, passo a passo, como estratégias de pump-and-dump podem surgir;
   - como é possível “comprar o mercado” e se tornar price setter em mercados pequenos.

3. **Construir ferramentas de visualização**:
   - séries de preço e volume,
   - gráficos de curvas de ordens,
   - métricas de manipulação ao longo do tempo.

4. **Servir como base para pesquisa, ensino e experimentação**:
   - aulas de finanças, microestrutura, economia comportamental,
   - artigos ou relatórios técnicos sobre manipulação por ordens.

---

## Escopo (v1)

A versão inicial do projeto (MVP) cobre:

- Mercado discreto em **passos diários**.
- Um único ativo.
- Preço de cada dia definido por **leilão único** (auction pricing).
- Traders aleatórios:
  - geram ordens de compra/venda a partir de distribuições de preço.
- Dois modos de mercado:
  - **Random Walk Gaussiano** (riqueza ilimitada).
  - **Wealth-Limited** (traders com dinheiro finito, gerando bandas de preço).
- Um manipulador simples:
  - compra gradualmente, manipula via self-trading e price-setting,
  - vende no topo (pump-and-dump grosseiro).
- Visualização básica:
  - preço × tempo,
  - volume × tempo,
  - riqueza do manipulador vs demais,
  - marcações de dias com manipulação.

---

## Organização do projeto

Estrutura sugerida:

```text
market-manipulation-lab/
├── README.md
├── pyproject.toml / requirements.txt
├── src/
│   └── market_lab/
│       ├── __init__.py
│       ├── core/
│       │   ├── market.py        # Engine de preço e volume
│       │   ├── traders.py       # Traders aleatórios e wealth-limited
│       │   ├── orders.py        # Estruturas de ordem e curvas agregadas
│       │   ├── sentiment.py     # Eventos de notícia / sentimento
│       │   └── simulation.py    # Loop de simulação de múltiplos dias
│       ├── manipulation/
│       │   ├── manipulator.py   # Estratégias de manipulação
│       │   ├── detection.py     # Métricas e detecção de padrões
│       │   └── metrics.py       # Funções de score quantitativo
│       ├── viz/
│       │   ├── plots.py         # Gráficos estáticos (matplotlib/plotly)
│       │   └── animation.py     # Animações simples opcionais
│       └── experiments/
│           ├── random_walk.py
│           ├── wealth_limits.py
│           ├── sentiment_shock.py
│           └── pump_and_dump.py
├── notebooks/
│   ├── 01_random_market.ipynb
│   ├── 02_wealth_limits.ipynb
│   ├── 03_manipulation_cycle.ipynb
│   └── 04_detection_metrics.ipynb
└── docs/
    ├── overview.md
    ├── theory.md
    ├── architecture.md
    ├── simulation_flow.md
    ├── modules_core.md
    ├── modules_manipulation.md
    ├── modules_viz.md
    └── roadmap.md
```

Cada módulo tem um papel **atômico**:

* `core/` → regras “justas” do mercado.
* `manipulation/` → tudo que quebra a justiça.
* `viz/` → tudo que mostra o que está acontecendo.
* `experiments/` → scripts de cenário, combinando peças do core + manipulation.
* `notebooks/` → exploração interativa e documentação viva.

---

## Tecnologias sugeridas

* **Linguagem:** Python 3.11+
* **Dependências mínimas (MVP):**

  * `numpy`
  * `pandas`
  * `matplotlib` ou `plotly`
  * (opcional) `scipy` para métricas mais avançadas
  * (opcional) `jupyter` para notebooks
* **Futuro:**

  * `streamlit` para dashboard interativo
  * `manim` ou `matplotlib.animation` para vídeos/animações

---

## Como começar (MVP)

1. Criar ambiente virtual e instalar dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate

   pip install -r requirements.txt
   ```

2. Rodar o primeiro experimento de mercado justo:

   ```bash
   python -m market_lab.experiments.random_walk
   ```

3. Abrir os notebooks:

   ```bash
   jupyter lab
   ```

   E abrir `notebooks/01_random_market.ipynb`.

---

## Filosofia do projeto

* **Didático primeiro, hardcore depois.**
* Cada arquivo deve ter **responsabilidade pequena e clara**.
* Códigos e funções sempre com:

  * docstrings em português,
  * exemplos de uso quando fizer sentido,
  * comentários explicando a intuição (não só a matemática).

---

## Aviso legal

Este projeto:

* é **apenas para fins educacionais e de pesquisa**;
* **não** é uma ferramenta de trading;
* **não** é recomendação de investimento.

Use os resultados com senso crítico.
Mercados reais são muito mais complexos — aqui focamos em **mecanismos**, não em edge real.
