FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta (Railway injeta a variável PORT)
EXPOSE ${PORT:-8000}

# Script de inicialização que usa a variável PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

