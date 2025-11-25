# 🚂 Deploy no Railway - lab.assert.com.br

Guia completo para deploy do Portal de Benefícios do Colaborador no domínio **lab.assert.com.br**.

---

## 🎯 Configuração Final

- **Backend**: `https://lab-backend.assert.com.br`
- **Frontend**: `https://lab.assert.com.br`
- **Swagger Docs**: `https://lab-backend.assert.com.br/docs`

---

## 📦 Passo 1: Deploy do Backend

### 1.1 Criar Projeto no Railway

1. Acesse https://railway.app/
2. Login com GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Selecione: `carvalh001/portal-colaborador-backend`
5. Railway detecta automaticamente o `Dockerfile` ✅

### 1.2 Adicionar PostgreSQL

1. No projeto do backend, clique **+ New**
2. Selecione **Database** → **PostgreSQL**
3. Railway provisiona automaticamente
4. A variável `DATABASE_URL` é criada automaticamente

### 1.3 Configurar Variáveis de Ambiente

Vá em **Variables** e adicione:

```bash
# Database (gerada automaticamente pelo Railway)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security (IMPORTANTE: gerar chave segura)
SECRET_KEY=your-super-secret-key-here-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - domínios permitidos
CORS_ORIGINS=https://lab.assert.com.br,http://localhost:8080

# Optional
DEBUG=False
ENVIRONMENT=production
```

**🔑 Para gerar SECRET_KEY segura:**
```bash
# No terminal local:
openssl rand -hex 32
```

### 1.4 Configurar Domínio Customizado

1. Vá em **Settings** → **Networking** → **Public Networking**
2. Clique em **Generate Domain** (Railway gera um domínio temporário)
3. Clique em **Custom Domain**
4. Adicione: `lab-backend.assert.com.br`

**Configuração DNS (no provedor do domínio assert.com.br):**

```
Tipo: CNAME
Nome: lab-backend
Valor: [valor fornecido pelo Railway]
TTL: 3600
```

### 1.5 Verificar Deploy

Acesse: `https://lab-backend.assert.com.br/health`

Resposta esperada:
```json
{
  "status": "healthy"
}
```

Swagger: `https://lab-backend.assert.com.br/docs`

---

## 🎨 Passo 2: Deploy do Frontend

### 2.1 Criar Projeto no Railway

1. **New Project** → **Deploy from GitHub repo**
2. Selecione: `carvalh001/portal-colabora-lovable`
3. Railway detecta Node.js automaticamente ✅

### 2.2 Configurar Variáveis de Ambiente

Vá em **Variables** e adicione:

```bash
VITE_API_BASE_URL=https://lab-backend.assert.com.br/api
```

### 2.3 Configurar Domínio Customizado

1. Vá em **Settings** → **Networking** → **Public Networking**
2. Clique em **Generate Domain**
3. Clique em **Custom Domain**
4. Adicione: `lab.assert.com.br`

**Configuração DNS (no provedor do domínio):**

```
Tipo: CNAME
Nome: lab (ou @)
Valor: [valor fornecido pelo Railway]
TTL: 3600
```

### 2.4 Verificar Deploy

Acesse: `https://lab.assert.com.br`

---

## 🔄 Passo 3: Atualizar CORS no Backend

Depois que o frontend estiver no ar, volte nas **Variables** do backend e atualize:

```bash
CORS_ORIGINS=https://lab.assert.com.br
```

---

## 🧪 Passo 4: Testar Integração

### 4.1 Testar Backend

```bash
# Health check
curl https://lab-backend.assert.com.br/health

# Login
curl -X POST https://lab-backend.assert.com.br/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"maria","senha":"123456"}'
```

### 4.2 Testar Frontend

1. Acesse: `https://lab.assert.com.br`
2. Faça login com:
   - Username: `maria`
   - Senha: `123456`
3. Teste todas as funcionalidades

---

## 📊 Monitoramento

### Logs do Backend

No Railway:
1. Selecione o serviço backend
2. Vá em **Logs**
3. Acompanhe em tempo real

### Logs do Frontend

1. Selecione o serviço frontend
2. Vá em **Logs**

---

## 🔧 Troubleshooting

### ❌ Backend não inicia

**Sintoma:** Service keeps restarting

**Solução:**
1. Verificar logs no Railway
2. Confirmar que `DATABASE_URL` está configurada
3. Verificar se PostgreSQL está online

### ❌ CORS Error no Frontend

**Sintoma:** "Access-Control-Allow-Origin" error

**Solução:**
1. Verificar variável `CORS_ORIGINS` no backend
2. Deve incluir: `https://lab.assert.com.br`
3. Fazer redeploy do backend após alterar

### ❌ Frontend não conecta no backend

**Sintoma:** Network errors / 500

