# 🌐 Configuração de CORS - Hosts Permitidos Fixos

## ✅ Mudança Implementada

Os hosts permitidos para CORS agora estão **fixos no código**, eliminando a necessidade de configuração manual no Railway.

---

## 🔧 Como Funciona

### Arquivo: `app/core/config.py`

```python
# Hosts permitidos fixos (sempre incluídos)
ALLOWED_HOSTS_FIXED: List[str] = [
    "https://lab.assert.com.br",      # Produção
    "http://localhost:5173",           # Desenvolvimento local
    "http://127.0.0.1:5173",           # Desenvolvimento local
    "http://localhost:8080",           # Vite preview local
    "http://127.0.0.1:8080",           # Vite preview local
]

@property
def cors_origins_list(self) -> List[str]:
    # Combinar hosts fixos com hosts da variável de ambiente
    env_origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # Criar conjunto para evitar duplicatas
    all_origins = set(self.ALLOWED_HOSTS_FIXED + env_origins)
    
    return list(all_origins)
```

---

## ✨ Vantagens

### ✅ Sem Erros de Configuração
- Não precisa configurar `CORS_ORIGINS` no Railway
- Impossível errar com barras finais (`/`)
- Funciona automaticamente em dev e produção

### ✅ Manutenção Simplificada
- Hosts de produção no código (versionados)
- Mudanças rastreadas no Git
- Menos variáveis de ambiente para gerenciar

### ✅ Desenvolvimento Mais Fácil
- Funciona out-of-the-box no localhost
- Não precisa configurar `.env` para dev local
- Preview local (`npm run preview`) também funciona

---

## 🚀 Hosts Permitidos (Fixos no Código)

| Host | Uso |
|------|-----|
| `https://lab.assert.com.br` | 🌐 **Produção** (Railway) |
| `http://localhost:5173` | 💻 Dev local (`npm run dev`) |
| `http://127.0.0.1:5173` | 💻 Dev local (IP) |
| `http://localhost:8080` | 🔍 Preview local (`npm run preview`) |
| `http://127.0.0.1:8080` | 🔍 Preview local (IP) |

---

## 🔧 Adicionar Hosts Extras (Opcional)

Se precisar adicionar **outros hosts** (staging, testes, etc.), use a variável de ambiente:

### No `.env` (local):
```bash
CORS_ORIGINS=http://staging.assert.com.br,http://test.assert.com.br
```

### No Railway (produção):
```bash
CORS_ORIGINS=http://staging.assert.com.br
```

**Os hosts extras serão combinados com os hosts fixos automaticamente.**

---

## 🧪 Como Testar

### 1️⃣ Backend Local
```bash
cd portal-colaborador-backend
uvicorn app.main:app --reload
```

Verifique os logs na inicialização - deve mostrar os CORS origins permitidos.

### 2️⃣ Frontend Local
```bash
cd portal-colabora-lovable
npm run dev
```

Acesse `http://localhost:5173` e tente fazer login - deve funcionar sem erro de CORS.

### 3️⃣ Produção
Acesse `https://lab.assert.com.br` e faça login - deve funcionar automaticamente.

---

## 📋 Variáveis de Ambiente Necessárias

### Backend (Railway)

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=0d4c1ea26e620ee3fd5cb44115b01ce4bf7f197ce4043c68f9a068ea89e53067
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
ENVIRONMENT=production
```

**✅ `CORS_ORIGINS` NÃO é mais necessária!**

---

## 🆘 Troubleshooting

### ❌ Ainda recebo erro de CORS

**1. Verifique o domínio no erro:**
```
Access to fetch at 'https://lab-backend.assert.com.br/api/...'
from origin 'https://lab.assert.com.br' has been blocked by CORS policy
```

**2. Certifique-se que o código atualizado foi deployado:**
```bash
git log -1 --oneline  # Veja o último commit
```

**3. Force redeploy no Railway:**
- Railway Dashboard → Deployments → "Redeploy"

### ❌ Funciona local mas não em produção

**Verifique se o domínio está correto no código:**
```python
"https://lab.assert.com.br",  # ✅ Sem barra final
```

**Não:**
```python
"https://lab.assert.com.br/",  # ❌ Com barra final
```

---

## 🔄 Adicionar Novo Domínio de Produção

Para adicionar um **novo domínio permanente**, edite `app/core/config.py`:

```python
ALLOWED_HOSTS_FIXED: List[str] = [
    "https://lab.assert.com.br",
    "https://novo-dominio.com",        # ← Adicione aqui
    "http://localhost:5173",
    # ...
]
```

Depois:
```bash
git add app/core/config.py
git commit -m "feat: adicionar novo domínio ao CORS"
git push origin main
```

Railway fará redeploy automaticamente! 🚀

---

## ✅ Status

✅ CORS configurado com hosts fixos  
✅ Produção (`https://lab.assert.com.br`) incluída  
✅ Desenvolvimento local funcionando  
✅ Preview local funcionando  
✅ Sem necessidade de variáveis extras  

**Pronto para usar! 🎉**

