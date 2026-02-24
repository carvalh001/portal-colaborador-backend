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

# Local (docker-compose): espera Postgres se DB_HOST estiver definido. Railway: sobe direto (PORT injetado).
CMD ["sh", "-c", "if [ -n \"$DB_HOST\" ]; then until pg_isready -h $DB_HOST -p ${DB_PORT:-5432} -U pbc_user 2>/dev/null; do echo 'Aguardando Postgres...'; sleep 2; done; fi; exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