**Solução:**
1. Verificar variável `VITE_API_BASE_URL` no frontend
2. Deve ser: `https://lab-backend.assert.com.br/api`
3. Fazer redeploy do frontend após alterar

### ❌ Banco não popula dados

**Sintoma:** Login não funciona / tabelas vazias

**Solução:**
```bash
# Os dados são populados automaticamente no primeiro deploy
# Para repopular:
1. No Railway, delete o serviço PostgreSQL
2. Crie um novo PostgreSQL
3. Reconnecte ao backend
4. Redeploy do backend
```

### ❌ Domínio customizado não funciona

**Sintoma:** DNS_PROBE_FINISHED_NXDOMAIN

**Solução:**
1. Verificar configuração DNS
2. Aguardar propagação (até 24h)
3. Testar com domínio temporário do Railway primeiro

---

## 🔐 Segurança para Produção

### ⚠️ Este projeto é INTENCIONALMENTE VULNERÁVEL

Para uso em workshops de segurança, as vulnerabilidades são propositais.

**Se for usar em ambiente público:**

1. ✅ Mude todas as senhas padrão
2. ✅ Use SECRET_KEY forte e única
3. ✅ Configure rate limiting
4. ✅ Adicione HTTPS (Railway já inclui)
5. ✅ Configure firewall se necessário
6. ⚠️ **Nunca use dados reais de produção!**

---

## 💰 Custos Estimados

### Railway Pricing

**Plano Developer ($5/mês):**
- $5 de crédito incluído
- Uso adicional cobrado

**Estimativa mensal:**
```
Backend (FastAPI):     ~$3/mês
Frontend (React):      ~$2/mês
PostgreSQL:           ~$4/mês
─────────────────────────────
Total:                ~$9/mês
```

Com plano de $5/mês + crédito, fica ~$4/mês adicional.

---

## 📝 Checklist de Deploy

### Backend ✅
- [ ] Repositório público no GitHub
- [ ] `railway.json` commitado
- [ ] Deploy no Railway
- [ ] PostgreSQL adicionado
- [ ] Variáveis de ambiente configuradas:
  - [ ] `DATABASE_URL`
  - [ ] `SECRET_KEY`
  - [ ] `CORS_ORIGINS`
- [ ] Domínio customizado configurado: `lab-backend.assert.com.br`
- [ ] DNS configurado
- [ ] Health check funcionando: `/health`
- [ ] Swagger funcionando: `/docs`

### Frontend ✅
- [ ] Repositório público no GitHub
- [ ] `railway.json` commitado
- [ ] `nixpacks.toml` commitado
- [ ] `vite.config.ts` com `process.env.PORT`
- [ ] Deploy no Railway
- [ ] Variável `VITE_API_BASE_URL` configurada
- [ ] Domínio customizado configurado: `lab.assert.com.br`
- [ ] DNS configurado
- [ ] Site carregando
- [ ] Login funcionando

### Integração ✅
- [ ] Backend acessível via HTTPS
- [ ] Frontend acessível via HTTPS
- [ ] CORS configurado corretamente
- [ ] Login funciona
- [ ] Todas as páginas carregam
- [ ] API calls funcionando

---

## 🎓 Para Workshop

### Acesso dos Participantes

**URL única para todos:**
- 🌐 **https://lab.assert.com.br**

**Credenciais de teste:**

| Usuário | Username | Senha | Papel |
|---------|----------|-------|-------|
| Maria Santos | `maria` | `123456` | COLABORADOR |
| João Silva | `joao` | `123456` | GESTOR_RH |
| Ana Admin | `admin` | `admin123` | ADMIN |

### Postman Collection

Importar do repositório:
- `portal-colaborador-backend/PBC_API.postman_collection.json`

Configurar variável:
```
base_url = https://lab-backend.assert.com.br
```

---

## 🔗 Links Úteis

- **Frontend**: https://lab.assert.com.br
- **Backend API**: https://lab-backend.assert.com.br/api
- **Swagger Docs**: https://lab-backend.assert.com.br/docs
- **ReDoc**: https://lab-backend.assert.com.br/redoc
- **Health Check**: https://lab-backend.assert.com.br/health

- **Railway Dashboard**: https://railway.app/dashboard
- **Backend Repo**: https://github.com/carvalh001/portal-colaborador-backend
- **Frontend Repo**: https://github.com/carvalh001/portal-colabora-lovable

---

## 📞 Suporte

- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Nos repositórios

---

## 🎉 Conclusão

Após seguir todos os passos:

✅ **Backend rodando em**: `https://lab-backend.assert.com.br`  
✅ **Frontend rodando em**: `https://lab.assert.com.br`  
✅ **Sistema 100% funcional**  
✅ **Pronto para workshops!**

**Tempo estimado de deploy**: 30-45 minutos (incluindo propagação DNS)

---

**Desenvolvido para workshops de QA + Segurança da Assert Consulting** 🎓🔐

