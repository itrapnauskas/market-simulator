"""
Runner - Script para executar o sistema de agentes.

Este script demonstra o exército de agentes trabalhando em conjunto
para analisar e melhorar o Market Manipulation Lab.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from .organization import Organization


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def main():
    """Executa o ciclo completo da organização de agentes."""

    print("\n" + "=" * 80)
    print("🏢 MARKET MANIPULATION LAB - SISTEMA DE AGENTES ESPECIALIZADOS")
    print("=" * 80)
    print("\nInicializando organização com 13 agentes super especializados...\n")

    # Criar organização
    org = Organization()

    # Contexto do projeto (baseado na análise real do codebase)
    project_context = {
        "codebase_analysis": {
            "lines_of_code": 799,
            "lines_of_docs": 1302,
            "test_coverage": 0,
            "modules": ["core", "manipulation", "viz", "experiments"],
            "technologies": ["Python 3.11+", "matplotlib (optional)"],
            "architecture": "Modular with clear separation of concerns",
        },
        "current_features": [
            "Market simulation with auction pricing",
            "Random and wealth-limited traders",
            "Pump-and-dump manipulation",
            "Basic anomaly detection",
            "Matplotlib visualizations",
            "Random walk experiment"
        ],
        "missing_features": [
            "Jupyter notebooks",
            "Test suite",
            "Additional experiments",
            "Streamlit dashboard",
            "Multiple assets",
            "CI/CD pipeline"
        ],
        "pain_points": [
            "Zero test coverage",
            "Missing docstrings in code",
            "No CI/CD automation",
            "CLI-only interface",
            "No notebooks for education"
        ]
    }

    print("📊 Contexto do projeto carregado:")
    print(f"  - Linhas de código: {project_context['codebase_analysis']['lines_of_code']}")
    print(f"  - Test coverage: {project_context['codebase_analysis']['test_coverage']}% ⚠️")
    print(f"  - Módulos: {len(project_context['codebase_analysis']['modules'])}")
    print("")

    # Executar ciclo completo
    print("🚀 Iniciando ciclo completo: Discovery → Planning → Execution → Report\n")

    results = org.run_full_cycle(project_context)

    # Mostrar relatório final
    print("\n" + "=" * 80)
    print("📋 RELATÓRIO FINAL DO CEO")
    print("=" * 80)
    print("")
    print(results["final_report"])
    print("")

    # Estatísticas de comunicação
    messages = results.get("messages", [])
    print(f"💬 Total de mensagens trocadas entre agentes: {len(messages)}")
    print("")

    # Mostrar algumas mensagens interessantes
    high_priority_msgs = [m for m in messages if m.priority.value >= 3]
    if high_priority_msgs:
        print("📢 Mensagens de alta prioridade:")
        for msg in high_priority_msgs[:5]:  # Mostrar até 5
            print(f"  - {msg}")
        print("")

    print("✅ Sistema de agentes executado com sucesso!")
    print("")
    print("=" * 80)
    print("Os agentes estão prontos para trabalhar de forma autônoma.")
    print("CEO Agent é o único ponto de contato para decisões externas.")
    print("=" * 80)
    print("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
