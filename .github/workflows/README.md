# GitHub Actions Workflows

Este diretório contém os workflows de CI/CD do Market Manipulation Lab.

## Workflows Disponíveis

### 1. CI (Continuous Integration) - `ci.yml`

**Trigger:** Push e Pull Request em `main` e `develop`

**Funcionalidades:**
- Testes em múltiplas versões do Python (3.11, 3.12, 3.13)
- Testes em múltiplos sistemas operacionais (Ubuntu, Windows, macOS)
- Cache inteligente de dependências para builds mais rápidos
- Linting com ruff
- Type checking com mypy
- Testes com pytest e coverage
- Upload de coverage para Codecov
- Verificações de segurança com safety e bandit
- Build e validação do pacote

**Jobs:**
- `test`: Executa testes em todas as combinações de Python e SO
- `lint-quality`: Verificações de qualidade de código
- `security`: Scans de segurança
- `build`: Build e validação do pacote

**Duração estimada:** ~10-15 minutos

### 2. Release - `release.yml`

**Trigger:**
- Push de tags no formato `v*.*.*` (ex: v0.1.0, v1.0.0)
- Workflow manual via `workflow_dispatch`

**Funcionalidades:**
- Validação do formato da tag
- Execução completa do CI antes do release
- Build de distribuições (sdist e wheel)
- Publicação no TestPyPI (para validação)
- Publicação no PyPI (produção)
- Criação de GitHub Release com changelog automático
- Build e push de imagens Docker para GHCR
- Suporte a multi-arquitetura (amd64, arm64)

**Jobs:**
- `validate`: Valida formato da tag e extrai versão
- `test`: Executa CI completo
- `build`: Build das distribuições
- `publish-testpypi`: Publica no TestPyPI
- `publish-pypi`: Publica no PyPI (apenas tags)
- `github-release`: Cria release no GitHub
- `docker-build`: Build e push de imagens Docker
- `notify`: Notificação de conclusão

**Duração estimada:** ~20-30 minutos

**Como fazer um release:**
```bash
# 1. Atualizar versão no pyproject.toml
# 2. Commit e push
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push

# 3. Criar e push tag
git tag v0.2.0
git push origin v0.2.0
```

### 3. Documentation - `docs.yml`

**Trigger:**
- Push em `main` e `develop` (apenas arquivos de docs e src)
- Pull Request para `main` (apenas arquivos de docs)
- Workflow manual via `workflow_dispatch`

**Funcionalidades:**
- Build da documentação com Sphinx
- Geração automática de API docs
- Verificação de links quebrados
- Deploy automático para GitHub Pages (apenas main)
- Upload de artifacts para análise

**Jobs:**
- `build-docs`: Build completo da documentação
- `deploy-docs`: Deploy para GitHub Pages (apenas main)
- `link-check`: Verificação de links (apenas PRs)

**Duração estimada:** ~5-10 minutos

**URL da documentação:** `https://itrapnauskas.github.io/market-simulator/`

### 4. Dependabot - `../dependabot.yml`

**Trigger:** Automático (semanal às segundas-feiras 09:00)

**Funcionalidades:**
- Atualização automática de dependências Python
- Atualização de GitHub Actions
- Atualização de imagens Docker
- Criação automática de PRs
- Labels e assignees automáticos

**Configurações:**
- Target branch: `develop`
- Limite de PRs: 10 (Python), 5 (Actions/Docker)
- Ignora major updates de algumas dependências estáveis

## Secrets Necessários

Para que todos os workflows funcionem corretamente, configure os seguintes secrets:

### GitHub Repository Secrets

1. **CODECOV_TOKEN** (opcional, mas recomendado)
   - Obtido em: https://codecov.io/
   - Usado para: Upload de coverage reports

2. **TEST_PYPI_API_TOKEN** (necessário para releases)
   - Obtido em: https://test.pypi.org/manage/account/token/
   - Usado para: Publicação no TestPyPI

3. **PYPI_API_TOKEN** (necessário para releases)
   - Obtido em: https://pypi.org/manage/account/token/
   - Usado para: Publicação no PyPI oficial

### Como adicionar secrets:

1. Vá para `Settings` > `Secrets and variables` > `Actions`
2. Click em `New repository secret`
3. Adicione nome e valor do secret

## Environments

Configure os seguintes environments para proteção adicional:

### 1. testpypi
- **Protection rules:** Nenhuma (pode publicar automaticamente)
- **Secrets:** TEST_PYPI_API_TOKEN

### 2. pypi
- **Protection rules:**
  - Require reviewers (recomendado)
  - Deployment branch: apenas tags
- **Secrets:** PYPI_API_TOKEN

### 3. github-pages
- **Protection rules:** Deployment branch: apenas `main`
- **Source:** GitHub Actions

### Como configurar environments:

1. Vá para `Settings` > `Environments`
2. Click em `New environment`
3. Configure proteções e secrets

## GitHub Pages Setup

Para ativar o deploy de documentação:

1. Vá para `Settings` > `Pages`
2. Em **Source**, selecione `GitHub Actions`
3. O primeiro deploy acontecerá após push em `main`

## Badges para o README

Adicione ao README.md:

```markdown
[![CI](https://github.com/itrapnauskas/market-simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/itrapnauskas/market-simulator/actions/workflows/ci.yml)
[![Documentation](https://github.com/itrapnauskas/market-simulator/actions/workflows/docs.yml/badge.svg)](https://github.com/itrapnauskas/market-simulator/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/itrapnauskas/market-simulator/branch/main/graph/badge.svg)](https://codecov.io/gh/itrapnauskas/market-simulator)
[![PyPI](https://img.shields.io/pypi/v/market-lab.svg)](https://pypi.org/project/market-lab/)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
```

## Workflow Dispatch (Execução Manual)

Todos os workflows suportam execução manual:

1. Vá para `Actions` tab
2. Selecione o workflow desejado
3. Click em `Run workflow`
4. Selecione a branch e parâmetros (se aplicável)

## Troubleshooting

### Build falhando?

1. Verifique os logs detalhados no GitHub Actions
2. Execute localmente: `make ci`
3. Verifique se todas as dependências estão atualizadas

### Testes lentos?

- Os caches estão configurados, mas podem precisar ser limpos
- Vá para `Actions` > `Caches` e delete caches antigos

### Release não publicando?

1. Verifique se a tag está no formato correto: `v*.*.*`
2. Verifique se os secrets do PyPI estão configurados
3. Verifique se os environments `testpypi` e `pypi` existem

### Documentação não atualizando?

1. Verifique se GitHub Pages está ativado
2. Verifique se o workflow de docs completou com sucesso
3. Pode levar alguns minutos para propagar

## Manutenção

### Atualizar Actions

O Dependabot atualiza automaticamente, mas você pode atualizar manualmente:

```bash
# Verifique versões mais recentes em:
# - actions/checkout
# - actions/setup-python
# - actions/cache
# - codecov/codecov-action
```

### Adicionar novos checks

Para adicionar novos checks ao CI:

1. Edite `.github/workflows/ci.yml`
2. Adicione novo step ou job
3. Teste localmente primeiro com `make ci`
4. Faça PR para `develop`

## Boas Práticas

1. **Sempre teste localmente primeiro**: Use `make ci` antes de push
2. **Use branches feature**: Crie PRs para mudanças significativas
3. **Mantenha workflows rápidos**: Use caches e paralelização
4. **Monitore custos**: GitHub Actions tem limite de minutos gratuitos
5. **Documente mudanças**: Atualize este README ao modificar workflows

## Recursos Adicionais

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Publishing to PyPI](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
