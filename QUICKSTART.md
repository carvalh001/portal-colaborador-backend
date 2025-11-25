# 🚀 Guia Rápido - Portal de Benefícios do Colaborador

## ⚡ Iniciar em 3 Passos

### 1. Subir o Backend

```bash
cd portal-colaborador-backend
docker compose up --build
```

### 2. Acessar a API

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Fazer Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}'
```

## 👥 Usuários Pré-cadastrados

| Username | Senha | Papel | Descrição |
|----------|-------|-------|-----------|
| `maria` | `123456` | COLABORADOR | Usuária padrão com acesso limitado |
| `joao` | `123456` | GESTOR_RH | Gestor de RH com acesso ampliado |
| `admin` | `admin123` | ADMIN | Administrador com acesso total |

## 📡 Endpoints Principais

```bash
# Autenticação
POST   /api/auth/login          # Login
POST   /api/auth/register       # Registro
GET    /api/auth/me             # Meus dados

# Usuários
GET    /api/users               # Listar usuários (RH/Admin)
GET    /api/users/me            # Meus dados
PUT    /api/users/me            # Atualizar meus dados
PATCH  /api/users/{id}/role     # Alterar papel (Admin)

# Benefícios
GET    /api/benefits            # Listar benefícios
GET    /api/users/{id}/benefits # Benefícios de um usuário

# Mensagens
GET    /api/messages            # Listar mensagens
POST   /api/messages            # Criar mensagem
PATCH  /api/messages/{id}       # Atualizar status (RH/Admin)

# Logs
GET    /api/logs                # Listar logs (RH/Admin)
```

## 🔐 Como Usar

### 1. Login e Obter Token

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}'

# Salvar o token retornado
TOKEN="seu_token_aqui"
```

### 2. Usar o Token nas Requisições

```bash
# Exemplo: Ver meus dados
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Exemplo: Ver meus benefícios
curl -X GET http://localhost:8000/api/benefits \
  -H "Authorization: Bearer $TOKEN"
```

## 🎯 Exemplos Rápidos

### Como Colaborador

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

# Ver meus benefícios
curl -X GET http://localhost:8000/api/benefits \
  -H "Authorization: Bearer $TOKEN" | jq

# Enviar mensagem ao RH
curl -X POST http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Dúvida", "conteudo": "Preciso de ajuda com meus benefícios"}' | jq
```

### Como Gestor RH

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "senha": "123456"}' | jq -r '.access_token')

# Ver todos os colaboradores
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN" | jq

# Ver mensagens pendentes
curl -X GET "http://localhost:8000/api/messages?status=PENDENTE" \
  -H "Authorization: Bearer $TOKEN" | jq

# Ver logs do sistema
curl -X GET http://localhost:8000/api/logs \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Como Admin

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "senha": "admin123"}' | jq -r '.access_token')

# Promover usuário a Gestor RH
curl -X PATCH http://localhost:8000/api/users/4/role \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"papel": "GESTOR_RH"}' | jq
```

## 🛠️ Comandos Docker Úteis

```bash
# Iniciar
docker compose up -d

# Ver logs
docker compose logs -f backend

# Parar
docker compose down

# Resetar banco de dados (limpa tudo)
docker compose down -v
docker compose up --build

# Acessar banco de dados
docker exec -it pbc_postgres psql -U pbc_user -d pbc_db

# Reiniciar apenas o backend
docker compose restart backend
```

## 📊 Status da API

```bash
# Health check
curl http://localhost:8000/health

# Informações da API
curl http://localhost:8000/
```

## 🔍 Debugging

### Ver logs do backend em tempo real

```bash
docker compose logs -f backend
```

### Ver logs do banco de dados

```bash
docker compose logs -f db
```

### Verificar se os containers estão rodando

```bash
docker compose ps
```

### Acessar o container do backend

```bash
docker exec -it pbc_backend /bin/bash
```

### Verificar conexão com o banco

```bash
docker exec -it pbc_postgres psql -U pbc_user -d pbc_db -c "SELECT COUNT(*) FROM users;"
```

## 🐛 Problemas Comuns

### "Connection refused"
- Certifique-se de que o Docker está rodando
- Execute: `docker compose up --build`

### "401 Unauthorized"
- Token expirado ou inválido
- Faça login novamente para obter novo token

### "403 Forbidden"
- Usuário sem permissão para acessar o recurso
- Verifique o papel do usuário

### Porta 8000 já em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Resetar tudo
```bash
docker compose down -v
docker system prune -a
docker compose up --build
```

## 📚 Documentação Completa

- [README.md](README.md) - Documentação completa do projeto
- [TESTING.md](TESTING.md) - Guia de testes detalhado
- [INTEGRATION.md](INTEGRATION.md) - Guia de integração com frontend
- [Swagger Docs](http://localhost:8000/docs) - Documentação interativa da API

## 💡 Dicas

1. Use o Swagger UI (http://localhost:8000/docs) para testar a API visualmente
2. Instale `jq` para formatar JSON: `curl ... | jq`
3. Salve o token em uma variável para facilitar: `TOKEN="..."`
4. Use o PostgreSQL diretamente se necessário: `docker exec -it pbc_postgres psql -U pbc_user -d pbc_db`

## 🎓 Objetivo do Projeto

Este é um projeto **didático** para treinamento em QA e Segurança. Ele contém vulnerabilidades intencionais para fins educacionais. **NÃO USE EM PRODUÇÃO**.

---

**Desenvolvido para Assert Consulting Labs - Workshop de QA + Segurança**

