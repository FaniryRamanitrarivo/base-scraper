FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ---- system deps minimal browsers ----
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# ---- install deps first (cache Docker) ----
COPY pyproject.toml ./
COPY README.md ./ 

RUN pip install --upgrade pip

# copier code AVANT install package
COPY app ./app

# install package + tests deps
RUN pip install .[dev]

# 👉 seulement si tu utilises Playwright réellement
# sinon SUPPRIME cette ligne
# RUN playwright install --with-deps chromium

# ---- security ----
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]