.PHONY: help install install-dev test lint format type-check clean build docker-build docker-run docs serve-docs

# Default Python version
PYTHON := python3
PIP := $(PYTHON) -m pip

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Market Manipulation Lab - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# Installation
# ============================================================================

install: ## Install package in production mode
	@echo "$(BLUE)Installing package...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[viz]"
	@echo "$(GREEN)Installation complete!$(NC)"

install-dev: ## Install package with development dependencies
	@echo "$(BLUE)Installing package with dev dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev,viz]"
	@echo "$(GREEN)Development installation complete!$(NC)"

install-all: ## Install all optional dependencies
	@echo "$(BLUE)Installing all dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev,viz]"
	$(PIP) install sphinx sphinx-rtd-theme myst-parser
	@echo "$(GREEN)All dependencies installed!$(NC)"

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run linter (ruff)
	@echo "$(BLUE)Running linter...$(NC)"
	ruff check src/ tests/
	@echo "$(GREEN)Linting complete!$(NC)"

lint-fix: ## Run linter and auto-fix issues
	@echo "$(BLUE)Running linter with auto-fix...$(NC)"
	ruff check --fix src/ tests/
	@echo "$(GREEN)Linting and fixes complete!$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format src/ tests/
	@echo "$(GREEN)Formatting complete!$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code format...$(NC)"
	ruff format --check src/ tests/
	@echo "$(GREEN)Format check complete!$(NC)"

type-check: ## Run type checker (mypy)
	@echo "$(BLUE)Running type checker...$(NC)"
	mypy src/market_lab/
	@echo "$(GREEN)Type checking complete!$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	safety check || true
	bandit -r src/ || true
	@echo "$(GREEN)Security checks complete!$(NC)"

# ============================================================================
# Testing
# ============================================================================

test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v
	@echo "$(GREEN)Tests complete!$(NC)"

test-cov: ## Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest tests/ --cov=market_lab --cov-report=html --cov-report=term-missing -v
	@echo "$(GREEN)Tests complete! Coverage report: htmlcov/index.html$(NC)"

test-fast: ## Run tests without coverage (fast)
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest tests/ -v --no-cov
	@echo "$(GREEN)Fast tests complete!$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	pytest-watch tests/

# ============================================================================
# Quality Gates (like CI)
# ============================================================================

ci: lint format-check type-check test-cov ## Run all CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

pre-commit: format lint test-fast ## Quick checks before commit
	@echo "$(GREEN)Pre-commit checks passed!$(NC)"

# ============================================================================
# Documentation
# ============================================================================

docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	mkdir -p docs/source docs/build
	cd docs && sphinx-build -b html source build/html
	@echo "$(GREEN)Documentation built! Open: docs/build/html/index.html$(NC)"

docs-serve: ## Build and serve documentation
	@echo "$(BLUE)Serving documentation...$(NC)"
	cd docs/build/html && $(PYTHON) -m http.server 8000
	@echo "$(GREEN)Documentation available at http://localhost:8000$(NC)"

docs-clean: ## Clean documentation build
	@echo "$(BLUE)Cleaning documentation...$(NC)"
	rm -rf docs/build/
	@echo "$(GREEN)Documentation cleaned!$(NC)"

# ============================================================================
# Building and Distribution
# ============================================================================

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)Build complete! Check dist/ directory$(NC)"

