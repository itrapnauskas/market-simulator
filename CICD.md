# Guia de CI/CD - Market Manipulation Lab

## Visão Geral

Este documento descreve a infraestrutura completa de CI/CD implementada para o Market Manipulation Lab, incluindo workflows automatizados, containerização e boas práticas.

## Índice

1. [Arquitetura de CI/CD](#arquitetura-de-cicd)
2. [Workflows Implementados](#workflows-implementados)
3. [Docker e Containerização](#docker-e-containerização)
4. [Automação de Dependências](#automação-de-dependências)
5. [Guia de Release](#guia-de-release)
6. [Comandos Úteis](#comandos-úteis)
7. [Configuração Inicial](#configuração-inicial)

---

## Arquitetura de CI/CD

### Fluxo de Trabalho

```
┌─────────────┐
│   Push to   │
│   develop   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CI Workflow│
│  - Lint     │
│  - Test     │
│  - Security │
│  - Build    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Pull Request│
│   to main   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Merge to  │
│    main     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Tag Release│
│  (v*.*.*)   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Release Workflow   │
│  - Build Package    │
│  - Test PyPI        │
│  - Publish PyPI     │
│  - GitHub Release   │
│  - Docker Images    │
└─────────────────────┘
```

### Branches

- **main**: Branch de produção (protegida)
- **develop**: Branch de desenvolvimento (CI contínuo)
- **feature/***: Branches de features (CI em PRs)

---

## Workflows Implementados

### 1. CI (Continuous Integration)

**Arquivo:** `.github/workflows/ci.yml`

#### Features

- **Matrix Testing:**
  - Python: 3.11, 3.12, 3.13
  - OS: Ubuntu, Windows, macOS

- **Cache Inteligente:**
  - Cache de pip packages
  - Dependências baseadas em hash do pyproject.toml

- **Jobs Paralelos:**
  - `test`: Testes em múltiplas versões
  - `lint-quality`: Verificações de código
  - `security`: Scans de segurança
  - `build`: Build do pacote

- **Checks de Qualidade:**
  - Ruff (linting e formatting)
  - Mypy (type checking)
  - Pytest (testes com coverage)
  - Safety (vulnerabilidades)
  - Bandit (segurança)

#### Timeouts

- Test job: 15 minutos
- Lint/Security: 10 minutos
- Concurrency: Cancela builds antigos automaticamente

#### Executar localmente:

```bash
make ci
```

---

### 2. Release (Publicação Automática)

**Arquivo:** `.github/workflows/release.yml`

#### Pipeline de Release

1. **Validação:**
   - Verifica formato da tag (v*.*.*)
   - Extrai versão

2. **Testes:**
   - Executa CI completo
   - Garante que tudo está funcionando

3. **Build:**
   - Cria sdist e wheel
   - Valida com twine
   - Upload de artifacts

4. **TestPyPI:**
   - Publica em test.pypi.org
   - Valida instalação

5. **PyPI:**
   - Publica em pypi.org
   - Apenas para tags em main

6. **GitHub Release:**
   - Cria release automático
   - Gera changelog baseado em commits
   - Anexa distribuições

7. **Docker:**
   - Build multi-stage
   - Push para ghcr.io
   - Suporte multi-arch (amd64, arm64)

#### Como fazer release:

```bash
# 1. Atualizar versão
vim pyproject.toml  # version = "0.2.0"

# 2. Commit
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
git push origin main

# 3. Criar tag
git tag v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# 4. Aguardar workflow
# GitHub Actions fará o resto automaticamente
```

---

### 3. Documentation (Sphinx + GitHub Pages)

**Arquivo:** `.github/workflows/docs.yml`

#### Features

- **Build Automático:**
  - Sphinx com tema RTD
  - API documentation automática
  - Suporte a MyST (Markdown)

- **Deploy:**
  - GitHub Pages automático
  - Apenas em push para main

- **Validações:**
  - Link checking
  - Build verification

#### Estrutura de Docs:

```
docs/
├── source/
│   ├── conf.py          # Configuração Sphinx
│   ├── index.rst        # Homepage
│   ├── api/             # API Reference
│   │   ├── core.rst
│   │   ├── manipulation.rst
│   │   └── visualization.rst
│   ├── examples/        # Exemplos
│   └── _static/         # Assets estáticos
└── build/               # Build output
```

#### Acessar documentação:

```
https://itrapnauskas.github.io/market-simulator/
```

#### Build local:

```bash
make docs
make docs-serve  # http://localhost:8000
```

---

### 4. Dependabot (Auto-updates)

**Arquivo:** `.github/dependabot.yml`

#### Configuração

- **Python Dependencies:**
  - Frequência: Semanal (segundas, 09:00)
  - Limite: 10 PRs
  - Target: develop branch

- **GitHub Actions:**
  - Frequência: Semanal
  - Limite: 5 PRs

- **Docker:**
  - Atualiza base images
  - Frequência: Semanal

#### Estratégia de Updates:

- Auto-merge para patches de segurança
- Review manual para major updates
- Labels automáticos para organização

---

## Docker e Containerização

### Multi-stage Dockerfile

**Arquivo:** `Dockerfile`

#### Stages Disponíveis:

1. **builder** (intermediário)
   - Compila dependências
   - Cria virtual environment

2. **runtime** (produção)
   - Imagem mínima
   - Apenas runtime dependencies
   - Non-root user
   - ~200MB

3. **development**
   - Inclui dev tools
   - Testes e linting
   - ~350MB

4. **jupyter**
   - JupyterLab completo
   - Extensões e widgets
   - ~400MB

5. **dashboard**
   - Streamlit
   - Visualizações
   - ~300MB

### Build de Imagens:

```bash
# Todas as imagens
make docker-build

# Apenas runtime
make docker-build-runtime

# Ou individualmente
docker build --target runtime -t market-lab:latest .
docker build --target jupyter -t market-lab:jupyter .
docker build --target dashboard -t market-lab:dashboard .
```

### Executar Containers:

```bash
# Runtime
make docker-run

# Development shell
make docker-dev

# Jupyter Lab
make docker-jupyter  # http://localhost:8888

# Dashboard
make docker-dashboard  # http://localhost:8501
```

### Docker Compose

**Arquivo:** `docker-compose.yml`

#### Serviços:

- **market-lab**: Runtime principal
- **market-lab-dev**: Shell de desenvolvimento
- **jupyter**: JupyterLab
- **dashboard**: Streamlit
- **postgres**: Database (opcional, profile: with-db)
- **redis**: Cache (opcional, profile: with-cache)

#### Uso:

```bash
# Todos os serviços core
make docker-compose-up

# Com database
docker-compose --profile with-db up -d

# Com tudo
docker-compose --profile with-db --profile with-cache up -d

# Parar tudo
make docker-compose-down

# Logs
docker-compose logs -f

# Apenas Jupyter
docker-compose up jupyter
```

---

## Automação de Dependências

### Gerenciamento de Pacotes

**Arquivo:** `pyproject.toml`

#### Grupos de Dependências:

```toml
[project.optional-dependencies]
viz = ["matplotlib>=3.8"]
dev = ["pytest>=7.4", "pytest-cov>=4.1", "ruff>=0.1.0", "mypy>=1.7"]
```

#### Instalação:

```bash
# Produção
pip install -e ".[viz]"

# Desenvolvimento
pip install -e ".[dev,viz]"

# Ou use Makefile
make install-dev
```

### Dependabot Configuration

- Atualiza automaticamente
- Cria PRs semanalmente
- Agrupa updates relacionados
- Ignora major updates de pacotes críticos

---

## Guia de Release

### Checklist de Release

- [ ] Todos os testes passando
- [ ] Coverage adequada (>80%)
- [ ] Documentação atualizada
- [ ] CHANGELOG atualizado
- [ ] Versão bumped em pyproject.toml
- [ ] Branch main atualizada

### Versionamento Semântico

```
v{MAJOR}.{MINOR}.{PATCH}

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes
```

### Processo de Release:

```bash
# 1. Finish feature
git checkout develop
git pull

# 2. Create release branch
git checkout -b release/v0.2.0

# 3. Bump version
vim pyproject.toml

# 4. Update CHANGELOG
vim CHANGELOG.md

# 5. Commit and merge to main
git commit -am "chore: prepare release v0.2.0"
git checkout main
git merge release/v0.2.0

# 6. Tag and push
git tag v0.2.0 -m "Release v0.2.0"
git push origin main
git push origin v0.2.0

# 7. Monitor GitHub Actions
# Workflow will:
# - Run tests
# - Build package
# - Publish to TestPyPI
# - Publish to PyPI
# - Create GitHub Release
# - Build and push Docker images

# 8. Merge back to develop
git checkout develop
git merge main
git push origin develop
```

---

## Comandos Úteis

### Makefile Commands

```bash
# Ver todos os comandos
make help

# Instalação
make install          # Produção
make install-dev      # Desenvolvimento
make install-all      # Tudo

# Qualidade de Código
make lint             # Lint
make lint-fix         # Lint + auto-fix
make format           # Format código
make format-check     # Check format
make type-check       # MyPy
make security         # Security scans

# Testes
make test             # Run tests
make test-cov         # Tests + coverage
make test-fast        # Tests sem coverage

# CI Local
make ci               # Todos os checks (como CI)
make pre-commit       # Quick checks

# Build
make build            # Build package
make build-check      # Build + validate

# Documentação
make docs             # Build docs
make docs-serve       # Serve docs

# Docker
make docker-build     # Build all images
make docker-run       # Run container
make docker-jupyter   # Jupyter
make docker-dashboard # Dashboard

# Cleanup
make clean            # Clean build artifacts
make clean-all        # Deep clean
```

### Git Workflows

```bash
# Feature branch
git checkout -b feature/new-feature
# ... work ...
git commit -am "feat: add new feature"
git push origin feature/new-feature
# Create PR to develop

# Hotfix
git checkout -b hotfix/critical-bug main
# ... fix ...
git commit -am "fix: critical bug"
# Merge to main and develop

# Release
git checkout -b release/v1.0.0 develop
# ... prepare ...
git commit -am "chore: release v1.0.0"
# Merge to main, tag, merge back to develop
```

---

## Configuração Inicial

### GitHub Repository

1. **Secrets** (Settings > Secrets and variables > Actions):
   ```
   CODECOV_TOKEN         # Codecov.io
   TEST_PYPI_API_TOKEN   # test.pypi.org
   PYPI_API_TOKEN        # pypi.org
   ```

2. **Environments** (Settings > Environments):
   - `testpypi`: Sem proteção
   - `pypi`: Require reviewers
   - `github-pages`: Deploy de main apenas

3. **GitHub Pages** (Settings > Pages):
   - Source: GitHub Actions
   - Branch: Automático

4. **Branch Protection** (Settings > Branches):
   ```
   main:
     - Require pull request reviews
     - Require status checks to pass
     - Require branches to be up to date
     - Include administrators
   ```

### Local Development

```bash
# 1. Clone
git clone https://github.com/itrapnauskas/market-simulator.git
cd market-simulator

# 2. Setup
make dev-setup

# 3. Run checks
make ci

# 4. Start coding!
```

### First Time PyPI Setup

```bash
# 1. Create account
# https://pypi.org/account/register/
# https://test.pypi.org/account/register/

# 2. Generate API tokens
# PyPI > Account Settings > API tokens

# 3. Add to GitHub Secrets
# Repository Settings > Secrets

# 4. Test publish
make upload-test  # TestPyPI

# 5. Real publish
# Will happen automatically on tag push
```

---

## Troubleshooting

### Build Failures

```bash
# Run CI locally
make ci

# Check specific component
make test-cov
make lint
make type-check

# Clean and retry
make clean
make install-dev
make test
```

### Docker Issues

```bash
# Clean rebuild
docker system prune -a
make docker-build

# Check logs
docker logs <container_id>

# Interactive debug
docker run -it market-lab:dev /bin/bash
```

### Release Problems

```bash
# Check tag format
git tag -l

# Delete bad tag
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0

# Re-create tag
git tag v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

---

## Best Practices

### Development

1. **Sempre use branches**: Nunca commit direto em main
2. **Teste localmente**: Use `make ci` antes de push
3. **Commits semânticos**: feat:, fix:, docs:, chore:
4. **Pequenos PRs**: Easier to review
5. **Documente**: Code + docs juntos

### CI/CD

1. **Fast feedback**: Mantenha CI < 15 min
2. **Cache everything**: Aproveite caches do GitHub
3. **Fail fast**: Checks rápidos primeiro
4. **Monitor costs**: Atenção aos minutos do GitHub Actions
5. **Security first**: Nunca commite secrets

### Docker

1. **Multi-stage builds**: Minimize image size
2. **Non-root user**: Security
3. **Layer caching**: Optimize build time
4. **Health checks**: Always include
5. **.dockerignore**: Exclude unnecessary files

---

## Próximos Passos

### Melhorias Futuras

- [ ] Benchmark performance tests
- [ ] Integration tests com database
- [ ] Smoke tests em produção
- [ ] Auto-changelog generation
- [ ] Automated version bumping
- [ ] Slack/Discord notifications
- [ ] Sentry integration
- [ ] Monitoring dashboards

### Recursos Adicionais

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Suporte

Para questões sobre CI/CD:

1. Verifique os logs do GitHub Actions
2. Consulte este documento
3. Abra uma issue no GitHub
4. Entre em contato com o time DevOps

---

**Última atualização:** 2025-11-19
**Versão do documento:** 1.0
