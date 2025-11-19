# Market Manipulation Lab - Premium Dashboard

Interactive dashboard completamente redesenhado com foco em UX e visualizações profissionais.

## Features Principais

### 1. Layout e Design Profissional
- **Custom Dark Theme**: Paleta de cores profissional com esquema cyan/coral
- **Sidebar Organizado**: Configuração intuitiva com presets e controles avançados
- **6 Tabs Especializadas**: Overview, Advanced Charts, Detection, Order Book, Compare, Data & Export
- **Responsive Design**: Layout adaptável e elegante
- **Loading States Elegantes**: Progress bars e animações durante simulações

### 2. Features Avançadas

#### Presets de Configuração
- Quick Start, Pump & Dump Demo, Small/Large Market, Extreme Manipulation, Random Walk

#### Save/Load Configurações
- Salvar/carregar configurações personalizadas
- Export/import em JSON

#### Export Multi-Formato
- CSV, JSON, Config JSON
- Download com um clique

#### Comparação de Simulações
- Múltiplas simulações lado a lado
- Tabela comparativa de métricas

### 3. Visualizações Interativas (Plotly)

- **Candlestick Charts**: Com janelas configuráveis
- **Price & Volume Dual-Axis**: Gráfico combinado
- **Order Book Visualization**: Curvas de oferta/demanda animadas
- **Manipulation Heatmap**: Padrões de trading
- **Anomaly Timeline**: Detecção visual de eventos
- **Distribution Charts**: Histogramas interativos
- **Comparison Charts**: Multi-simulação overlay

### 4. UX Enhancements

- **Welcome Screen**: Para novos usuários
- **Tutorial Mode Interativo**: 6 passos guiados
- **Help Sidebar**: 6 tópicos de ajuda contextual
- **Tooltips**: Em todos os controles importantes
- **Error Handling User-Friendly**: Mensagens claras e troubleshooting
- **Empty States**: Calls-to-action quando não há dados

### 5. Arquitetura Modular

```
dashboard/
├── app.py                    # Aplicação principal
└── components/
    ├── __init__.py          # Public exports
    ├── theme.py             # Cores, CSS, templates Plotly
    ├── charts.py            # 8 tipos de charts Plotly
    ├── config.py            # Presets, UI, save/load
    ├── utils.py             # Export, métricas, tabelas
    └── layout.py            # Header, footer, help, tutorial
```

## Instalação e Uso

### Dependências

```bash
# Instalar dependências do dashboard
pip install plotly streamlit pandas numpy

# Ou via pyproject.toml
pip install -e ".[viz]"
pip install streamlit plotly
```

### Executar Dashboard

```bash
# A partir da raiz do projeto
streamlit run dashboard/app.py

# Com porta customizada
streamlit run dashboard/app.py --server.port 8501
```

O dashboard abrirá em http://localhost:8501

### Primeiro Uso

1. Welcome screen será exibida
2. Escolha "Start Tutorial" ou "Skip to Dashboard"
3. Selecione preset (ex: "Pump & Dump Demo")
4. Click "🚀 Run Simulation"
5. Explore as 6 tabs!

## Tabs Overview

### 📊 Overview
- 8 metric cards (Days, Price Change, Volume, Volatility, etc)
- Price & Volume dual-axis chart
- Distribution histograms

### 📈 Advanced Charts
- Selector para 4 tipos de visualização
- Candlestick, Heatmap, Wealth Comparison, Anomaly Timeline
- Controles interativos

### 🔍 Detection
- Métricas de alerta (High/Medium/Avg/Max)
- Anomaly timeline com marcadores
- Metodologia explicada

### 📚 Order Book
- Slider para selecionar dia
- Curvas de oferta/demanda
- Estatísticas do dia + alerts

### 🔄 Compare
- Gráfico multi-simulação
- Tabela comparativa
- Suporte ilimitado de comparações

### 📥 Data & Export
- Botões: CSV, JSON, Config
- Tabela interativa
- Summary statistics

## Workflow Recomendado

1. **Configure**: Preset ou manual
2. **Run**: Execute simulação
3. **Explore**: Navegue pelas tabs
4. **Compare**: Adicione à comparação, varie parâmetros
5. **Export**: Download para análise

## Technical Highlights

- **Plotly Charts**: Totalmente interativos (zoom, pan, hover)
- **Session State**: Persistência de dados e configs
- **Performance**: Lazy loading, progress tracking
- **Modular**: Componentes reutilizáveis e testáveis
- **Professional Theme**: Dark mode com cores consistentes

## User Flow

```
Welcome → Configure → Run → Explore → Compare → Export
         ↑___________________________________|
```

## Screenshots Layout

```
┌──────────────────────────────────────────────────────────┐
│ SIDEBAR              │ MAIN CONTENT                      │
├──────────────────────────────────────────────────────────┤
│ Presets             │ Header + Help Button              │
│ Basic Config        │ Tutorial (optional)               │
│ Manipulator         │                                    │
│ Advanced            │ Tabs: Overview | Charts | ...     │
│                     │                                    │
│ Save/Load           │ Metrics Cards (8)                 │
│ Compare             │ Interactive Plotly Charts         │
│                     │ Info Boxes & Tips                 │
│ [🚀 Run]            │                                    │
│                     │ Footer                            │
└──────────────────────────────────────────────────────────┘
```

## Melhorias vs Versão Anterior

✅ Matplotlib → Plotly (interativo!)
✅ 2 charts → 8+ visualizações avançadas
✅ Config manual → 6 presets + manual
✅ Sem export → CSV/JSON/Config download
✅ Single view → 6 tabs organizadas
✅ Sem detecção → Detection tab com anomaly scores
✅ Sem help → Tutorial + Help sidebar completo
✅ Basic metrics → 8 metric cards detalhadas
✅ Sem comparação → Multi-sim comparison mode
✅ Sem theme → Professional dark theme customizado

## Roadmap Futuro

- Real-time streaming updates
- Animated order book evolution
- Network graph (collusion detection)
- ML-based advanced detection
- Theme toggle (dark/light)
- URL-based config sharing
- Internacionalização (EN/PT)
- Mobile-responsive design

---

**Educational Purpose Only**
Este dashboard é para fins educacionais e pesquisa.
Não constitui aconselhamento financeiro.
