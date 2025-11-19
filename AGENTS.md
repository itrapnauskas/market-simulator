# 🏢 Sistema de Agentes Especializados

## Visão Geral

O **Sistema de Agentes Especializados** é uma fábrica autônoma de desenvolvimento e melhorias para o Market Manipulation Lab. Consiste em **13 agentes super especializados** que trabalham em conjunto, cada um com expertise específica, comunicando-se entre si para chegar em decisões e implementar melhorias de forma autônoma.

## 🎯 Filosofia

- **Especialização Máxima**: Cada agente é FODA na sua área específica
- **Autonomia**: Agentes tomam decisões dentro de sua expertise
- **Colaboração**: Comunicação entre agentes para decisões complexas
- **Pipeline Estruturado**: Discovery → Planning → Execution → Report
- **CEO como Ponto Único**: Apenas o CEO reporta para stakeholders externos

## 👥 Hierarquia Organizacional

```
                        ┌─────────┐
                        │   CEO   │  ← Único ponto de contato externo
                        └────┬────┘
                             │
                ┌────────────┴────────────┐
                │                         │
            ┌───┴───┐                ┌───┴───────┐
            │  CTO  │                │ Product   │
            │       │                │ Manager   │
            └───┬───┘                └───┬───────┘
                │                        │
    ┌───────────┼──────────┐            │
    │           │          │            │
┌───┴───┐  ┌───┴───┐  ┌───┴────┐   ┌──┴────┐
│ Tech  │  │DevOps │  │   QA   │   │  UX   │
│ Lead  │  │       │  │        │   │Design │
└───┬───┘  └───────┘  └────────┘   └───────┘
    │
    ├──────────────────────────┐
    │           │              │
┌───┴────┐  ┌──┴───┐      ┌───┴────┐
│Backend │  │Front │      │ Data   │
│  Dev   │  │ end  │      │Science │
└────────┘  └──────┘      └────────┘

        Specialists (reportam ao CEO/CTO)
┌──────────┬────────────┬──────────────┐
│ Market   │    Doc     │    User      │
│Specialist│  Writer    │  Research    │
└──────────┴────────────┴──────────────┘
```

## 🤖 Agentes e Suas Responsabilidades

### C-Level

#### **CEO - Chief Executive Officer**
- **Expertise**: Strategic Vision, Stakeholder Management, Decision Making
- **Responsabilidades**:
  - Único ponto de contato com usuário/stakeholders
  - Aprovação de roadmap e decisões críticas
  - Resolução de conflitos entre departamentos
  - Coordenação geral da organização

#### **CTO - Chief Technology Officer**
- **Expertise**: System Architecture, Technology Stack, Code Standards, Security
- **Responsabilidades**:
  - Decisões técnicas e arquiteturais finais
  - Definição de padrões de código (ruff, mypy)
  - Escolha de tecnologias
  - Supervisão de Dev, QA, DevOps

### Management

#### **Product Manager**
- **Expertise**: Product Vision, Feature Prioritization, User Stories
- **Responsabilidades**:
  - Criar e manter roadmap de produto
  - Definir o que construir e por quê
  - Priorizar features baseado em valor
  - Ponte entre usuários e time técnico

#### **Tech Lead**
- **Expertise**: Code Architecture, Design Patterns, Code Review
- **Responsabilidades**:
  - Liderança técnica do dia-a-dia
  - Code review e qualidade de código
  - Mentoria técnica
  - Implementação de padrões definidos pelo CTO

### Design

#### **UX/UI Designer**
- **Expertise**: User Experience, Interface Design, Usability
- **Responsabilidades**:
  - Design de interfaces (dashboard, notebooks)
  - Wireframes e protótipos
  - Usability testing
  - Visual design

### Development

#### **Backend Developer**
- **Expertise**: Python Development, Algorithms, API Design
- **Responsabilidades**:
  - Implementação de lógica core
  - Algoritmos de simulação
  - Performance optimization
  - API design

#### **Frontend Developer**
- **Expertise**: Data Visualization, Streamlit, Matplotlib/Plotly
- **Responsabilidades**:
  - Visualizações interativas
  - Dashboard Streamlit
  - Notebooks Jupyter (parte visual)
  - UI implementation

#### **Data Scientist**
- **Expertise**: Statistical Analysis, Machine Learning, Anomaly Detection
- **Responsabilidades**:
  - Algoritmos de detecção de manipulação
  - Análises estatísticas
  - Machine learning models
  - Financial modeling

### Quality & Operations

#### **QA Engineer**
- **Expertise**: Test Automation, Pytest, Coverage Analysis
- **Responsabilidades**:
  - Test suite com pytest
  - Test design e coverage
  - Integration testing
  - Quality metrics

#### **DevOps Engineer**
- **Expertise**: CI/CD, GitHub Actions, Docker, Automation
- **Responsabilidades**:
  - GitHub Actions workflows
  - CI/CD pipelines
  - Deployment automation
  - Infrastructure as code

