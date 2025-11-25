# 🚨 Railway Troubleshooting

Guia para resolver problemas comuns de deploy no Railway.

---

## ❌ Erro 1: Backend Healthcheck Falha

### **Sintoma:**
```
Attempt #1 failed with service unavailable
Attempt #2 failed with service unavailable
...
1/1 replicas never became healthy!
```

### **Causa:**
O backend não está conseguindo iniciar corretamente. Geralmente é por:
1. ❌ PostgreSQL não foi adicionado
2. ❌ Variável `DATABASE_URL` não está configurada
3. ❌ Variável `SECRET_KEY` não está configurada
4. ❌ Erro na conexão com o banco

### **Solução Passo a Passo:**

#### 1️⃣ **Adicionar PostgreSQL**

```bash
# No projeto do backend no Railway:
1. Clique "+ New"
2. Selecione "Database" → "PostgreSQL"
3. Aguarde ~30 segundos para provisionar
4. Verifique se está "Running"
```

#### 2️⃣ **Verificar Variável DATABASE_URL**

```bash
# Vá em Variables do backend

# Deve ter automaticamente:
DATABASE_URL = ${{Postgres.DATABASE_URL}}

# Se NÃO tiver, adicione manualmente:
DATABASE_URL = ${{Postgres.DATABASE_URL}}
```

#### 3️⃣ **Adicionar SECRET_KEY**

```bash
# No seu computador local, gere uma chave:
openssl rand -hex 32

# No Railway Variables, adicione:
SECRET_KEY = [cole a chave gerada]
```

#### 4️⃣ **Adicionar Outras Variáveis Obrigatórias**

```bash
# No Railway Variables, adicione:

CORS_ORIGINS = https://lab.assert.com.br
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

#### 5️⃣ **Fazer Redeploy**

```bash
# No Railway:
1. Settings → Deploy Trigger
2. Clique "Redeploy"
3. Aguarde o build
4. Verifique os logs
```

#### 6️⃣ **Verificar Logs**

```bash
# Vá em "Logs" e procure por:

✅ "Iniciando aplicação..."
✅ "Criando tabelas no banco de dados..."
✅ "Banco de dados populado com sucesso!"
✅ "Aplicação iniciada com sucesso!"
✅ "Uvicorn running on http://0.0.0.0:8000"

# Se aparecer erro, copie e investigue
```

---

## ❌ Erro 2: Frontend Build Falha com "bun: command not found"

### **Sintoma:**
```
RUN bun run build
/bin/bash: line 1: bun: command not found
ERROR: failed to build: exit code: 127
```

### **Causa:**
O `nixpacks.toml` estava configurado para usar `bun` mas deveria usar `npm`.

### **Solução:**

#### ✅ **Já corrigido!**

O arquivo `nixpacks.toml` foi atualizado para:

```toml
[phases.setup]
nixPkgs = ["nodejs-18_x"]

