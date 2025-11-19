"""
Organization - Sistema que coordena todos os agentes trabalhando em conjunto.

A Organization é a fábrica de sistemas e negócios onde todos os agentes
colaboram para melhorar o Market Manipulation Lab.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import logging

from .core import CommunicationBus, MessagePriority, AgentRole
from .specialists import (
    CEOAgent,
    CTOAgent,
    ProductManagerAgent,
    TechLeadAgent,
    UXDesignerAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    DataScientistAgent,
    QAEngineerAgent,
    DevOpsEngineerAgent,
    MarketSpecialistAgent,
    DocumentationWriterAgent,
    UserResearcherAgent,
)

logger = logging.getLogger(__name__)


@dataclass
class Organization:
    """
    A Organização que coordena todos os agentes especializados.

    Esta é a fábrica de sistemas onde cada agente tem função específica,
    conversam entre si para chegar em conclusões, e trabalham em um pipeline
    de criação do Market Simulator.

    O CEO é o único ponto de contato com stakeholders externos.
    Todos os outros agentes se reportam através da hierarquia.
    """

    # Communication infrastructure
    communication_bus: CommunicationBus = field(default_factory=CommunicationBus)

    # Agents (initialized in __post_init__)
    ceo: CEOAgent = field(init=False)
    cto: CTOAgent = field(init=False)
    product_manager: ProductManagerAgent = field(init=False)
    tech_lead: TechLeadAgent = field(init=False)
    ux_designer: UXDesignerAgent = field(init=False)
    backend_dev: BackendDeveloperAgent = field(init=False)
    frontend_dev: FrontendDeveloperAgent = field(init=False)
    data_scientist: DataScientistAgent = field(init=False)
    qa_engineer: QAEngineerAgent = field(init=False)
    devops_engineer: DevOpsEngineerAgent = field(init=False)
    market_specialist: MarketSpecialistAgent = field(init=False)
    doc_writer: DocumentationWriterAgent = field(init=False)
    user_researcher: UserResearcherAgent = field(init=False)

    def __post_init__(self):
        """Inicializa todos os agentes e conecta ao communication bus."""
        # C-Level
        self.ceo = CEOAgent(
            role=AgentRole.CEO,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.cto = CTOAgent(
            role=AgentRole.CTO,
            expertise=[],
            communication_bus=self.communication_bus
        )

        # Management
        self.product_manager = ProductManagerAgent(
            role=AgentRole.PRODUCT_MANAGER,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.tech_lead = TechLeadAgent(
            role=AgentRole.TECH_LEAD,
            expertise=[],
            communication_bus=self.communication_bus
        )

        # Design
        self.ux_designer = UXDesignerAgent(
            role=AgentRole.UX_DESIGNER,
            expertise=[],
            communication_bus=self.communication_bus
        )

        # Development
        self.backend_dev = BackendDeveloperAgent(
            role=AgentRole.BACKEND_DEVELOPER,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.frontend_dev = FrontendDeveloperAgent(
            role=AgentRole.FRONTEND_DEVELOPER,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.data_scientist = DataScientistAgent(
            role=AgentRole.DATA_SCIENTIST,
            expertise=[],
            communication_bus=self.communication_bus
        )

        # Quality & Ops
        self.qa_engineer = QAEngineerAgent(
            role=AgentRole.QA_ENGINEER,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.devops_engineer = DevOpsEngineerAgent(
            role=AgentRole.DEVOPS_ENGINEER,
            expertise=[],
            communication_bus=self.communication_bus
        )

        # Specialists
        self.market_specialist = MarketSpecialistAgent(
            role=AgentRole.MARKET_SPECIALIST,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.doc_writer = DocumentationWriterAgent(
            role=AgentRole.DOCUMENTATION_WRITER,
            expertise=[],
            communication_bus=self.communication_bus
        )
        self.user_researcher = UserResearcherAgent(
            role=AgentRole.USER_RESEARCHER,
            expertise=[],
            communication_bus=self.communication_bus
        )

        logger.info("Organization initialized with 13 specialized agents")

    def get_agent(self, role: AgentRole):
        """Retorna agente por role."""
        mapping = {
            AgentRole.CEO: self.ceo,
            AgentRole.CTO: self.cto,
            AgentRole.PRODUCT_MANAGER: self.product_manager,
            AgentRole.TECH_LEAD: self.tech_lead,
            AgentRole.UX_DESIGNER: self.ux_designer,
            AgentRole.BACKEND_DEVELOPER: self.backend_dev,
            AgentRole.FRONTEND_DEVELOPER: self.frontend_dev,
            AgentRole.DATA_SCIENTIST: self.data_scientist,
            AgentRole.QA_ENGINEER: self.qa_engineer,
            AgentRole.DEVOPS_ENGINEER: self.devops_engineer,
            AgentRole.MARKET_SPECIALIST: self.market_specialist,
            AgentRole.DOCUMENTATION_WRITER: self.doc_writer,
            AgentRole.USER_RESEARCHER: self.user_researcher,
        }
        return mapping[role]

    def kickoff_discovery_phase(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Fase 1: Discovery - Todos os agentes analisam o projeto atual.

        Args:
            context: Contexto sobre o projeto (codebase, docs, etc)

        Returns:
            Compilação de todas as análises
        """
        logger.info("=== DISCOVERY PHASE STARTED ===")

        # CEO inicia o processo
        self.ceo.communicate(
            receiver=None,  # Broadcast
            content="Discovery phase initiated. All teams: analyze current state and provide insights.",
            priority=MessagePriority.HIGH
        )

        # Cada agente faz sua análise
        analyses = {}

        # C-Level
        analyses["ceo"] = self.ceo.analyze(context)
        analyses["cto"] = self.cto.analyze(context)

        # Management
        analyses["product_manager"] = self.product_manager.analyze(context)
        analyses["tech_lead"] = self.tech_lead.analyze(context)

        # Design
        analyses["ux_designer"] = self.ux_designer.analyze(context)

        # Development
        analyses["backend_dev"] = self.backend_dev.analyze(context)
        analyses["frontend_dev"] = self.frontend_dev.analyze(context)
        analyses["data_scientist"] = self.data_scientist.analyze(context)

        # Quality & Ops
        analyses["qa_engineer"] = self.qa_engineer.analyze(context)
        analyses["devops_engineer"] = self.devops_engineer.analyze(context)

        # Specialists
        analyses["market_specialist"] = self.market_specialist.analyze(context)
        analyses["doc_writer"] = self.doc_writer.analyze(context)
        analyses["user_researcher"] = self.user_researcher.analyze(context)

        logger.info("=== DISCOVERY PHASE COMPLETED ===")
        return analyses

    def kickoff_planning_phase(self, discovery_results: dict[str, Any]) -> dict[str, Any]:
        """
        Fase 2: Planning - PM cria roadmap, CTO define padrões, etc.

        Args:
            discovery_results: Resultados da fase de discovery

        Returns:
            Planos de cada área
        """
        logger.info("=== PLANNING PHASE STARTED ===")

        # Product Manager cria roadmap
        roadmap_result = self.product_manager.execute_task({
            "type": "create_roadmap",
            "context": discovery_results
        })

        # CTO define padrões técnicos
        standards_result = self.cto.execute_task({
            "type": "define_standards",
            "context": discovery_results
        })

        # UX Designer cria wireframes
        design_result = self.ux_designer.execute_task({
            "type": "design_dashboard",
            "context": discovery_results
        })

        # User Researcher cria personas
        personas_result = self.user_researcher.execute_task({
            "type": "create_personas",
            "context": discovery_results
        })

        # CEO aprova roadmap
        approval_result = self.ceo.execute_task({
            "type": "approve_roadmap",
            "roadmap": roadmap_result.get("roadmap")
        })

        logger.info("=== PLANNING PHASE COMPLETED ===")

        return {
            "roadmap": roadmap_result,
            "technical_standards": standards_result,
            "design": design_result,
            "personas": personas_result,
            "ceo_approval": approval_result
        }

    def kickoff_execution_phase(self, plans: dict[str, Any]) -> dict[str, Any]:
        """
        Fase 3: Execution - Times executam as tarefas planejadas.

        Args:
            plans: Planos da fase de planning

        Returns:
            Resultados da execução
        """
        logger.info("=== EXECUTION PHASE STARTED ===")

        results = {}

        # DevOps setup CI/CD primeiro
        results["ci_cd"] = self.devops_engineer.execute_task({
            "type": "setup_ci"
        })

        # QA cria test suite
        results["tests"] = self.qa_engineer.execute_task({
            "type": "create_test_suite"
        })

        # Doc Writer adiciona docstrings
        results["documentation"] = self.doc_writer.execute_task({
            "type": "write_docstrings"
        })

        # Backend Dev implementa features
        results["backend_features"] = self.backend_dev.execute_task({
            "type": "implement_feature",
            "feature": "Additional manipulation strategies"
        })

        # Frontend Dev implementa dashboard
        results["dashboard"] = self.frontend_dev.execute_task({
            "type": "implement_dashboard"
        })

        # Data Scientist melhora detecção
        results["detection"] = self.data_scientist.execute_task({
            "type": "improve_detection"
        })

        # Market Specialist valida realismo
        results["validation"] = self.market_specialist.execute_task({
            "type": "validate_realism"
        })

        # Tech Lead faz code review
        results["code_review"] = self.tech_lead.execute_task({
            "type": "code_review"
        })

        logger.info("=== EXECUTION PHASE COMPLETED ===")

        return results

    def generate_report_for_stakeholder(
        self,
        discovery: dict[str, Any],
        planning: dict[str, Any],
        execution: dict[str, Any]
    ) -> str:
        """
        CEO gera relatório para stakeholder externo.

        Args:
            discovery: Resultados da discovery
            planning: Resultados do planning
            execution: Resultados da execution

        Returns:
            Relatório formatado
        """
        report = []
        report.append("=" * 80)
        report.append("MARKET MANIPULATION LAB - RELATÓRIO EXECUTIVO")
        report.append("Preparado por: CEO Agent")
        report.append("=" * 80)
        report.append("")

        # Executive Summary
        report.append("## EXECUTIVE SUMMARY")
        report.append("")
        report.append("A organização conduziu análise completa do Market Manipulation Lab")
        report.append("e executou plano de melhorias coordenado por 13 agentes especializados.")
        report.append("")

        # Discovery Highlights
        report.append("## DISCOVERY HIGHLIGHTS")
        report.append("")
        report.append("### Technical Assessment (CTO)")
        cto_analysis = discovery.get("cto", {})
        for rec in cto_analysis.get("recommendations", []):
            report.append(f"  - {rec}")
        report.append("")

        report.append("### Product Assessment (Product Manager)")
        pm_analysis = discovery.get("product_manager", {})
        for gap in pm_analysis.get("feature_gaps", []):
            report.append(f"  - {gap}")
        report.append("")

        report.append("### Quality Assessment (QA Engineer)")
        qa_analysis = discovery.get("qa_engineer", {})
        report.append(f"  - Test Coverage: {qa_analysis.get('current_test_coverage', 'N/A')}")
        report.append(f"  - Risk Level: {qa_analysis.get('risk_level', 'N/A')}")
        report.append("")

        # Planning Results
        report.append("## PLANNING RESULTS")
        report.append("")
        roadmap = planning.get("roadmap", {}).get("roadmap", {})
        for version, details in roadmap.items():
            report.append(f"### {version}: {details.get('theme')}")
            for feature in details.get("features", []):
                report.append(f"  - {feature}")
            report.append("")

        # Execution Results
        report.append("## EXECUTION RESULTS")
        report.append("")
        for area, result in execution.items():
            status = result.get("status", "unknown")
            report.append(f"### {area.replace('_', ' ').title()}: {status}")
            if area == "tests":
                report.append(f"  - Coverage: {result.get('coverage', 'N/A')}")
                report.append(f"  - Tests Created: {result.get('tests_created', 'N/A')}")
            elif area == "documentation":
                report.append(f"  - Files Documented: {result.get('files_documented', 'N/A')}")
                report.append(f"  - Coverage: {result.get('docstring_coverage', 'N/A')}")
            elif area == "detection":
                report.append(f"  - Accuracy Improvement: {result.get('accuracy_improvement', 'N/A')}")
            report.append("")

        # Next Steps
        report.append("## NEXT STEPS")
        report.append("")
        report.append("1. Continue execution of v0.2.0 roadmap")
        report.append("2. Monitor quality metrics (test coverage, code quality)")
        report.append("3. Gather user feedback on new features")
        report.append("4. Plan v0.3.0 (Educational Content)")
        report.append("")

        report.append("=" * 80)
        report.append("End of Report")
        report.append("=" * 80)

        return "\n".join(report)

    def run_full_cycle(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Executa ciclo completo: Discovery → Planning → Execution → Report

        Args:
            context: Contexto inicial sobre o projeto

        Returns:
            Todos os resultados e relatório final
        """
        logger.info("🚀 Starting full organizational cycle")

        # Fase 1: Discovery
        discovery_results = self.kickoff_discovery_phase(context)

        # Fase 2: Planning
        planning_results = self.kickoff_planning_phase(discovery_results)

        # Fase 3: Execution
        execution_results = self.kickoff_execution_phase(planning_results)

        # Fase 4: Report
        final_report = self.generate_report_for_stakeholder(
            discovery=discovery_results,
            planning=planning_results,
            execution=execution_results
        )

        logger.info("✅ Full organizational cycle completed")

        return {
            "discovery": discovery_results,
            "planning": planning_results,
            "execution": execution_results,
            "final_report": final_report,
            "messages": self.communication_bus.get_messages()
        }