build-check: build ## Build and check distribution
	@echo "$(BLUE)Checking distribution...$(NC)"
	twine check dist/*
	@echo "$(GREEN)Distribution check complete!$(NC)"

upload-test: build-check ## Upload to TestPyPI
	@echo "$(YELLOW)Uploading to TestPyPI...$(NC)"
	twine upload --repository testpypi dist/*
	@echo "$(GREEN)Uploaded to TestPyPI!$(NC)"

upload: build-check ## Upload to PyPI (use with caution!)
	@echo "$(RED)WARNING: This will upload to PyPI!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		twine upload dist/*; \
		echo "$(GREEN)Uploaded to PyPI!$(NC)"; \
	fi

# ============================================================================
# Docker
# ============================================================================

docker-build: ## Build all Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker build --target runtime -t market-lab:latest .
	docker build --target development -t market-lab:dev .
	docker build --target jupyter -t market-lab:jupyter .
	docker build --target dashboard -t market-lab:dashboard .
	@echo "$(GREEN)Docker images built!$(NC)"

docker-build-runtime: ## Build runtime Docker image only
	@echo "$(BLUE)Building runtime Docker image...$(NC)"
	docker build --target runtime -t market-lab:latest .
	@echo "$(GREEN)Runtime image built!$(NC)"

docker-run: ## Run Docker container
	@echo "$(BLUE)Running Docker container...$(NC)"
	docker run --rm -v $(PWD)/results:/app/results market-lab:latest

docker-dev: ## Run development Docker container
	@echo "$(BLUE)Starting development container...$(NC)"
	docker run --rm -it -v $(PWD)/src:/app/src -v $(PWD)/tests:/app/tests market-lab:dev

docker-jupyter: ## Run Jupyter container
	@echo "$(BLUE)Starting Jupyter Lab...$(NC)"
	docker run --rm -p 8888:8888 -v $(PWD)/notebooks:/app/notebooks market-lab:jupyter

docker-dashboard: ## Run dashboard container
	@echo "$(BLUE)Starting dashboard...$(NC)"
	docker run --rm -p 8501:8501 market-lab:dashboard

docker-compose-up: ## Start all services with docker-compose
	@echo "$(BLUE)Starting all services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "  Jupyter: http://localhost:8888"
	@echo "  Dashboard: http://localhost:8501"

docker-compose-down: ## Stop all services
	@echo "$(BLUE)Stopping all services...$(NC)"
	docker-compose down
	@echo "$(GREEN)Services stopped!$(NC)"

# ============================================================================
# Cleaning
# ============================================================================

clean: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-all: clean docs-clean ## Clean everything including docs
	@echo "$(BLUE)Deep cleaning...$(NC)"
	rm -rf .venv/
	rm -rf venv/
	rm -rf env/
	@echo "$(GREEN)Deep cleanup complete!$(NC)"

# ============================================================================
# Development Utilities
# ============================================================================

dev-setup: install-dev ## Setup development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run tests: make test"
	@echo "  2. Check code quality: make lint"
	@echo "  3. Format code: make format"

run-experiment: ## Run random walk experiment
	@echo "$(BLUE)Running random walk experiment...$(NC)"
	$(PYTHON) -m market_lab.experiments.random_walk

run-agents: ## Run agents simulation
	@echo "$(BLUE)Running agents simulation...$(NC)"
	$(PYTHON) run_agents.py

jupyter: ## Start Jupyter Lab locally
	@echo "$(BLUE)Starting Jupyter Lab...$(NC)"
	jupyter lab

dashboard: ## Start Streamlit dashboard locally
	@echo "$(BLUE)Starting dashboard...$(NC)"
	streamlit run dashboard/app.py

# ============================================================================
# Release Management
# ============================================================================

version: ## Show current version
	@echo "Current version: $(shell grep 'version = ' pyproject.toml | cut -d'"' -f2)"

bump-patch: ## Bump patch version (0.1.0 -> 0.1.1)
	@echo "$(BLUE)Bumping patch version...$(NC)"
	@echo "$(YELLOW)TODO: Implement version bumping$(NC)"

bump-minor: ## Bump minor version (0.1.0 -> 0.2.0)
	@echo "$(BLUE)Bumping minor version...$(NC)"
	@echo "$(YELLOW)TODO: Implement version bumping$(NC)"

bump-major: ## Bump major version (0.1.0 -> 1.0.0)
	@echo "$(BLUE)Bumping major version...$(NC)"
	@echo "$(YELLOW)TODO: Implement version bumping$(NC)"

# ============================================================================
# Information
# ============================================================================

info: ## Show project information
	@echo "$(BLUE)Project Information$(NC)"
	@echo ""
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Pip version: $(shell $(PIP) --version)"
	@echo "Project version: $(shell grep 'version = ' pyproject.toml | cut -d'"' -f2)"
	@echo ""
	@echo "Installed packages:"
	@$(PIP) list | grep -E 'market-lab|pytest|ruff|mypy'
