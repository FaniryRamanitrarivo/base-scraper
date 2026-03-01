FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Fixe le dossier des navigateurs pour qu'il soit accessible à tous
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- install deps (Cache Docker) ----
COPY pyproject.toml README.md ./ 
RUN pip install --upgrade pip

# ---- Installation Playwright & Browsers ----
# On le fait AVANT de changer d'utilisateur, mais dans le dossier partagé
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium && \
    chmod -R 775 /ms-playwright

# ---- Copier le code et installer le projet ----
COPY app ./app
RUN pip install .[dev]

# ---- Security ----
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
    
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]