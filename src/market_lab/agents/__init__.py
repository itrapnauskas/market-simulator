"""
Sistema de Agentes Especializados para Market Manipulation Lab

Este módulo implementa um exército de agentes super especializados que trabalham
em conjunto para desenvolver, melhorar e manter o Market Simulator.

Cada agente tem expertise específica e pode comunicar-se com outros agentes
para tomar decisões colaborativas. O CEO coordena tudo e é o único ponto de
contato com stakeholders externos.
"""

from .core import Agent, AgentRole, Message, MessagePriority, CommunicationBus
from .organization import Organization
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

__all__ = [
    "Agent",
    "AgentRole",
    "Message",
    "MessagePriority",
    "CommunicationBus",
    "Organization",
    "CEOAgent",
    "CTOAgent",
    "ProductManagerAgent",
    "TechLeadAgent",
    "UXDesignerAgent",
    "BackendDeveloperAgent",
    "FrontendDeveloperAgent",
    "DataScientistAgent",
    "QAEngineerAgent",
    "DevOpsEngineerAgent",
    "MarketSpecialistAgent",
    "DocumentationWriterAgent",
    "UserResearcherAgent",
]
