FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- install python deps (cache Docker) ----
COPY pyproject.toml README.md ./
RUN pip install --upgrade pip

# Installer dépendances en mode editable (SANS code encore)
RUN pip install -e .[dev]

# ---- Playwright ----
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium && \
    chmod -R 775 /ms-playwright

# ---- créer user ----
RUN useradd -m appuser
USER appuser

# ---- IMPORTANT : on ne copie PAS le code ici ----
# 👉 il sera monté via volume

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]