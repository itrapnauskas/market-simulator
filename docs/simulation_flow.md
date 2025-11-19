# Fluxo da Simulação

Este documento descreve, passo a passo, como a simulação é executada.

---

## 1. Inicialização

### 1.1. Configuração do mercado

Criar um objeto de configuração, por exemplo:

- `n_traders` – número de traders aleatórios.
- `initial_price` – preço inicial do ativo.
- `price_volatility` – desvio-padrão das distribuições de preços de ordem.
- `wealth_mode` – `"unlimited"` ou `"limited"`.
- `sentiment_mode` – `"none"` ou `"external_curve"`.
- `has_manipulator` – `True`/`False`.

### 1.2. Criação dos traders

- Se `wealth_mode = "unlimited"`:
  - instanciar `RandomTrader` sem restrições de riqueza.
- Se `wealth_mode = "limited"`:
  - instanciar `WealthLimitedTrader` com:
    - riqueza inicial,
    - holdings iniciais.

### 1.3. Criação do manipulador (opcional)

- Instanciar `Manipulator` com:
  - capital inicial,
  - estratégia (ex.: modo `"pump_and_dump"`).

---

## 2. Loop diário (para cada dia t)

Para `t = 1 ... n_days`:

### 2.1. Calcular sentimento (se aplicável)

- Consultar `sentiment(t)` se `sentiment_mode != "none"`.
- Ajustar, conforme necessário:
  - centro das distribuições de preço dos traders,
  - dispersão, se desejado.

### 2.2. Geração de ordens pelos traders

Para cada trader:

1. Decidir se participa ou não no dia (probabilidade de inatividade).
2. Se participa:
   - sorteia um preço de ordem em torno do preço do dia anterior:
     - ex.: `N(price_{t-1} + ajuste_sentimento, sigma)`,
   - sorteia um volume:
     - ex.: uniforme em `[0, max_volume]`,
     - se wealth-limited:
       - volume máximo = `wealth / price_max`.

3. Gera um objeto `Order`:
   - tipo: compra ou venda (probabilidade 50/50, ou outra regra),
   - preço limite,
   - volume.

Resultado: uma lista de ordens de compra e outra de ordens de venda.

### 2.3. Ação do manipulador (se presente)

Dependendo da fase do manipulador conforme a estratégia:

- **Fase de acumulação**:
  - gera ordens de compra discretas, sem chamar atenção.

- **Fase de pump**:
  - injeta ordens de self-trading (compra e venda ao mesmo preço),
  - possivelmente deslocando as curvas.

- **Fase de dump**:
  - injeta grandes ordens de venda para realizar lucro.

Todas essas ordens entram na mesma lista de ordens do mercado.

---

## 3. Formação das curvas de oferta e demanda

A partir das listas de ordens:

1. Para a curva de compra:
   - ordenar ordens por preço decrescente;
   - construir uma curva acumulada de volume demandado em função do preço.

2. Para a curva de venda:
   - ordenar ordens por preço crescente;
   - construir curva acumulada de volume ofertado.

Essas curvas podem ser representadas como:

- arrays discretizados em uma grade de preços,
- ou histogramas/pontos com interpolação.

---

## 4. Determinação do preço e volume do dia (auction pricing)

Dados:

- curva de demanda: `D(p)` – volume comprado a preço `p` ou maior;
- curva de oferta: `S(p)` – volume vendido a preço `p` ou menor.

Procurar o(s) preço(s) onde:

- a interseção das curvas gera o volume máximo negociável,
- ou, mais formalmente, o preço que maximiza uma função de:

  `satisfacao(p) = min(D(p), S(p))`

Em caso de intervalo de preços que maximizam `satisfacao(p)`:

- escolher o preço médio do intervalo,
- ou outro critério simples.

Resultado:

- `price_t` – preço de mercado do dia t,
- `volume_t` – volume negociado.

---

## 5. Atualização de estados

### 5.1. Traders

Para cada ordem que foi executada:

- Atualizar:
  - riqueza (dinheiro),
  - quantidade de ações.

### 5.2. Manipulador

Da mesma forma:

- atualizar riqueza e holdings,
- registrar lucros/perdas,
- registrar em qual fase da estratégia está.

### 5.3. Estado do mercado

Registrar em `MarketState`:

- `price_t`,
- `volume_t`,
- `sentiment_t` (se houver),
- quaisquer métricas agregadas desejadas:
  - número de ordens ativas,
  - espalhamento das curvas,
  - score de manipulação (se for calculado nesse passo).

---

## 6. Métricas de manipulação

Após atualizar o estado do dia:

- Passar curvas de ordens e/ou séries do dia em funções de detecção:

  - ex.: `manipulation_score_t = compute_manipulation_score(order_curves_t, reference_envelope)`

- Armazenar essa métrica para análise posterior.

---

## 7. Saída da simulação

Ao final de `n_days`, o simulador deve ter:

- uma lista/array de `MarketState` (um por dia),
- métricas de manipulação por dia,
- histórico de riqueza do manipulador,
- histórico de riqueza média dos demais traders.

Esses dados são então utilizados por:

- `viz/plots.py` para gerar gráficos,
- `notebooks/` para exploração e comentários.
