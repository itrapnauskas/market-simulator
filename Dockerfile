# Multi-stage Dockerfile for Market Manipulation Lab
# Optimized for size and security

# ============================================================================
# Stage 1: Builder - Compile dependencies and install packages
# ============================================================================
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Copy only dependency files first (for better caching)
WORKDIR /build
COPY pyproject.toml ./

# Install dependencies
RUN pip install -e ".[viz]"

# Copy source code
COPY src/ ./src/
COPY README.md ./

# Install the package
RUN pip install -e .


# ============================================================================
# Stage 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.12-slim AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    MARKET_LAB_HOME="/app"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For matplotlib
    libfreetype6 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r marketlab && useradd -r -g marketlab marketlab

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
WORKDIR /app
COPY --from=builder /build/src ./src
COPY --from=builder /build/README.md ./

# Create directories for data and results
RUN mkdir -p /app/data /app/results /app/logs && \
    chown -R marketlab:marketlab /app

# Switch to non-root user
USER marketlab

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import market_lab; print('OK')" || exit 1

# Set working directory
WORKDIR /app

# Default command
CMD ["python", "-m", "market_lab.experiments.random_walk"]


# ============================================================================
# Stage 3: Development - With dev tools
# ============================================================================
FROM runtime AS development

USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dev dependencies
COPY --from=builder /opt/venv /opt/venv

# Install additional dev packages
RUN pip install pytest pytest-cov ruff mypy jupyter ipython

# Copy tests
COPY tests/ ./tests/

USER marketlab

# Default command for dev
CMD ["/bin/bash"]


# ============================================================================
# Stage 4: Jupyter - For interactive notebooks
# ============================================================================
FROM development AS jupyter

USER root

# Install Jupyter and extensions
RUN pip install \
    jupyterlab \
    notebook \
    ipywidgets \
    plotly \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Copy notebooks
COPY notebooks/ ./notebooks/

# Expose Jupyter port
EXPOSE 8888

USER marketlab

# Set working directory
WORKDIR /app/notebooks

# Default command
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]


# ============================================================================
# Stage 5: Dashboard - For Streamlit/web interface
# ============================================================================
FROM runtime AS dashboard

USER root

# Install dashboard dependencies
RUN pip install streamlit plotly pandas

# Copy dashboard code
COPY dashboard/ ./dashboard/

# Expose Streamlit port
EXPOSE 8501

USER marketlab

# Set working directory
WORKDIR /app/dashboard

# Default command
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]


# ============================================================================
# Build instructions:
# ============================================================================
# Production:
#   docker build --target runtime -t market-lab:latest .
#
# Development:
#   docker build --target development -t market-lab:dev .
#
# Jupyter:
#   docker build --target jupyter -t market-lab:jupyter .
#
# Dashboard:
#   docker build --target dashboard -t market-lab:dashboard .
#
# Run examples:
#   docker run -v $(pwd)/results:/app/results market-lab:latest
#   docker run -p 8888:8888 market-lab:jupyter
#   docker run -p 8501:8501 market-lab:dashboard
# ============================================================================