### Specialists

#### **Market Specialist**
- **Expertise**: Market Microstructure, Trading Strategies, Financial Theory
- **Responsabilidades**:
  - Validação de realismo das simulações
  - Expertise em manipulação de mercado
  - Sugestões de novas estratégias
  - Compliance com teoria financeira

#### **Documentation Writer**
- **Expertise**: Technical Writing, Tutorial Creation, API Documentation
- **Responsabilidades**:
  - Docstrings em código
  - Jupyter notebooks educacionais
  - API reference (Sphinx)
  - Tutoriais e guias

#### **User Researcher**
- **Expertise**: User Research, Usability Testing, User Personas
- **Responsabilidades**:
  - Criação de personas
  - User interviews
  - Analytics interpretation
  - Feedback collection

## 🔄 Pipeline de Trabalho

### Fase 1: Discovery
Todos os agentes analisam o estado atual do projeto em paralelo:
- CTO analisa arquitetura e tecnologias
- Product Manager identifica feature gaps
- QA Engineer avalia test coverage
- UX Designer analisa usabilidade
- Market Specialist valida realismo
- Etc.

### Fase 2: Planning
Baseado na discovery, os agentes planejam:
- Product Manager cria roadmap
- CTO define padrões técnicos
- UX Designer cria wireframes
- User Researcher cria personas
- CEO aprova o roadmap

### Fase 3: Execution
Agentes implementam as melhorias:
- DevOps configura CI/CD
- QA cria test suite
- Doc Writer adiciona docstrings
- Backend Dev implementa features
- Frontend Dev cria dashboard
- Data Scientist melhora algoritmos

### Fase 4: Report
CEO compila e reporta resultados para stakeholder externo.

## 💬 Sistema de Comunicação

### CommunicationBus
Sistema centralizado de mensagens entre agentes:
- **Mensagens direcionadas**: Agente → Agente específico
- **Broadcast**: Agente → Todos
- **Prioridades**: LOW, MEDIUM, HIGH, CRITICAL
- **Contexto**: Dados adicionais anexados a mensagens
- **Response tracking**: Sistema de requires_response

### Exemplo de Comunicação
```python
# Product Manager envia roadmap para CEO aprovar
product_manager.communicate(
    receiver=AgentRole.CEO,
    content="Product roadmap ready for approval",
    context={"roadmap": roadmap},
    priority=MessagePriority.HIGH,
    requires_response=True
)

# CEO aprova e faz broadcast
ceo.communicate(
    receiver=None,  # Broadcast
    content="Roadmap approved. All teams: execute with excellence!",
    priority=MessagePriority.HIGH
)
```

## 🚀 Como Usar

### Demo Rápida
```bash
python run_agents.py --demo
```

Mostra todos os agentes disponíveis e suas responsabilidades.

### Relatório de Análise
```bash
python run_agents.py --report
```

Executa apenas a fase de Discovery e mostra insights de cada agente.

### Ciclo Completo
```bash
python run_agents.py --full
```

Executa o ciclo completo:
1. Discovery (análise)
2. Planning (planejamento)
3. Execution (implementação real de melhorias)
4. Report (relatório final do CEO)

Isso vai **CRIAR ARQUIVOS REAIS**:
- Estrutura de testes (`tests/`)
- GitHub Actions CI (`.github/workflows/ci.yml`)
- Configuração de ferramentas (`pyproject.toml` atualizado)
- Jupyter notebooks (`notebooks/`)
- Streamlit dashboard (`dashboard/`)

## 📦 Estrutura de Arquivos

```
src/market_lab/agents/
├── __init__.py              # Exports principais
├── core.py                  # Infraestrutura base (Agent, Message, Bus)
├── specialists.py           # Implementação dos 13 agentes
├── organization.py          # Orquestração e coordenação
├── actions.py               # Ações concretas (criar arquivos, etc)
└── runner.py                # Script de execução

run_agents.py                # CLI principal
AGENTS.md                    # Esta documentação
```

## 🎯 Artefatos Gerados

Quando você roda `python run_agents.py --full`, os agentes criam:

### 1. Test Suite (QA Engineer)
- `tests/` - Estrutura completa de testes
- `tests/conftest.py` - Fixtures compartilhadas
- `tests/test_core/test_orders.py` - Testes de exemplo
- pytest configurado com coverage

### 2. CI/CD (DevOps Engineer)
- `.github/workflows/ci.yml` - GitHub Actions workflow
- Testes automáticos em PRs
- Linting com ruff
- Type checking com mypy
- Coverage reporting

### 3. Dev Tools (CTO)
- Configuração ruff em `pyproject.toml`
- Configuração mypy em `pyproject.toml`
- Dependências de dev adicionadas

### 4. Jupyter Notebooks (Doc Writer + Frontend Dev)
- `notebooks/` - Estrutura de notebooks
- `notebooks/01_random_walk.ipynb` - Primeiro notebook
- `notebooks/README.md` - Guia de uso