[phases.install]
cmds = ["npm install --legacy-peer-deps"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm run preview -- --host 0.0.0.0 --port $PORT"
```

#### **Fazer novo push:**

```bash
cd portal-colabora-lovable
git add .
git commit -m "fix: corrigir build do Railway (usar npm ao invés de bun)"
git push origin main
```

#### **Railway fará redeploy automático!**

---

## ❌ Erro 3: CORS Error no Frontend

### **Sintoma:**
```
Access to fetch at 'https://lab-backend.assert.com.br/api/...' 
has been blocked by CORS policy
```

### **Causa:**
Backend não permite o domínio do frontend.

### **Solução:**

```bash
# No Railway, variáveis do BACKEND:

# Atualize CORS_ORIGINS para incluir o domínio do frontend:
CORS_ORIGINS = https://lab.assert.com.br

# Ou para permitir tudo (apenas para teste):
CORS_ORIGINS = *

# Salve e aguarde redeploy automático
```

---

## ❌ Erro 4: Frontend não conecta no Backend

### **Sintoma:**
- Frontend carrega mas não consegue fazer login
- Erros 500 ou Network Error no console

### **Causa:**
Variável `VITE_API_BASE_URL` não está configurada ou está errada.

### **Solução:**

```bash
# No Railway, variáveis do FRONTEND:

# Adicione:
VITE_API_BASE_URL = https://lab-backend.assert.com.br/api

# IMPORTANTE: 
# - Não esquecer o /api no final
# - Não esquecer o S em https://
# - Usar o domínio customizado, não o domínio .up.railway.app

# Salve e aguarde redeploy automático
```

---

## ❌ Erro 5: Build Timeout

### **Sintoma:**
```
Build timed out after 10 minutes
```

### **Causa:**
Backend ou frontend demorando muito para fazer build.

### **Solução para Backend:**

```bash
# Nada a fazer - Dockerfile é otimizado
# Se continuar, tente aumentar o timeout no Railway:
Settings → Build → Build Timeout → 15 minutes
```

### **Solução para Frontend:**

```bash
# Se o npm install estiver travando:

# Opção 1: Usar cache do Railway (já configurado)
# Opção 2: Limpar cache e tentar novamente:
Settings → Clear Cache → Redeploy
```

---

## ❌ Erro 6: PostgreSQL não conecta

### **Sintoma:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

### **Causa:**
- PostgreSQL não está rodando
- DATABASE_URL está errada
- Network do Railway tem problema

### **Solução:**

```bash
# 1. Verificar se PostgreSQL está Running
No dashboard Railway, veja se o serviço PostgreSQL está "Running"

# 2. Verificar DATABASE_URL
Variables do backend → DATABASE_URL deve ser:
${{Postgres.DATABASE_URL}}

# 3. Se ainda não funcionar, delete e recrie PostgreSQL:
1. Delete o serviço PostgreSQL
2. Crie novo: "+ New" → Database → PostgreSQL
3. Reconnecte ao backend
4. Redeploy do backend
```

---

## ✅ Checklist de Deploy Correto

### Backend:
- [ ] PostgreSQL adicionado e "Running"
- [ ] Variável `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
- [ ] Variável `SECRET_KEY` = (gerada com openssl)
- [ ] Variável `CORS_ORIGINS` = `https://lab.assert.com.br`
- [ ] Variável `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
- [ ] Build concluído com sucesso
- [ ] Healthcheck passou (todos verdes)
- [ ] Logs mostram "Aplicação iniciada com sucesso!"
- [ ] Endpoint `/health` retorna 200

### Frontend:
- [ ] Variável `VITE_API_BASE_URL` = `https://lab-backend.assert.com.br/api`
- [ ] Build concluído com sucesso
- [ ] Site carrega no navegador
- [ ] Login funciona (maria/123456)

---

## 📊 Como Verificar se Está Tudo OK

### 1. Testar Backend:

```bash
# Health check
curl https://lab-backend.assert.com.br/health

# Deve retornar:
{"status":"healthy"}

# Swagger
# Abra no navegador:
https://lab-backend.assert.com.br/docs

# Deve mostrar toda a API
```

### 2. Testar Frontend:

```bash
# Abra no navegador:
https://lab.assert.com.br

# Teste login:
Username: maria
Senha: 123456

# Deve entrar no sistema
```

### 3. Testar Integração:

```bash
# No frontend, abra DevTools (F12)
# Vá em Network
# Faça login
# Veja as requisições para:
https://lab-backend.assert.com.br/api/auth/login

# Deve retornar 200 OK com token
```

---

## 🆘 Precisa de Ajuda?

### Copie os Logs:

1. **Backend Logs:**
   - Railway → Backend Service → Logs
   - Copie as últimas 50 linhas
   - Cole aqui ou em um issue

2. **Frontend Logs:**
   - Railway → Frontend Service → Logs
   - Copie as últimas 50 linhas

3. **Browser Console:**
   - F12 → Console
   - Copie erros vermelhos

### Informações Úteis:

- **Railway Dashboard**: https://railway.app/dashboard
- **Railway Docs**: https://docs.railway.app/
- **Railway Discord**: https://discord.gg/railway

---

## 🎯 Comandos Úteis

### Gerar SECRET_KEY:
```bash
openssl rand -hex 32
```

### Ver logs em tempo real no Railway:
```bash
railway logs
# (requer Railway CLI instalado)
```

### Forçar redeploy:
```bash
Settings → Deploy Trigger → Redeploy
```

### Limpar cache:
```bash
Settings → Clear Cache
```

---

## 📝 Ordem Correta de Deploy

1. **Backend primeiro:**
   - Deploy backend
   - Adicionar PostgreSQL
   - Configurar variáveis
   - Aguardar healthcheck passar
   - Configurar domínio customizado

2. **Frontend depois:**
   - Deploy frontend
   - Configurar variável VITE_API_BASE_URL
   - Aguardar build
   - Configurar domínio customizado

3. **DNS por último:**
   - Configurar CNAME no provedor
   - Aguardar propagação (até 24h)

---

**💡 Dica**: Sempre use os domínios temporários do Railway (`.up.railway.app`) primeiro para testar antes de configurar DNS customizado!

