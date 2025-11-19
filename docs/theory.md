# Fundamentos Teóricos

Este documento descreve a intuição e a teoria básica usada no simulador.

---

## 1. Random Walk Gaussiano

Quando traders agem de forma independente, com expectativas distribuídas simetricamente em torno do preço anterior, e **não há restrição de riqueza**, o movimento do preço tende a:

- ser “sem memória” de longo prazo (cada dia é quase independente),
- ter variações diárias distribuídas aproximadamente de forma normal (gaussiana),
- apresentar **random walk gaussiano**:
  - o preço segue um passeio aleatório com passos ~N(0, σ²).

No simulador:

- Compradores e vendedores sorteiam seus preços de ordem a partir de uma distribuição normal em torno do preço de ontem.
- A interseção dessas curvas define o preço de hoje.
- Como não há limite de quanto podem comprar/vender, a forma das curvas não muda com o nível absoluto do preço.

---

## 2. Auction Pricing

Em vez de simular um book contínuo de ordens, o simulador usa um **leilão de preço único por dia**.

Ideia:

1. Coletar todas as ordens de compra:
   - cada ordem tem:
     - preço máximo aceito (willingness to pay),
     - volume desejado.

2. Coletar todas as ordens de venda:
   - cada ordem tem:
     - preço mínimo aceito (willingness to accept),
     - volume disponível.

3. Construir curvas agregadas:
   - curva de demanda (compras) como função do preço;
   - curva de oferta (vendas) como função do preço.

4. Definir o preço de mercado como aquele que:
   - maximiza o volume trocado
   - ou, de forma equivalente, maximiza uma função de “satisfação” (quantos querem/aceitam negociar naquele preço).

Na prática:

- Há um intervalo de preços possíveis que produzem o mesmo volume máximo.
- O simulador escolhe um critério simples (ex.: preço médio do intervalo).

Isso imita o processo de abertura de mercado em muitas bolsas.

---

## 3. Wealth-Limited e “Gravidade” de Preço

Quando traders têm riqueza limitada:

- Não podem comprar volume arbitrário a preços altos.
- A curva de demanda começa a **encolher** à medida que o preço sobe:
  - cada trader tem menos unidades que consegue comprar.

Já a curva de oferta:

- Pode continuar oferecendo volumes a preços altos (wishful thinking),
- Não sofre restrição tão rápida do lado do vendedor.

Resultado:

- Surge uma **assimetria**:
  - a demanda cai mais rápido do que a oferta à medida que o preço se afasta de um centro.
- Há uma espécie de “puxão” de volta em direção ao preço médio histórico.

Consequência:

- O preço ainda flutua de forma randômica,
- Mas passa a **orbitar** dentro de um canal/banda,
- Preços muito altos ou muito baixos tornam-se **cada vez menos prováveis**.

Essa “gravidade” não é imposta por nenhuma regra explícita de “limite de banda”:
- é consequência das regras de riqueza + forma de geração de ordens.

---

## 4. Manipuladores: Price Takers vs Price Setters

Traders comuns são **price takers**:

- Observam o preço,
- Decidem comprar/vender,
- Mas não mudam significativamente a forma das curvas de oferta/demanda.

Um manipulador com muito capital pode se tornar **price setter**:

- Colocando ordens grandes o suficiente para:
  - distorcer as curvas,
  - deslocar a interseção (preço de equilíbrio),
  - ou simular volume alto via self-trading.

---

## 5. Self-Trading / Wash Trading

**Self-trading**:

- Quando o mesmo participante:
  - envia uma ordem de compra e uma de venda,
  - que se cruzam entre si,
  - via exchange/broker.

A troca é, na essência, entre “bolso esquerdo” e “bolso direito”.

Efeitos:

- Gera volume aparente,
- Pode dar impressão de liquidez alta,
- Pode “empurrar” o preço dependendo de como as ordens se encaixam.

Em muitos mercados, práticas específicas de self-trading são ilegais (wash trading), justamente porque:

- distorcem sinais de preço e volume,
- confundem outros participantes.

---

## 6. Pump-and-Dump

Esquema clássico de manipulação:

1. **Acumulação**:
   - o manipulador compra aos poucos, sem chamar atenção.

2. **Pump**:
   - eleva o preço:
     - via nova rodada de compras,
     - via self-trading em preços mais altos,
     - criando ilusão de interesse genuíno.

3. **Dump**:
   - vende os ativos a preços inflados,
   - deixando os demais segurando o “mico”.

No simulador:

- Medimos o efeito:
  - na riqueza do manipulador,
  - na riqueza média dos traders aleatórios,
  - na forma das curvas de ordens.

---

## 7. Detecção de Manipulação

Algumas ideias de métricas que o projeto pretende implementar:

- Desvio das curvas de oferta/demanda em relação a um “envelope” de referência:
  - baseado em simulações sem manipulação.
- Mudanças abruptas de volume não acompanhadas por mudança de sentimento (no modo com “sentiment curve”).
- Repetição de padrões de:
  - grandes ordens de compra e venda em preços muito próximos,
  - concentração anormal de volume em torno de um participante (em versões futuras, com identificação de agentes).

Essas métricas **não são prova** de fraude, mas indicadores:

- ajudam a priorizar dias/períodos para inspeção mais profunda,
- simulam o trabalho de uma equipe de compliance / regulação.
