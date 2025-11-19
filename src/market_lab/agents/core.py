"""
Core infrastructure para o sistema de agentes especializados.

Define as classes base, protocolos e infraestrutura de comunicação
que permitem aos agentes trabalharem de forma colaborativa e autônoma.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, Callable, Any
from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Prioridade de mensagens no sistema de comunicação."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AgentRole(Enum):
    """Papéis possíveis para agentes no sistema."""

    # C-Level
    CEO = "CEO"
    CTO = "CTO"

    # Management
    PRODUCT_MANAGER = "Product Manager"
    TECH_LEAD = "Tech Lead"

    # Design
    UX_DESIGNER = "UX/UI Designer"

    # Development
    BACKEND_DEVELOPER = "Backend Developer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    DATA_SCIENTIST = "Data Scientist"

    # Quality & Ops
    QA_ENGINEER = "QA Engineer"
    DEVOPS_ENGINEER = "DevOps Engineer"

    # Specialists
    MARKET_SPECIALIST = "Market Specialist"
    DOCUMENTATION_WRITER = "Documentation Writer"
    USER_RESEARCHER = "User Researcher"


@dataclass
class Message:
    """
    Mensagem trocada entre agentes.

    Attributes:
        sender: Role do agente que enviou
        receiver: Role do agente destinatário (None = broadcast)
        content: Conteúdo da mensagem
        priority: Prioridade da mensagem
        timestamp: Momento de criação
        context: Contexto adicional (dados, referências, etc)
        requires_response: Se o remetente espera resposta
    """

    sender: AgentRole
    receiver: AgentRole | None
    content: str
    priority: MessagePriority = MessagePriority.MEDIUM
    timestamp: datetime = field(default_factory=datetime.now)
    context: dict[str, Any] = field(default_factory=dict)
    requires_response: bool = False

    def __str__(self) -> str:
        receiver_str = self.receiver.value if self.receiver else "ALL"
        return f"[{self.priority.name}] {self.sender.value} → {receiver_str}: {self.content}"


class CommunicationBus:
    """
    Sistema de comunicação centralizado entre agentes.

    Permite que agentes enviem mensagens uns aos outros,
    subscribe em tópicos específicos e processem mensagens de forma assíncrona.
    """

    def __init__(self):
        self._messages: list[Message] = []
        self._subscribers: dict[AgentRole, list[Callable[[Message], None]]] = defaultdict(list)
        self._broadcast_subscribers: list[Callable[[Message], None]] = []

    def send(self, message: Message) -> None:
        """Envia uma mensagem no bus."""
        self._messages.append(message)
        logger.info(f"Message sent: {message}")

        # Entregar para destinatário específico
        if message.receiver:
            for handler in self._subscribers[message.receiver]:
                handler(message)

        # Entregar para subscribers de broadcast
        for handler in self._broadcast_subscribers:
            handler(message)

    def subscribe(self, role: AgentRole, handler: Callable[[Message], None]) -> None:
        """Subscribe um handler para mensagens direcionadas a um role."""
        self._subscribers[role].append(handler)
        logger.debug(f"Agent {role.value} subscribed to messages")

    def subscribe_broadcast(self, handler: Callable[[Message], None]) -> None:
        """Subscribe um handler para todas as mensagens (broadcast)."""
        self._broadcast_subscribers.append(handler)
        logger.debug("Handler subscribed to broadcast messages")

    def get_messages(
        self,
        sender: AgentRole | None = None,
        receiver: AgentRole | None = None,
        priority: MessagePriority | None = None
    ) -> list[Message]:
        """Recupera mensagens filtradas por critérios."""
        filtered = self._messages

        if sender:
            filtered = [m for m in filtered if m.sender == sender]
        if receiver:
            filtered = [m for m in filtered if m.receiver == receiver]
        if priority:
            filtered = [m for m in filtered if m.priority == priority]

        return filtered

    def clear(self) -> None:
        """Limpa todas as mensagens (útil para testes)."""
        self._messages.clear()


class Agent(Protocol):
    """
    Protocol que define a interface de um agente especializado.

    Cada agente deve implementar estes métodos para participar
    do sistema colaborativo.
    """

    role: AgentRole
    expertise: list[str]
    communication_bus: CommunicationBus

    def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Analisa um contexto e retorna insights da sua expertise.

        Args:
            context: Informações sobre o que precisa ser analisado

        Returns:
            Insights, recomendações e análises
        """
        ...

    def execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Executa uma tarefa específica da sua área.

        Args:
            task: Descrição da tarefa e parâmetros

        Returns:
            Resultado da execução
        """
        ...

    def communicate(self, receiver: AgentRole | None, content: str, priority: MessagePriority = MessagePriority.MEDIUM) -> None:
        """
        Envia uma mensagem para outro agente ou broadcast.

        Args:
            receiver: Agente destinatário (None para broadcast)
            content: Conteúdo da mensagem
            priority: Prioridade da mensagem
        """
        ...

    def receive_message(self, message: Message) -> None:
        """
        Processa uma mensagem recebida.

        Args:
            message: Mensagem recebida
        """
        ...


@dataclass
class BaseAgent:
    """
    Implementação base de um agente especializado.

    Fornece funcionalidade comum que todos os agentes compartilham.
    """

    role: AgentRole
    expertise: list[str]
    communication_bus: CommunicationBus
    name: str = ""

    # Estado interno
    inbox: list[Message] = field(default_factory=list)
    decisions_made: list[dict[str, Any]] = field(default_factory=list)
    tasks_completed: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = self.role.value

        # Subscribe para mensagens direcionadas a este agente
        self.communication_bus.subscribe(self.role, self.receive_message)

    def communicate(
        self,
        receiver: AgentRole | None,
        content: str,
        priority: MessagePriority = MessagePriority.MEDIUM,
        context: dict[str, Any] | None = None,
        requires_response: bool = False
    ) -> None:
        """Envia mensagem via communication bus."""
        message = Message(
            sender=self.role,
            receiver=receiver,
            content=content,
            priority=priority,
            context=context or {},
            requires_response=requires_response
        )
        self.communication_bus.send(message)

    def receive_message(self, message: Message) -> None:
        """Processa mensagem recebida."""
        self.inbox.append(message)
        logger.info(f"{self.name} received: {message.content}")

    def log_decision(self, decision: str, rationale: str, context: dict[str, Any] | None = None) -> None:
        """Registra uma decisão tomada."""
        decision_record = {
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now(),
            "context": context or {}
        }
        self.decisions_made.append(decision_record)
        logger.info(f"{self.name} decided: {decision}")

    def log_task_completion(self, task: str, result: dict[str, Any]) -> None:
        """Registra conclusão de uma tarefa."""
        task_record = {
            "task": task,
            "result": result,
            "timestamp": datetime.now()
        }
        self.tasks_completed.append(task_record)
        logger.info(f"{self.name} completed: {task}")
