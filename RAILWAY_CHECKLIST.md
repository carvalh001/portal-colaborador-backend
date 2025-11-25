# ✅ Railway Deploy Checklist

Checklist passo a passo para deploy bem-sucedido no Railway.

---

## 🔴 **PROBLEMA ATUAL: Healthcheck Falhando**

### **Sintoma:**
```
Attempt #1 failed with service unavailable
...
1/1 replicas never became healthy!
```

### **Causa Raiz:**
1. ❌ Variável `DATABASE_URL` não configurada
2. ❌ Variável `SECRET_KEY` não configurada  
3. ❌ Backend não consegue iniciar sem essas variáveis

---

## 📋 **Passo a Passo para Resolver**

### **✅ Passo 1: Adicionar PostgreSQL**

```bash
# No Railway Dashboard:
1. Abra seu projeto backend
2. Clique em "+ New"
3. Selecione "Database" → "PostgreSQL"
4. Aguarde ~30 segundos para provisionar
5. Verifique se o status está "Running" (verde)
```

**⚠️ Importante**: Sem o PostgreSQL, o backend **NÃO VAI FUNCIONAR**!

---

### **✅ Passo 2: Configurar Variáveis Obrigatórias**

```bash
# No Railway Dashboard → Seu Backend Service → Variables

Adicione TODAS estas variáveis:
```

#### **1. DATABASE_URL** (automática se PostgreSQL foi adicionado)
```bash
DATABASE_URL = ${{Postgres.DATABASE_URL}}
```

**Se não aparecer automaticamente:**
1. Clique em "New Variable"
2. Variable Reference: Selecione "Postgres" → "DATABASE_URL"
3. Salvar

#### **2. SECRET_KEY** (você precisa gerar!)
```bash
# No seu terminal local, execute:
python generate_secret.py

# OU:
python -c "import secrets; print(secrets.token_hex(32))"

# Copie a chave gerada (64 caracteres)
# Exemplo: f3a8b9c2d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0

# No Railway Variables, adicione:
SECRET_KEY = [cole aqui a chave gerada]
```

#### **3. CORS_ORIGINS**
```bash
CORS_ORIGINS = https://lab.assert.com.br
```

**Ou para permitir tudo (apenas para teste):**
```bash
CORS_ORIGINS = *
```

#### **4. ACCESS_TOKEN_EXPIRE_MINUTES**
```bash
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

### **✅ Passo 3: Verificar Todas as Variáveis**

Seu painel de Variables deve ter **NO MÍNIMO** estas 4 variáveis:

```
✅ DATABASE_URL = ${{Postgres.DATABASE_URL}}
✅ SECRET_KEY = [sua chave de 64 caracteres]
✅ CORS_ORIGINS = https://lab.assert.com.br
✅ ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**⚠️ Se faltar QUALQUER UMA, o deploy vai falhar!**

---

### **✅ Passo 4: Fazer Redeploy**

```bash
# No Railway Dashboard → Seu Backend Service:
1. Vá em "Settings"
2. Role até "Deploy Trigger"
3. Clique em "Redeploy"
4. Aguarde o build
```

---

### **✅ Passo 5: Verificar Logs**

```bash
# No Railway Dashboard → Seu Backend Service → Logs

Procure por estas mensagens:
✅ "Iniciando aplicação..."
✅ "Criando tabelas no banco de dados..."
✅ "Verificando necessidade de seed..."
✅ "Banco de dados populado com sucesso!"
✅ "Aplicação iniciada com sucesso!"
✅ "Uvicorn running on http://0.0.0.0:XXXX"

Se aparecer estas mensagens = SUCESSO! ✅
```

**❌ Se aparecer erros:**
- Copie os logs completos
- Veja a seção "Erros Comuns" abaixo

---

### **✅ Passo 6: Testar Healthcheck**

```bash
# Acesse (substitua pela sua URL do Railway):
https://sua-url-backend.up.railway.app/health

# Deve retornar:
{
  "status": "healthy"
}

# Se retornar isso = SUCESSO! ✅
```

---

### **✅ Passo 7: Testar Swagger**

```bash
# Acesse:
https://sua-url-backend.up.railway.app/docs

# Deve mostrar toda a documentação da API
# Se mostrar = SUCESSO! ✅
```

---

### **✅ Passo 8: Testar Login**

```bash
# No Swagger ou via curl:
curl -X POST https://sua-url-backend.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"maria","senha":"123456"}'

# Deve retornar um token JWT
# Se retornar = SUCESSO! ✅
```

---

## 🚨 **Erros Comuns e Soluções**

### **Erro 1: "relation 'users' does not exist"**

**Causa**: Tabelas não foram criadas

**Solução:**
```bash
1. Verificar se DATABASE_URL está correta
2. Verificar logs: deve ter "Criando tabelas no banco de dados..."
3. Se não tiver, fazer redeploy
4. Se ainda não funcionar, deletar PostgreSQL e criar novo
```

