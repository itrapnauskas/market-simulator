# Market Manipulation Strategies

Este documento descreve as 3 novas estratégias de manipulação de mercado implementadas para o Market Manipulation Lab.

## Visão Geral

Todas as estratégias herdam de `WealthLimitedTrader` e implementam o método `maybe_generate_order()` para gerar ordens de acordo com suas táticas específicas de manipulação.

---

## 1. SpoofingManipulator

**Arquivo:** `src/market_lab/manipulation/spoofing.py`

### Descrição

Spoofing é uma técnica de manipulação onde o trader coloca ordens grandes (spoof orders) para criar a falsa impressão de pressão de compra ou venda, influenciando o comportamento de outros traders e o preço do mercado. Essas ordens são canceladas antes de serem executadas.

### Estratégia

1. **Spoof Orders**: Coloca ordens grandes em um lado do book (compra ou venda) para criar ilusão de pressão
2. **Genuine Orders**: Coloca ordens menores no lado oposto para lucrar com o movimento de preço causado
3. **Cancellation**: Remove (simula cancelamento) das spoof orders antes da execução

### Parâmetros Configuráveis

```python
SpoofingManipulator(
    trader_id="spoofer_001",
    rng=Random(42),
    wealth=100_000.0,          # Capital inicial
    holdings=50.0,             # Holdings iniciais
    spoof_multiplier=8.0,      # Ordens spoof são 8x maiores
    spoof_probability=0.4,     # 40% chance de criar spoof
    price_offset=0.03,         # 3% de offset do preço de mercado
    cancel_threshold=1,        # Cancela após 1 dia
    target_side="buy"          # Foca em spoofing de compra
)
```

### Parâmetros

- **spoof_multiplier** (default: 5.0): Multiplicador de tamanho para ordens spoof
- **spoof_probability** (default: 0.3): Probabilidade de criar spoof order
- **price_offset** (default: 0.02): Offset de preço como fração (2%)
- **cancel_threshold** (default: 1): Dias antes de cancelar spoof orders
- **target_side** (default: "random"): Lado preferencial ("buy", "sell", "random")

### Características

- Ordens spoof criam percepção de suporte/resistência
- Ordens genuínas menores capturam lucro no lado oposto
- Spoof orders são rastreadas e "canceladas" após threshold
- Detectabilidade: **Média** (cancelamentos visíveis)

---

## 2. WashTradingManipulator

**Arquivo:** `src/market_lab/manipulation/wash_trading.py`

### Descrição

Wash trading é uma forma de manipulação onde o trader compra e vende simultaneamente o mesmo ativo, criando volume artificial sem alterar sua posição líquida. Isso dá a falsa impressão de alta liquidez e interesse no mercado.

### Estratégia

1. **Paired Orders**: Gera pares de ordens de compra/venda com preços similares
2. **Artificial Volume**: Cria volume sem mudança líquida de posição
3. **Neutral Position**: Mantém holdings aproximadamente neutros ao longo do tempo
4. **Tight Spreads**: Usa spreads pequenos para garantir execução de ambas ordens

### Parâmetros Configuráveis

```python
WashTradingManipulator(
    trader_id="washer_001",
    rng=Random(123),
    wealth=150_000.0,
    holdings=100.0,
    wash_probability=0.6,       # 60% chance de wash trade
    volume_multiplier=4.0,      # Wash trades são 4x maiores
    price_spread=0.0005,        # 0.05% spread entre buy/sell
    pairs_per_session=3,        # 3 pares por sessão
    randomize_timing=True,      # Randomiza timing das ordens
    max_position_drift=0.1      # Permite 10% de drift
)
```

### Parâmetros

- **wash_probability** (default: 0.5): Probabilidade de gerar wash trades
- **volume_multiplier** (default: 3.0): Multiplicador de volume para wash trades
- **price_spread** (default: 0.001): Spread entre buy/sell como fração (0.1%)
- **pairs_per_session** (default: 2): Número de pares buy/sell por sessão
- **randomize_timing** (default: True): Randomiza timing das ordens nos pares
- **max_position_drift** (default: 0.1): Drift máximo permitido (10%)

### Características

- Pares de ordens buy/sell com spreads apertados
- Cria volume artificial sem alterar posição
- Rebalanceamento periódico para manter holdings neutros
- Detectabilidade: **Baixa** (parece trading normal)

---

## 3. LayeringManipulator

**Arquivo:** `src/market_lab/manipulation/layering.py`

### Descrição

Layering (também conhecido como quote stuffing) é uma técnica sofisticada onde o trader coloca múltiplas ordens limit em diferentes níveis de preço (camadas) em um lado do order book para criar a ilusão de forte suporte ou resistência. Essa falsa liquidez influencia a percepção e decisões de outros traders.

### Estratégia

Opera em 4 fases cíclicas:

1. **BUILD**: Cria múltiplas camadas de ordens em níveis de preço incrementais
2. **MAINTAIN**: Mantém as camadas ativas para influenciar percepção do mercado
3. **REMOVE**: Cancela sistematicamente as camadas antes da execução
4. **PROFIT**: Executa ordens genuínas no lado oposto a preços favoráveis

### Parâmetros Configuráveis

