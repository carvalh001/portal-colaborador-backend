# Guia de Testes da API - PBC

Este documento fornece exemplos práticos de como testar todos os endpoints da API do Portal de Benefícios do Colaborador.

## 🔧 Configuração Inicial

1. Certifique-se de que a API está rodando:
```bash
docker compose up --build
```

2. A API estará disponível em: `http://localhost:8000`
3. Documentação interativa: `http://localhost:8000/docs`

## 📝 Exemplos de Requisições

### 1. Autenticação

#### Login como Colaborador (Maria)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "senha": "123456"
  }'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nome": "Maria Santos",
    "email": "maria.santos@empresa.com.br",
    "username": "maria",
    "cpf": "123.456.789-00",
    "papel": "COLABORADOR",
    "telefone": "(11) 98765-4321",
    "status": "ATIVO",
    "dadosBancarios": {
      "banco": "Banco do Brasil",
      "agencia": "1234-5",
      "conta": "12345-6"
    }
  }
}
```

#### Login como Gestor RH (João)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "senha": "123456"
  }'
```

#### Login como Admin (Ana)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "senha": "admin123"
  }'
```

#### Registrar Novo Usuário

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Colaborador",
    "email": "novo@empresa.com.br",
    "username": "novo",
    "senha": "123456",
    "cpf": "111.222.333-44",
    "telefone": "(11) 99999-9999"
  }'
```

#### Obter Dados do Usuário Autenticado

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### 2. Usuários

**Nota:** Salve o token JWT retornado no login em uma variável para facilitar:

```bash
TOKEN="seu_token_jwt_aqui"
```

#### Listar Todos os Usuários (GESTOR_RH/ADMIN)

```bash
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN"
```

#### Listar Usuários com Filtros

```bash
# Filtrar por papel
curl -X GET "http://localhost:8000/api/users?role=COLABORADOR" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por status
curl -X GET "http://localhost:8000/api/users?is_active=true" \
  -H "Authorization: Bearer $TOKEN"

# Buscar por nome/email
curl -X GET "http://localhost:8000/api/users?search=maria" \
  -H "Authorization: Bearer $TOKEN"
```

#### Obter Detalhes de um Usuário Específico

```bash
curl -X GET http://localhost:8000/api/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

#### Atualizar Meus Dados

```bash
curl -X PUT http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Santos Silva",
    "telefone": "(11) 99999-9999",
    "dadosBancarios": {
      "banco": "Nubank",
      "agencia": "0001",
      "conta": "99999-9"
    }
  }'
```

#### Alterar Papel de um Usuário (ADMIN)

```bash
curl -X PATCH http://localhost:8000/api/users/4/role \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "papel": "GESTOR_RH"
  }'
```

#### Obter Benefícios de um Usuário Específico

```bash
curl -X GET http://localhost:8000/api/users/1/benefits \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Benefícios

#### Listar Meus Benefícios (Colaborador)

```bash
curl -X GET http://localhost:8000/api/benefits \
  -H "Authorization: Bearer $TOKEN"
```

#### Listar Todos os Benefícios com Filtros (GESTOR_RH/ADMIN)

```bash
# Filtrar por usuário
curl -X GET "http://localhost:8000/api/benefits?user_id=1" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por categoria
curl -X GET "http://localhost:8000/api/benefits?category=ALIMENTACAO" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por status
curl -X GET "http://localhost:8000/api/benefits?status=ATIVO" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Mensagens

#### Listar Minhas Mensagens (Colaborador)

```bash
curl -X GET http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN"
```

#### Listar Todas as Mensagens (GESTOR_RH/ADMIN)

```bash
# Todas
curl -X GET http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por usuário
curl -X GET "http://localhost:8000/api/messages?user_id=1" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por status
curl -X GET "http://localhost:8000/api/messages?status=PENDENTE" \
  -H "Authorization: Bearer $TOKEN"
```

#### Criar Nova Mensagem

```bash
curl -X POST http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Solicitação de Férias",
    "conteudo": "Gostaria de solicitar férias para o mês de dezembro. Como devo proceder?"
  }'
