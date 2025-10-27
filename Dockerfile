# ============================================================================
# Dockerfile Multi-Stage para Bot RPA de Memoriales
# Siguiendo Buenas Prácticas de RPA con Python
# ============================================================================

# ----------------------------------------------------------------------------
# STAGE 1: BUILDER - Instalación de dependencias y compilación
# ----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Metadata
LABEL maintainer="Desarrollo <desarrollo@empresa.com>"
LABEL description="Bot RPA para gestión automatizada de memoriales"
LABEL version="1.0.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    unixodbc-dev \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Microsoft ODBC Driver 18 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /build

# Copiar archivos de dependencias
COPY pyproject.toml ./

# Crear virtualenv e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# ----------------------------------------------------------------------------
# STAGE 2: RUNNER - Imagen final optimizada
# ----------------------------------------------------------------------------
FROM python:3.11-slim AS runner

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Instalar solo dependencias runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Microsoft ODBC Driver 18 for SQL Server (runtime)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario sin privilegios para ejecutar la aplicación
RUN groupadd -r botuser && \
    useradd -r -g botuser -u 1001 -m -s /bin/bash botuser

# Crear directorios necesarios con permisos
RUN mkdir -p /app/logs /app/core /app/tests && \
    chown -R botuser:botuser /app

# Copiar virtualenv desde builder
COPY --from=builder --chown=botuser:botuser /opt/venv /opt/venv

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de la aplicación
COPY --chown=botuser:botuser main.py ./
COPY --chown=botuser:botuser logger.py ./
COPY --chown=botuser:botuser config.py ./
COPY --chown=botuser:botuser core/ ./core/
COPY --chown=botuser:botuser cases.json ./

# Cambiar al usuario sin privilegios
USER botuser

# Healthcheck (verificar que Python está disponible)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python --version || exit 1

# Comando por defecto
CMD ["python", "main.py"]