### 5. Streamlit Dashboard (Frontend Developer)
- `dashboard/app.py` - Dashboard interativo
- `dashboard/README.md` - Instruções de uso
- Configuração visual de simulações
- Visualização em tempo real

## 🔧 Extensibilidade

### Adicionar Novo Agente

1. Criar classe em `specialists.py`:
```python
@dataclass
class NewSpecialistAgent(BaseAgent):
    def __post_init__(self):
        self.role = AgentRole.NEW_SPECIALIST  # Adicionar ao enum
        self.expertise = ["Expertise 1", "Expertise 2"]
        super().__post_init__()

    def analyze(self, context):
        # Implementar análise
        return {...}

    def execute_task(self, task):
        # Implementar execução
        return {...}
```

2. Adicionar ao `Organization.__post_init__()`:
```python
self.new_specialist = NewSpecialistAgent(
    role=AgentRole.NEW_SPECIALIST,
    expertise=[],
    communication_bus=self.communication_bus
)
```

3. Integrar no pipeline conforme necessário.

### Adicionar Nova Ação

1. Adicionar método em `AgentActions`:
```python
def create_new_feature(self) -> dict[str, Any]:
    """
    Descrição da ação.
    """
    # Implementar criação de arquivos/configurações
    return {"status": "completed"}
```

2. Chamar em `demonstrate_agent_actions()`.

## 📊 Métricas e Observabilidade

Cada agente mantém:
- **inbox**: Mensagens recebidas
- **decisions_made**: Log de decisões com rationale
- **tasks_completed**: Log de tarefas completadas

Acessar via:
```python
org = Organization()
ceo_decisions = org.ceo.decisions_made
qa_tasks = org.qa_engineer.tasks_completed
```

## 🎓 Conceitos Avançados

### 1. Autonomia vs. Coordenação
- Agentes são **autônomos** dentro de sua expertise
- Decisões **críticas** sobem para CEO
- Decisões **técnicas** passam por CTO/Tech Lead

### 2. Communication Patterns
- **Command**: CEO → Agente (ordem direta)
- **Query**: Agente → Agente (pedir informação)
- **Broadcast**: Qualquer → Todos (anúncio)
- **Escalation**: Agente → Superior (quando bloqueado)

### 3. Decision Making
- Cada decisão é logged com **rationale**
- Permite auditoria de por que mudanças foram feitas
- Aprendizado organizacional

## 🚧 Roadmap do Sistema de Agentes

### v1.0 (Atual)
- ✅ 13 agentes especializados
- ✅ Communication bus
- ✅ Pipeline Discovery → Planning → Execution
- ✅ Ações concretas (criar arquivos)
- ✅ CLI funcional

### v2.0 (Futuro)
- 🔲 Agentes com LLM integration
- 🔲 Auto-review de código
- 🔲 Auto-fix de bugs encontrados
- 🔲 Aprendizado a partir de métricas

### v3.0 (Visão)
- 🔲 Agentes totalmente autônomos
- 🔲 Self-improvement cycle
- 🔲 Community feedback integration
- 🔲 Multi-projeto support

## 💡 Exemplos de Uso

### Exemplo 1: Adicionar Nova Feature
```python
from market_lab.agents.organization import Organization

org = Organization()

# PM define feature
roadmap = org.product_manager.execute_task({
    "type": "add_feature",
    "feature": "Spoofing manipulation strategy"
})

# Market Specialist valida
validation = org.market_specialist.execute_task({
    "type": "validate_strategy",
    "strategy": "spoofing"
})

# Backend Dev implementa
implementation = org.backend_dev.execute_task({
    "type": "implement_feature",
    "feature": "spoofing",
    "spec": validation
})

# QA cria testes
tests = org.qa_engineer.execute_task({
    "type": "test_feature",
    "feature": "spoofing"
})

# CEO aprova release
org.ceo.execute_task({
    "type": "approve_release",
    "version": "0.2.1"
})
```

### Exemplo 2: Quality Check
```python
# QA roda análise
qa_report = org.qa_engineer.analyze({
    "codebase": "market_lab"
})

if qa_report["test_coverage"] < 70:
    # Escalar para CEO
    org.qa_engineer.communicate(
        receiver=AgentRole.CEO,
        content="Test coverage below threshold!",
        priority=MessagePriority.CRITICAL,
        requires_response=True
    )
```

## 🤝 Contribuindo

Para estender o sistema de agentes:

1. **Novos Agentes**: Adicionar em `specialists.py`
2. **Novas Ações**: Adicionar em `actions.py`
3. **Novos Workflows**: Modificar `organization.py`
4. **Documentação**: Atualizar este arquivo

## 📝 Licença

Este sistema de agentes é parte do Market Manipulation Lab e segue a mesma licença do projeto principal.

---

**Criado por**: Sistema de Agentes Especializados
**Última atualização**: 2025-11-19
**Status**: 🟢 Production Ready
