# 📮 Guia Postman - Portal de Benefícios do Colaborador

## 🚀 Como Importar a Collection

1. Abra o Postman
2. Clique em **"Import"** (canto superior esquerdo)
3. Selecione o arquivo `PBC_API.postman_collection.json`
4. A collection será importada com todas as requisições configuradas

## 🔧 Configuração Inicial

### Variáveis da Collection

A collection já vem com as seguintes variáveis configuradas:

- **`base_url`**: `http://localhost:8000` (URL base da API)
- **`access_token`**: (será preenchido automaticamente após login)

### Como Alterar a URL Base

Se sua API estiver rodando em outra porta ou host:

1. Clique com o botão direito na collection **"PBC API"**
2. Selecione **"Edit"**
3. Vá na aba **"Variables"**
4. Altere o valor de `base_url`

## 🔐 Fluxo de Autenticação

### 1. Fazer Login

Escolha um dos logins disponíveis na pasta **"1. Autenticação"**:

- **Maria Santos** (COLABORADOR)
  - Username: `maria`
  - Senha: `123456`

- **João Silva** (GESTOR_RH)
  - Username: `joao`
  - Senha: `123456`

- **Ana Admin** (ADMIN)
  - Username: `admin`
  - Senha: `admin123`

⚠️ **Importante**: Ao fazer login com sucesso, o token JWT é **automaticamente salvo** na variável `access_token` via script de teste.

### 2. Usar o Token

Após o login, todas as demais requisições usarão automaticamente o token salvo! 🎉

A collection já está configurada com **Bearer Token** no nível da collection, então você não precisa copiar/colar tokens manualmente.

### 3. Trocar de Usuário

Para testar com outro perfil:
1. Execute o login correspondente (ex: "Login - Admin")
2. O token será atualizado automaticamente
3. Todas as próximas requisições usarão o novo token

## 📁 Estrutura da Collection

### 0. Health Check
- Verificar se a API está rodando
- Acessar documentação Swagger

### 1. Autenticação
- Login com diferentes perfis
- Registrar novo usuário
- Obter dados do usuário autenticado

### 2. Usuários
- Listar usuários (com filtros)
- Obter detalhes de usuário
- Atualizar dados pessoais
- Alterar papel de usuário (apenas ADMIN)

### 3. Benefícios
- Listar benefícios
- Filtrar por categoria/status
- Ver benefícios de colaborador específico

### 4. Mensagens
- Listar mensagens
- Criar nova mensagem
- Atualizar status (GESTOR_RH/ADMIN)

### 5. Logs de Eventos
- Listar logs de auditoria
- Filtrar por tipo de evento
- Filtrar por período

## 🎯 Exemplos de Uso

### Cenário 1: Colaborador Consulta Benefícios

```
1. Execute "Login - Colaborador (Maria)"
2. Execute "Listar Meus Benefícios"
3. Execute "Criar Nova Mensagem"
```

### Cenário 2: Gestor RH Consulta Colaboradores

```
1. Execute "Login - Gestor RH (João)"
2. Execute "Listar Todos os Usuários"
3. Execute "Listar Benefícios do Usuário" (altere ID para 1)
4. Execute "Listar Todas as Mensagens"
```

### Cenário 3: Admin Gerencia Papéis

```
1. Execute "Login - Admin (Ana)"
2. Execute "Listar Todos os Usuários"
3. Execute "Alterar Papel do Usuário" (altere papel para GESTOR_RH)
4. Execute "Listar Todos os Logs" (verá o evento CHANGE_ROLE)
```

## 🔍 Testando Vulnerabilidades

### 🛡️ Pilar: Autenticação

**1. Senhas Fracas**
```
Request: POST /api/auth/register
Body: { "senha": "123" }
Esperado: Sistema aceita senha fraca
```

**2. Mensagens de Erro Informativas**
```
Request: POST /api/auth/login
Body: { "username": "maria", "senha": "errada" }
Esperado: Mensagem revela que o username existe
```

