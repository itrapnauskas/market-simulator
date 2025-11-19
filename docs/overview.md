# Visão Geral do Market Manipulation Lab

## Motivação

Este projeto nasce da vontade de entender, com as mãos no código, perguntas do tipo:

- Como um mercado “justo” se parece quando ninguém tem informação privilegiada?
- O que acontece quando adicionamos **limites de riqueza**?
- De onde surgem canais de preço, bandas e “gravidade” em torno de certos níveis?
- Como um agente com muito capital pode:
  - distorcer preço e volume,
  - ganhar dos demais traders sistematicamente,
  - e ainda parecer “só mais um” no meio do fluxo?

Ao invés de discutir isso só na teoria, este laboratório constrói um **mercado sintético** onde:

- as regras são explícitas;
- a microestrutura é controlável;
- e tudo pode ser instrumentado, medido e visualizado.

---

## Ideia central

O projeto implementa:

1. Um **mercado de referência “justo”**:
   - tempo discreto (dias),
   - um único ativo,
   - traders aleatórios,
   - preço definido por um leilão único (“auction pricing”),
   - dois regimes:
     - random walk gaussiano,
     - wealth-limited com bandas de preço emergentes.

2. Um **módulo de manipulação**:
   - agentes que não são apenas “price takers”, mas “price setters”;
   - conseguem influenciar:
     - o formato das curvas de demanda/oferta,
     - o preço de equilíbrio resultante,
     - o volume aparente.

3. Um **módulo de detecção**:
   - comparação entre simulações com e sem manipulação;
   - métricas que tentam quantificar “quão estranho” é o comportamento em um dado dia;
   - base para pensar como reguladores e exchanges podem detectar fraude.

4. **Ferramentas de visualização e experimentação**:
   - scripts de experimentos reproduzíveis (`experiments/`);
   - notebooks interativos com gráficos e comentários (`notebooks/`).

---

## Formas de uso

### Como laboratório pessoal

- Rodar os scripts de experimentos.
- Tunar parâmetros (número de traders, variância das distribuições, tamanho do manipulador).
- Ver o que acontece com:
  - série de preços,
  - volatilidade,
  - riqueza do manipulador.

### Como material didático

- Mostrar em sala de aula:
  - random walk gaussiano,
  - efeito de limites de riqueza,
  - diferença entre “notícia real” e “volume fake”,
  - ciclo pump-and-dump.

- Pedir que alunos:
  - criem suas próprias estratégias de manipulação;
  - criem métricas de detecção;
  - comparem “mercado justo” vs “mercado manipulado”.

### Como base de pesquisa

- Implementar extensões:
  - múltiplos ativos;
  - diferentes tipos de traders (market makers, trend-followers, noise traders);
  - regras de margin call, alavancagem, short selling;
  - ligação com dados reais (para calibragem).

---

## Limitações assumidas (de propósito)

Para manter o projeto gerenciável e didático:

- Um único ativo no MVP.
- Sem order book de alta frequência (ticks) no núcleo inicial.
- Tempo discreto (um leilão por “dia”).
- Modelo de traders simplificado:
  - inicialmente sem aprendizado,
  - comportamento randômico + restrições básicas.

Essas simplificações não são defeito: elas tornam os **mecanismos visíveis**.

A partir desse núcleo, é possível avançar em direção a:

- simulação de book de ofertas contínuo,
- mercados multi-ativos,
- agentes com aprendizado (RL, heurísticas, etc.).
