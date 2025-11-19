#!/usr/bin/env python3
"""
🏢 MARKET MANIPULATION LAB - SISTEMA DE AGENTES ESPECIALIZADOS

Script principal para executar o exército de agentes super especializados
que trabalham de forma autônoma para melhorar o Market Simulator.

Uso:
    python run_agents.py --demo       # Demonstração rápida
    python run_agents.py --full       # Ciclo completo com ações concretas
    python run_agents.py --report     # Apenas relatório de análise
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from market_lab.agents.organization import Organization
from market_lab.agents.actions import demonstrate_agent_actions


def run_demo():
    """Demonstração rápida dos agentes."""
    print("\n" + "=" * 80)
    print("🏢 DEMO: SISTEMA DE AGENTES ESPECIALIZADOS")
    print("=" * 80)
    print("\n📋 Agentes Disponíveis:")
    print()

    org = Organization()

    agents_info = [
        ("CEO", "Coordenação estratégica e decisões finais"),
        ("CTO", "Liderança técnica e arquitetura"),
        ("Product Manager", "Roadmap e priorização de features"),
        ("Tech Lead", "Qualidade de código e arquitetura"),
        ("UX Designer", "Design de experiência e interface"),
        ("Backend Developer", "Implementação de lógica core"),
        ("Frontend Developer", "Visualizações e dashboards"),
        ("Data Scientist", "Algoritmos e análises"),
        ("QA Engineer", "Testes e qualidade"),
        ("DevOps Engineer", "CI/CD e infraestrutura"),
        ("Market Specialist", "Expertise em finanças"),
        ("Documentation Writer", "Documentação técnica"),
        ("User Researcher", "Pesquisa de usuários"),
    ]

    for name, description in agents_info:
        print(f"  👤 {name:25s} → {description}")

    print("\n" + "=" * 80)
    print("✅ 13 agentes prontos para trabalhar de forma autônoma!")
    print("=" * 80)
    print()


def run_report_only():
    """Executa apenas análise e relatório."""
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO DE ANÁLISE DO PROJETO")
    print("=" * 80)
    print()

    org = Organization()

    context = {
        "codebase_analysis": {
            "lines_of_code": 799,
            "lines_of_docs": 1302,
            "test_coverage": 0,
            "modules": ["core", "manipulation", "viz", "experiments"],
        }
    }

    # Apenas discovery
    print("🔍 Executando Discovery Phase...\n")
    discovery = org.kickoff_discovery_phase(context)

    # Mostrar insights chave
    print("📌 INSIGHTS CHAVE:\n")

    print("🔧 CTO Analysis:")
    for rec in discovery["cto"].get("recommendations", []):
        print(f"   • {rec}")

    print("\n📦 Product Manager Analysis:")
    for gap in discovery["product_manager"].get("feature_gaps", []):
        print(f"   • {gap}")

    print("\n🧪 QA Engineer Analysis:")
    qa = discovery["qa_engineer"]
    print(f"   • Test Coverage: {qa.get('current_test_coverage', 'N/A')}")
    print(f"   • Risk Level: {qa.get('risk_level', 'N/A')}")

    print("\n🎨 UX Designer Analysis:")
    for improvement in discovery["ux_designer"].get("ux_improvements", []):
        print(f"   • {improvement}")

    print("\n" + "=" * 80)
    print()


def run_full_cycle():
    """Executa ciclo completo: análise + ações concretas."""
    print("\n" + "=" * 80)
    print("🚀 CICLO COMPLETO: AGENTES EM AÇÃO")
    print("=" * 80)
    print()

    # 1. Executar organização (análise e planejamento)
    print("📊 FASE 1: ANÁLISE E PLANEJAMENTO\n")

    org = Organization()

    context = {
        "codebase_analysis": {
            "lines_of_code": 799,
            "lines_of_docs": 1302,
            "test_coverage": 0,
            "modules": ["core", "manipulation", "viz", "experiments"],
        }
    }

    results = org.run_full_cycle(context)

    print("\n✅ Análise concluída!\n")
    print("=" * 80)

    # 2. Executar ações concretas
    print("\n🔨 FASE 2: IMPLEMENTAÇÃO\n")

    project_root = Path(__file__).parent
    action_results = demonstrate_agent_actions(project_root)

    print("=" * 80)

    # 3. Relatório final
    print("\n📋 RELATÓRIO FINAL DO CEO\n")
    print("=" * 80)
    print()
    print(results["final_report"])
    print()

    # 4. Resumo das ações
    print("=" * 80)
    print("\n🎯 RESUMO DAS AÇÕES EXECUTADAS:\n")

    actions_summary = [
        ("Tests", action_results["tests"]["tests_created"], "test files created"),
        ("CI/CD", len(action_results["ci_cd"]["workflows_created"]), "GitHub Actions workflows"),
        ("Dev Tools", len(action_results["dev_deps"].get("dependencies_added", [])), "dev dependencies"),
        ("Linting", 1, "ruff configuration"),
        ("Type Checking", 1, "mypy configuration"),
        ("Notebooks", len(action_results["notebooks"]["notebooks_created"]), "Jupyter notebooks"),
        ("Dashboard", len(action_results["dashboard"]["files_created"]), "dashboard files"),
    ]

    for category, count, description in actions_summary:
        print(f"  ✓ {category:15s} → {count} {description}")

    print("\n" + "=" * 80)
    print("🎉 SISTEMA PRONTO! Os agentes implementaram melhorias concretas.")
    print("=" * 80)
    print()

    # 5. Próximos passos
    print("📌 PRÓXIMOS PASSOS:\n")
    print("  1. Revisar os arquivos criados pelos agentes")
    print("  2. Instalar dependências: pip install -e '.[dev,viz]'")
    print("  3. Rodar testes: pytest tests/")
    print("  4. Rodar linter: ruff check src/")
    print("  5. Explorar notebooks: jupyter lab notebooks/")
    print("  6. Testar dashboard: streamlit run dashboard/app.py")
    print()


def main():
    """Função principal com CLI."""
    parser = argparse.ArgumentParser(
        description="🏢 Sistema de Agentes Especializados para Market Manipulation Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python run_agents.py --demo        # Mostra os agentes disponíveis
  python run_agents.py --report      # Análise do projeto
  python run_agents.py --full        # Ciclo completo com implementação
        """
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Demonstração rápida dos agentes"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Apenas relatório de análise"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Ciclo completo: análise + implementação"
    )

    args = parser.parse_args()

    # Se nenhum argumento, mostrar help
    if not (args.demo or args.report or args.full):
        parser.print_help()
        return 0

    # Executar modo selecionado
    if args.demo:
        run_demo()

    if args.report:
        run_report_only()

    if args.full:
        run_full_cycle()

    return 0


if __name__ == "__main__":
    sys.exit(main())
