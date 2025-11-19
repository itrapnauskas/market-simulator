# Arquitetura do Projeto

A arquitetura segue uma ideia de **módulos atômicos**, cada um com responsabilidade clara.

---

## Visão em camadas

1. **Core (núcleo de mercado justo)**  
   - Representa o funcionamento de um mercado sem manipulação.
   - Responsável por:
     - traders aleatórios,
     - geração de ordens,
     - formação de curvas de oferta/demanda,
     - cálculo de preço e volume por auction pricing,
     - loop de simulação.

2. **Manipulation (camada de distorção)**  
   - Camada que opera “por cima” do core.
   - Adiciona:
     - manipuladores,
     - estratégias de pump-and-dump,
     - self-trading,
     - price-setting,
     - métricas de detecção.

3. **Viz (visualização)**  
   - Traduz estados e resultados em gráficos e animações.
   - Não conhece detalhes internos de implementação:
     - recebe séries temporais, curvas e métricas já calculadas.

4. **Experiments (cenários)**  
   - Scripts autocontidos que:
     - configuram o mercado,
     - executam simulações para um cenário específico,
     - produzem saídas (gráficos, dados).

5. **Notebooks (interface de exploração)**  
   - Reutilizam as peças das camadas acima,
   - servem como:
     - documentação viva,
     - playground interativo.

---

## Estrutura de pastas (detalhada)

```text
src/market_lab/
├── core/
│   ├── market.py
│   ├── traders.py
│   ├── orders.py
│   ├── sentiment.py
│   └── simulation.py
├── manipulation/
│   ├── manipulator.py
│   ├── detection.py
│   └── metrics.py
├── viz/
│   ├── plots.py
│   └── animation.py
└── experiments/
    ├── random_walk.py
    ├── wealth_limits.py
    ├── sentiment_shock.py
    └── pump_and_dump.py
```

### `core/market.py`

Responsável por:

* Definir as estruturas de:

  * `MarketConfig` (parâmetros do mercado),
  * `MarketState` (estado em um dado dia),
* Implementar:

  * função para construir curvas agregadas a partir de ordens,
  * função para encontrar o preço de equilíbrio e volume.

### `core/traders.py`

Responsável por:

* Definir `Trader` (classe base) e variações:

  * `RandomTrader`,
  * `WealthLimitedTrader`.
* Cada trader sabe:

  * qual sua riqueza,
  * quantas ações possui,
  * como gerar uma ordem de compra/venda em um dia dado.

### `core/orders.py`

Responsável por:

* Estruturas de dados:

  * `Order` (compra ou venda),
  * coleções de ordens,
  * curvas agregadas (ex.: histogramas ou funções discretizadas).
* Pode incluir lógica de:

  * normalização de curvas,
  * conversão para arrays/vetores para análise.

### `core/sentiment.py`

Responsável por:

* Representar eventos externos (notícia boa/ruim),
* Fornecer uma função `sentiment(t)` que ajusta:

  * centro da distribuição de preços desejados,
  * ou a dispersão.

### `core/simulation.py`

Responsável por:

* Encapsular o loop de simulação:

  * inicializar traders,
  * iterar por `n_days`,
  * armazenar `MarketState` para cada dia.

---

### `manipulation/manipulator.py`

Responsável por:

* Definir a classe `Manipulator`:

  * com estado próprio (riqueza, ações, estratégia),
  * com métodos como:

    * `build_position()`,
    * `inject_self_trades()`,
    * `dump_position()`.
* Integrar o manipulador ao fluxo de ordens do mercado:

  * manipulador também gera ordens,
  * que entram junto com as ordens dos demais traders.

### `manipulation/detection.py`

Responsável por:

* Funções para avaliar:

  * curvas de oferta/demanda em um dia,
  * séries de preço e volume,
* Retornar métricas de “estranheza” ou score de manipulação.

### `manipulation/metrics.py`

Responsável por:

* Implementar métricas atômicas, por exemplo:

  * desvio em relação à média de referência,
  * distância KL entre curvas,
  * contagem de “dentes” abruptos nas curvas (discontinuidades suspeitas).

---

### `viz/plots.py`

Responsável por:

* Funções de alto nível como:

  * `plot_price_series(states)`,
  * `plot_volume_series(states)`,
  * `plot_order_curves(day_state)`,
  * `plot_manipulation_score(scores)`.

### `viz/animation.py`

Responsável por (opcional):

* Criar animações simples:

  * evolução diária das curvas,
  * highlight do manipulador.

---

### `experiments/`

Cada arquivo em `experiments/`:

* Representa um **cenário autocontido**.
* Exemplo: `random_walk.py`:

  * cria um `MarketConfig` para mercado justo;
  * inicializa traders aleatórios;
  * roda `SimulationRunner` (ou função equivalente);
  * salva resultados e plota usando `viz/plots.py`.

Isso mantém o núcleo da simulação limpo e testável, e os cenários como “camada de aplicação”.