### 🛡️ Pilar: Autorização (IDOR)

**Navegação Direta**
```
1. Login como Maria (COLABORADOR)
2. GET /api/users/2 (tentar acessar dados de outro usuário)
Esperado: Sistema permite acesso (IDOR)
```

### 🛡️ Pilar: Sessão

**Timeout de Sessão**
```
1. Faça login
2. Aguarde 30 minutos (ou mais)
3. Tente acessar /api/users/me
Esperado: Token ainda válido (sem expiração adequada)
```

**Reutilização de Token**
```
1. Faça login e copie o token
2. Execute POST /api/auth/logout (se implementado)
3. Use o token antigo em outra requisição
Esperado: Token ainda funciona (sem revogação)
```

### 🛡️ Pilar: Manipulação

**XSS em Mensagens**
```
Request: POST /api/messages
Body: {
  "titulo": "<script>alert('XSS')</script>",
  "conteudo": "Teste de XSS"
}
Esperado: Sistema aceita e armazena script
```

**Validação Apenas no Cliente**
```
Request: PUT /api/users/me
Body: { "email": "email-invalido" }
Esperado: Sistema aceita email inválido (bypass validação)
```

**Exposição de Dados Sensíveis**
```
Request: GET /api/users/1
Esperado: Retorna CPF completo, dados bancários, etc.
```

### 🛡️ Pilar: Auditoria

**Verificar Logs**
```
1. Execute alguma ação sensível (ex: atualizar dados bancários)
2. GET /api/logs
3. Verifique se a ação foi registrada
```

## 🧪 Cenários de Teste Automatizado

O Postman permite criar testes automatizados. Exemplos:

### Teste 1: Login Bem-Sucedido

```javascript
pm.test("Login retorna 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Resposta contém token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access_token');
});

pm.test("Token é salvo na variável", function () {
    pm.expect(pm.collectionVariables.get("access_token")).to.not.be.empty;
});
```

### Teste 2: Acesso Negado sem Autenticação

```javascript
pm.test("Retorna 401 sem token", function () {
    pm.response.to.have.status(401);
});
```

### Teste 3: RBAC - Admin pode alterar papéis

```javascript
pm.test("Admin pode alterar papel", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.papel).to.eql("GESTOR_RH");
});
```

## 🎓 Dicas Profissionais

### 1. Usar Environments

Crie environments separados para:
- **Local**: `http://localhost:8000`
- **Docker**: `http://localhost:8000`
- **Produção**: `https://api.seudominio.com`

### 2. Organizar Testes

Crie uma pasta "Testes de Segurança" separada com requests específicos para cada vulnerabilidade.

### 3. Newman (CLI)

Execute a collection via linha de comando:

```bash
# Instalar Newman
npm install -g newman

# Executar collection
newman run PBC_API.postman_collection.json

# Com environment
newman run PBC_API.postman_collection.json -e environment.json
```

### 4. Exportar Resultados

```bash
newman run PBC_API.postman_collection.json --reporters cli,json --reporter-json-export results.json
```

## 🔗 Links Úteis

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📝 Notas de Segurança

⚠️ **Este é um sistema didático intencionalmente vulnerável!**

As vulnerabilidades implementadas são para fins educacionais:
- Senhas fracas aceitas
- Tokens com expiração longa
- Ausência de CSRF protection
- Mensagens de erro verbosas
- Falta de sanitização (XSS)
- IDOR em alguns endpoints
- Validação apenas no cliente

**NÃO use este código em produção!**

## 🎯 Objetivos do Workshop

Usar esta collection para:
1. **Identificar** vulnerabilidades reais
2. **Especificar** casos de teste de segurança
3. **Classificar** testes por pilar e tipo
4. **Automatizar** verificações com Newman
5. **Documentar** findings em Azure DevOps

---

**Boa diversão explorando vulnerabilidades! 🔓🎓**