```

#### Atualizar Status de uma Mensagem (GESTOR_RH/ADMIN)

```bash
curl -X PATCH http://localhost:8000/api/messages/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "EM_ANALISE"
  }'
```

### 5. Logs

#### Listar Logs (GESTOR_RH/ADMIN)

```bash
curl -X GET http://localhost:8000/api/logs \
  -H "Authorization: Bearer $TOKEN"
```

#### Listar Logs com Filtros

```bash
# Filtrar por usuário
curl -X GET "http://localhost:8000/api/logs?user_id=1" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por tipo de evento
curl -X GET "http://localhost:8000/api/logs?event_type=LOGIN" \
  -H "Authorization: Bearer $TOKEN"

# Paginação
curl -X GET "http://localhost:8000/api/logs?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 Cenários de Teste

### Cenário 1: Fluxo Completo de um Colaborador

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

# 2. Ver meus dados
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 3. Ver meus benefícios
curl -X GET http://localhost:8000/api/benefits \
  -H "Authorization: Bearer $TOKEN"

# 4. Enviar mensagem para RH
curl -X POST http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Dúvida", "conteudo": "Teste de mensagem"}'

# 5. Ver minhas mensagens
curl -X GET http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN"

# 6. Atualizar meus dados
curl -X PUT http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"telefone": "(11) 99999-9999"}'
```

### Cenário 2: Fluxo de um Gestor RH

```bash
# 1. Login como Gestor
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "senha": "123456"}' | jq -r '.access_token')

# 2. Listar todos os colaboradores
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN"

# 3. Ver detalhes de um colaborador
curl -X GET http://localhost:8000/api/users/1 \
  -H "Authorization: Bearer $TOKEN"

# 4. Ver benefícios de um colaborador
curl -X GET http://localhost:8000/api/users/1/benefits \
  -H "Authorization: Bearer $TOKEN"

# 5. Ver todas as mensagens
curl -X GET http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN"

# 6. Atualizar status de uma mensagem
curl -X PATCH http://localhost:8000/api/messages/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "RESPONDIDA"}'

# 7. Ver logs do sistema
curl -X GET http://localhost:8000/api/logs \
  -H "Authorization: Bearer $TOKEN"
```

### Cenário 3: Fluxo de um Admin

```bash
# 1. Login como Admin
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "senha": "admin123"}' | jq -r '.access_token')

# 2. Listar todos os usuários
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN"

# 3. Alterar papel de um usuário
curl -X PATCH http://localhost:8000/api/users/4/role \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"papel": "GESTOR_RH"}'

# 4. Ver logs de mudanças
curl -X GET "http://localhost:8000/api/logs?event_type=CHANGE_ROLE" \
  -H "Authorization: Bearer $TOKEN"
```

## 🛡️ Testes de Segurança

### Teste 1: Acesso sem Autenticação

```bash
# Deve retornar 401
curl -X GET http://localhost:8000/api/users
```

### Teste 2: Acesso com Token Inválido

```bash
# Deve retornar 401
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer token_invalido"
```

### Teste 3: Acesso a Recurso sem Permissão

```bash
# Login como colaborador
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

# Tentar listar todos os usuários (deve retornar 403)
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN"
```

### Teste 4: Login com Credenciais Inválidas

```bash
# Senha incorreta (mensagem informativa - vulnerabilidade)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "senha_errada"}'

# Usuário inexistente (mensagem informativa - vulnerabilidade)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario_inexistente", "senha": "123456"}'
```

## 📊 Usando com Postman/Insomnia

1. Importe a URL base: `http://localhost:8000`
2. Crie uma variável de ambiente para o token
3. Configure o header `Authorization: Bearer {{token}}`
4. Use a documentação Swagger para ver todos os schemas

## 🔍 Dicas

- Use `jq` para formatar as respostas JSON: `curl ... | jq`
- Salve tokens em variáveis para facilitar os testes
- Use o Swagger UI para testar interativamente: http://localhost:8000/docs
- Monitore os logs do backend: `docker compose logs -f backend`

---

**Desenvolvido para Assert Consulting Labs - Workshop de QA + Segurança**