---

### **Erro 2: "could not connect to server"**

**Causa**: PostgreSQL não está acessível

**Solução:**
```bash
1. Verificar se PostgreSQL está "Running" (não "Crashed")
2. Verificar se DATABASE_URL = ${{Postgres.DATABASE_URL}}
3. Fazer redeploy do backend
```

---

### **Erro 3: "SECRET_KEY must be provided"**

**Causa**: SECRET_KEY não foi configurada

**Solução:**
```bash
1. Gerar chave: python generate_secret.py
2. Adicionar em Variables: SECRET_KEY = [chave gerada]
3. Fazer redeploy
```

---

### **Erro 4: Healthcheck continua falhando**

**Causa**: Backend não está iniciando

**Solução:**
```bash
1. Verificar TODAS as 4 variáveis obrigatórias estão presentes
2. Ver logs completos (copiar últimas 100 linhas)
3. Procurar por erros em vermelho nos logs
4. Verificar se PostgreSQL está "Running"
```

---

## 📊 **Template de Variáveis (Copie e Cole)**

```bash
# No Railway Variables, adicione exatamente assim:

# 1. Database (referência ao PostgreSQL)
DATABASE_URL = ${{Postgres.DATABASE_URL}}

# 2. Security (gere sua própria chave!)
SECRET_KEY = [GERE AQUI: python -c "import secrets; print(secrets.token_hex(32))"]

# 3. CORS
CORS_ORIGINS = https://lab.assert.com.br

# 4. Token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 5. Opcional (para debug)
DEBUG = False
ENVIRONMENT = production
```

---

## 🎯 **Ordem Correta de Deploy**

```
1. ✅ Fazer push do código corrigido (Dockerfile atualizado)
2. ✅ Criar projeto no Railway
3. ✅ Deploy do backend (vai falhar - é esperado!)
4. ✅ Adicionar PostgreSQL
5. ✅ Configurar as 4 variáveis obrigatórias
6. ✅ Fazer Redeploy
7. ✅ Verificar logs
8. ✅ Testar /health
9. ✅ Configurar domínio customizado (opcional)
```

---

## 🔍 **Como Saber se Está Tudo Certo**

### **Checklist Final:**

- [ ] PostgreSQL está "Running" (verde)
- [ ] 4 variáveis configuradas (DATABASE_URL, SECRET_KEY, CORS_ORIGINS, ACCESS_TOKEN_EXPIRE_MINUTES)
- [ ] Deploy concluído sem erros
- [ ] Logs mostram "Aplicação iniciada com sucesso!"
- [ ] `/health` retorna `{"status":"healthy"}`
- [ ] `/docs` mostra o Swagger
- [ ] Login funciona (maria/123456)

**Se TODOS estiverem ✅ = Deploy bem-sucedido! 🎉**

---

## 🆘 **Ainda Está com Problemas?**

### **Copie estes logs e me envie:**

```bash
# 1. Logs do Backend (últimas 50 linhas)
Railway → Backend Service → Logs

# 2. Variáveis configuradas (sem mostrar valores sensíveis!)
Railway → Backend Service → Variables → Liste quais estão presentes

# 3. Status do PostgreSQL
Railway → PostgreSQL Service → Status

# 4. Erro específico
Copie a mensagem de erro completa
```

---

## 💡 **Dicas Importantes**

### **1. PostgreSQL DEVE estar rodando ANTES do backend**
Se o PostgreSQL estiver "Crashed", o backend nunca vai funcionar.

### **2. SECRET_KEY deve ser ÚNICA e SEGURA**
NÃO use exemplos da documentação! Gere sua própria.

### **3. Sem as 4 variáveis, o backend NÃO inicia**
Verifique 2x, 3x se todas estão lá.

### **4. Railway leva ~1-2 minutos para aplicar mudanças**
Após configurar variáveis, aguarde o redeploy automático.

### **5. Use o domínio temporário (.up.railway.app) primeiro**
Só configure domínio customizado depois que tudo funcionar.

---

## 📞 **Links Úteis**

- **Railway Dashboard**: https://railway.app/dashboard
- **Railway Docs - Healthcheck**: https://docs.railway.app/guides/healthchecks
- **Railway Docs - Variables**: https://docs.railway.app/develop/variables
- **Railway Discord**: https://discord.gg/railway

---

## 🎉 **Após Resolver**

Quando tudo funcionar:

1. ✅ Configurar domínio customizado: `lab-backend.assert.com.br`
2. ✅ Fazer deploy do frontend
3. ✅ Testar integração completa
4. ✅ Celebrar! 🎊

---

**Última atualização**: Novembro 2025  
**Status**: Dockerfile corrigido para usar variável PORT do Railway