```python
LayeringManipulator(
    trader_id="layer_001",
    rng=Random(456),
    wealth=200_000.0,
    holdings=150.0,
    n_layers=7,                 # 7 camadas de preço
    layer_spacing=0.003,        # 0.3% entre camadas
    volume_decay=0.75,          # Cada camada é 75% da anterior
    layer_probability=0.7,      # 70% chance de adicionar layers
    removal_rate=0.3,           # 30% chance de remover layer
    phase_duration=10,          # 10 turns por fase
    target_side="sell",         # Foca em layering de venda
    base_volume_multiplier=4.0  # Volume base 4x maior
)
```

### Parâmetros

- **n_layers** (default: 5): Número de camadas de preço a criar
- **layer_spacing** (default: 0.005): Espaçamento entre camadas (0.5%)
- **volume_decay** (default: 0.8): Fator de redução de volume por camada (80%)
- **layer_probability** (default: 0.6): Probabilidade de adicionar/manter layers
- **removal_rate** (default: 0.3): Probabilidade de remover layer na fase de remoção
- **phase_duration** (default: 10): Número de turns por fase
- **target_side** (default: "random"): Lado para layering ("buy", "sell", "random")
- **base_volume_multiplier** (default: 4.0): Multiplicador de volume da camada base

### Características

- Múltiplas camadas criam ilusão de liquidez profunda
- Camadas são progressivamente removidas antes de execução
- Ordens genuínas de lucro no lado oposto
- Cicla através das fases build/maintain/remove/profit
- Detectabilidade: **Alta** (padrão distintivo)

---

## Comparação das Estratégias

| Estratégia | Objetivo | Mecanismo | Detectabilidade | Impacto no Mercado |
|-----------|----------|-----------|----------------|-------------------|
| **Spoofing** | Criar falsos sinais de preço | Ordens grandes que são rapidamente canceladas | Média | Distorção de preço de curto prazo |
| **Wash Trading** | Inflar volume de trading | Pares simultâneos de buy/sell | Baixa | Volume artificial, impacto mínimo no preço |
| **Layering** | Criar falsa impressão de liquidez | Múltiplas camadas de ordens em níveis de preço | Alta | Ilusão de liquidez de médio prazo |

---

## Exemplo de Uso

```python
from random import Random
from market_lab.core.market import MarketConfig
from market_lab.manipulation import (
    SpoofingManipulator,
    WashTradingManipulator,
    LayeringManipulator,
)

# Configuração do mercado
config = MarketConfig(
    n_traders=100,
    initial_price=100.0,
    price_volatility=2.0,
    max_daily_volume=10.0,
    price_tick=0.01,
)

# Criar manipuladores
spoofer = SpoofingManipulator(
    trader_id="spoof_001",
    rng=Random(42),
    wealth=100_000.0,
    holdings=50.0,
    spoof_multiplier=8.0,
    target_side="buy"
)

washer = WashTradingManipulator(
    trader_id="wash_001",
    rng=Random(123),
    wealth=150_000.0,
    holdings=100.0,
    wash_probability=0.6
)

layerer = LayeringManipulator(
    trader_id="layer_001",
    rng=Random(456),
    wealth=200_000.0,
    holdings=150.0,
    n_layers=7,
    target_side="sell"
)

# Gerar ordens
order1 = spoofer.maybe_generate_order(
    last_price=100.0,
    sentiment_value=0.5,
    config=config
)

order2 = washer.maybe_generate_order(
    last_price=100.0,
    sentiment_value=0.0,
    config=config
)

order3 = layerer.maybe_generate_order(
    last_price=100.0,
    sentiment_value=0.0,
    config=config
)
```

Para um exemplo completo e executável, veja `examples/manipulation_strategies.py`.

---

## Notas de Implementação

### Herança e Design

Todas as estratégias:
- Herdam de `WealthLimitedTrader`
- Respeitam restrições de capital (`wealth`) e holdings
- Implementam `maybe_generate_order()` para lógica customizada
- Usam `apply_fill()` herdado para atualizar estado após execução

### Limitações

- As estratégias respeitam `max_daily_volume` da configuração
- Ordens de compra são limitadas pela wealth disponível
- Ordens de venda são limitadas pelos holdings disponíveis
- Todos os preços respeitam o `price_tick` mínimo

### Estado Interno

Cada estratégia mantém estado interno para:
- **Spoofing**: Rastreia spoof orders ativas e dia de criação
- **Wash Trading**: Rastreia pares pendentes e holdings iniciais
- **Layering**: Rastreia fase atual, camadas ativas e contador de ciclo

---

## Arquivos Criados

1. `/home/user/market-simulator/src/market_lab/manipulation/spoofing.py`
2. `/home/user/market-simulator/src/market_lab/manipulation/wash_trading.py`
3. `/home/user/market-simulator/src/market_lab/manipulation/layering.py`
4. `/home/user/market-simulator/src/market_lab/manipulation/__init__.py` (atualizado)
5. `/home/user/market-simulator/examples/manipulation_strategies.py`

---

## Referências

Estas implementações são para fins educacionais e de pesquisa no contexto do Market Manipulation Lab. Todas as estratégias descritas são ilegais em mercados reais e são apresentadas aqui apenas para estudo de detecção e análise de padrões de manipulação.
