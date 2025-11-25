# Portal de Benefícios do Colaborador (PBC) - Backend API

API Backend para o Portal de Benefícios do Colaborador, uma aplicação didática desenvolvida para workshops de QA + Segurança.

## 📋 Descrição

O PBC é um sistema interno de RH que permite:

- **Colaboradores**: Visualizar benefícios, atualizar dados pessoais, enviar mensagens ao RH
- **Gestores de RH**: Visualizar colaboradores, gerenciar mensagens, acessar logs
- **Administradores**: Gerenciar usuários, alterar papéis, acesso total ao sistema

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **Alembic** - Gerenciamento de migrações (opcional)
- **JWT (python-jose)** - Autenticação com tokens
- **Passlib** - Hash de senhas
- **Docker & Docker Compose** - Containerização

## 📁 Estrutura do Projeto

```
portal-colaborador-backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependências de autenticação
│   │   └── routes/              # Rotas da API
│   │       ├── auth.py          # Autenticação
│   │       ├── users.py         # Usuários
│   │       ├── benefits.py      # Benefícios
│   │       ├── messages.py      # Mensagens
│   │       └── logs.py          # Logs
│   ├── core/
│   │   ├── config.py            # Configurações
│   │   ├── database.py          # Conexão com banco
│   │   └── security.py          # Segurança (JWT, hash)
│   ├── crud/                    # Operações de banco
│   ├── models/                  # Modelos SQLAlchemy
│   ├── schemas/                 # Schemas Pydantic
│   ├── main.py                  # Aplicação principal
│   └── seed.py                  # Dados iniciais
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── env.example
└── README.md
```

## 🐳 Como Rodar com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Passo a Passo

1. **Clone o repositório** (se ainda não clonou):

```bash
cd portal-colaborador-backend
```

2. **Configure as variáveis de ambiente** (opcional):

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o .env se necessário (as configurações padrão já funcionam)
```

3. **Inicie os containers**:

```bash
docker compose up --build
```

4. **Acesse a API**:

- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

## 👥 Usuários de Teste

O sistema é populado automaticamente com os seguintes usuários:

| Nome | Username | Senha | Papel |
|------|----------|-------|-------|
| Maria Santos | `maria` | `123456` | COLABORADOR |
| João Silva | `joao` | `123456` | GESTOR_RH |
| Ana Admin | `admin` | `admin123` | ADMIN |
| Carlos Oliveira | `carlos` | `123456` | COLABORADOR |
| Fernanda Lima | `fernanda` | `123456` | COLABORADOR (Inativo) |

## 📡 Endpoints Principais

### Autenticação

```
POST   /api/auth/login      # Login (retorna JWT)
POST   /api/auth/register   # Registro de novo usuário
GET    /api/auth/me         # Dados do usuário autenticado
```

### Usuários

```
GET    /api/users/me                # Dados do usuário autenticado
PUT    /api/users/me                # Atualizar dados do usuário
GET    /api/users                   # Listar usuários (GESTOR_RH/ADMIN)
GET    /api/users/{user_id}         # Detalhes de um usuário (GESTOR_RH/ADMIN)
PATCH  /api/users/{user_id}/role    # Atualizar papel (ADMIN)
```

### Benefícios

```
GET    /api/benefits                      # Listar benefícios
GET    /api/users/{user_id}/benefits      # Benefícios de um usuário (GESTOR_RH/ADMIN)
```

### Mensagens

```
GET    /api/messages           # Listar mensagens
POST   /api/messages           # Criar nova mensagem
PATCH  /api/messages/{id}      # Atualizar status (GESTOR_RH/ADMIN)
```

### Logs

```
GET    /api/logs              # Listar logs de eventos (GESTOR_RH/ADMIN)
```

## 🔐 Autenticação

A API usa autenticação JWT (JSON Web Tokens). Para acessar endpoints protegidos:

1. Faça login em `/api/auth/login`
2. Receba o `access_token` na resposta
3. Inclua o token no header das requisições:

```
Authorization: Bearer {access_token}
```

## 🎯 Papéis e Permissões (RBAC)

- **COLABORADOR**: Acesso aos próprios dados, benefícios e mensagens
- **GESTOR_RH**: Acesso a todos os colaboradores, mensagens e logs
- **ADMIN**: Acesso total, incluindo gerenciamento de papéis

## 🔧 Comandos Úteis

### Parar os containers

```bash
docker compose down
```

### Ver logs do backend

```bash
docker compose logs -f backend
```

### Ver logs do banco de dados

```bash
docker compose logs -f db
```

### Resetar o banco de dados

```bash
docker compose down -v
docker compose up --build
```

### Acessar o PostgreSQL diretamente

```bash
docker exec -it pbc_postgres psql -U pbc_user -d pbc_db
```

## 🧪 Testando a API

### Exemplo de Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "senha": "123456"
  }'
```

### Exemplo de Acesso Protegido

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer {seu_token_aqui}"
```

## 📚 Documentação Automática

A API possui documentação interativa automática gerada pelo FastAPI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Você pode testar todos os endpoints diretamente pelo navegador usando o Swagger UI.

## ⚠️ Observações de Segurança

**IMPORTANTE**: Esta aplicação foi desenvolvida para fins **didáticos** e contém vulnerabilidades intencionais para treinamento em segurança. **NÃO USE EM PRODUÇÃO**.

Algumas características propositais:
- Senhas fracas aceitas sem validação de complexidade
- Mensagens de erro detalhadas
- Validações básicas (não exaustivas)
- Sem proteção CSRF
- Sem rate limiting
- Sanitização básica de inputs

## 🎓 Objetivo Pedagógico

Este projeto faz parte de um laboratório de segurança onde as seguintes vulnerabilidades podem ser exploradas:

- **Autenticação**: Mensagens de erro informativas, senhas fracas
- **Sessão**: Timeout, logout, reutilização de tokens
- **Auditoria**: Logs incompletos
- **Manipulação**: XSS, Injection, CSRF, exposição de dados, navegação direta
- **Validação**: Validação apenas no cliente

## 📝 Desenvolvimento

### Rodar sem Docker (para desenvolvimento)

1. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

```bash
export DATABASE_URL="postgresql+psycopg2://pbc_user:pbc_password@localhost:5432/pbc_db"
export SECRET_KEY="seu-secret-key-aqui"
```

4. Inicie o servidor:

```bash
uvicorn app.main:app --reload
```

## 📧 Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido para Assert Consulting Labs - Workshop de QA + Segurança**

