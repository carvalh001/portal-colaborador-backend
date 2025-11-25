# 📚 Índice de Documentação - Portal de Benefícios do Colaborador

Documentação completa do projeto organizada por tópicos.

## 🎯 Para Começar

### [QUICKSTART.md](QUICKSTART.md) ⭐ **COMECE AQUI**
Guia rápido para subir o projeto e fazer as primeiras requisições. Ideal para começar em minutos.

**Inclui:**
- Como subir o backend em 3 passos
- Usuários pré-cadastrados
- Exemplos de login e requisições básicas
- Comandos Docker úteis
- Troubleshooting

---

## 📖 Documentação Principal

### [README.md](README.md)
Documentação completa do projeto com visão geral, arquitetura e instruções detalhadas.

**Inclui:**
- Descrição do projeto e objetivos
- Stack tecnológico
- Estrutura de pastas
- Como rodar com Docker
- Usuários de teste
- Endpoints principais
- Papéis e permissões (RBAC)
- Comandos úteis
- Notas de segurança

---

## 🧪 Testes

### [TESTING.md](TESTING.md)
Guia completo de testes com exemplos práticos de todas as funcionalidades.

**Inclui:**
- Exemplos de requisições para cada endpoint
- Cenários de teste por perfil (Colaborador, Gestor RH, Admin)
- Testes de segurança
- Testes de autenticação e autorização
- Testes de RBAC
- Exemplos com curl
- Dicas para usar Postman/Insomnia

**Use este guia para:**
- Testar manualmente a API
- Criar casos de teste
- Explorar vulnerabilidades intencionais
- Validar comportamento de cada endpoint

---

## 🔗 Integração

### [INTEGRATION.md](INTEGRATION.md)
Guia de integração frontend React/TypeScript com o backend FastAPI.

**Inclui:**
- Estrutura de dados (TypeScript interfaces)
- Serviço de autenticação completo
- Cliente HTTP com autenticação automática
- Serviços para cada módulo (users, benefits, messages, logs)
- Exemplos de componentes React
- Hook customizado useAuth
- Componente de rota protegida
- Tratamento de erros
- Configuração de CORS

**Use este guia para:**
- Integrar o frontend com o backend
- Criar serviços de API no frontend
- Implementar autenticação JWT
- Criar rotas protegidas
- Gerenciar estado de autenticação

---

## 📂 Estrutura do Projeto

```
portal-colaborador-backend/
├── app/
│   ├── api/                    # Rotas da API
│   │   ├── deps.py            # Dependências (auth, RBAC)
│   │   └── routes/            # Endpoints
│   │       ├── auth.py        # Login, registro
│   │       ├── users.py       # Gestão de usuários
│   │       ├── benefits.py    # Benefícios
│   │       ├── messages.py    # Mensagens
│   │       └── logs.py        # Logs
│   ├── core/                  # Configurações centrais
│   │   ├── config.py         # Settings
│   │   ├── database.py       # SQLAlchemy
│   │   └── security.py       # JWT, hash
│   ├── crud/                  # Operações de banco
│   ├── models/                # Modelos SQLAlchemy
│   ├── schemas/               # Schemas Pydantic
│   ├── main.py               # App principal
│   └── seed.py               # Dados iniciais
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── Documentação/
    ├── README.md             # Principal
    ├── QUICKSTART.md         # Guia rápido
    ├── TESTING.md            # Testes
    ├── INTEGRATION.md        # Integração
    └── DOCS_INDEX.md         # Este arquivo
```

---

## 🔐 Autenticação e Segurança

### Fluxo de Autenticação

1. **Login**: `POST /api/auth/login`
   - Enviar username e senha
   - Receber JWT token + dados do usuário
   - Salvar token (localStorage no frontend)

2. **Requisições Autenticadas**
   - Incluir header: `Authorization: Bearer {token}`
   - Token válido por 24 horas

3. **Verificação de Papel (RBAC)**
   - COLABORADOR: acesso aos próprios dados
   - GESTOR_RH: acesso a colaboradores, mensagens, logs
   - ADMIN: acesso total + gestão de papéis

### Endpoints de Autenticação

```
POST   /api/auth/login       # Login
POST   /api/auth/register    # Registro (sempre COLABORADOR)
GET    /api/auth/me          # Dados do usuário autenticado
```

---

## 📡 Mapa de Endpoints

### Usuários (`/api/users`)

```
GET    /api/users                    # Listar (GESTOR_RH/ADMIN)
GET    /api/users/{id}               # Detalhes (GESTOR_RH/ADMIN)
GET    /api/users/me                 # Meus dados
PUT    /api/users/me                 # Atualizar meus dados
PATCH  /api/users/{id}/role          # Alterar papel (ADMIN)
GET    /api/users/{id}/benefits      # Benefícios do usuário (GESTOR_RH/ADMIN)
```

### Benefícios (`/api/benefits`)

```
GET    /api/benefits                 # Listar benefícios
                                     # COLABORADOR: só seus
                                     # GESTOR_RH/ADMIN: todos (com filtros)
```

### Mensagens (`/api/messages`)

```
GET    /api/messages                 # Listar mensagens
                                     # COLABORADOR: só suas
                                     # GESTOR_RH/ADMIN: todas (com filtros)
POST   /api/messages                 # Criar mensagem
PATCH  /api/messages/{id}            # Atualizar status (GESTOR_RH/ADMIN)
```

### Logs (`/api/logs`)

```
GET    /api/logs                     # Listar logs (GESTOR_RH/ADMIN)
                                     # Filtros: user_id, event_type, datas
```

---

## 🎭 Perfis de Usuário

### COLABORADOR
**Usuários de teste:** maria, carlos, fernanda

**Pode acessar:**
- Próprios dados pessoais
- Próprios benefícios
- Próprias mensagens
- Enviar mensagens ao RH
- Atualizar próprios dados

**Não pode acessar:**
- Dados de outros usuários
- Lista de usuários
- Logs do sistema
- Alterar papéis

### GESTOR_RH
**Usuário de teste:** joao

**Pode acessar:**
- Tudo que COLABORADOR pode
- Lista de todos os usuários
- Detalhes de qualquer usuário
- Benefícios de qualquer usuário
- Todas as mensagens
- Atualizar status de mensagens
- Logs do sistema

**Não pode acessar:**
- Alterar papéis de usuários

### ADMIN
**Usuário de teste:** admin

**Pode acessar:**
- Tudo que GESTOR_RH pode
- Alterar papéis de usuários
- Acesso total ao sistema

---

## 🛠️ Comandos Essenciais

### Iniciar o projeto
```bash
cd portal-colaborador-backend
docker compose up --build
```

### Ver logs
```bash
docker compose logs -f backend
```

### Parar o projeto
```bash
docker compose down
```

### Resetar banco de dados
```bash
docker compose down -v
docker compose up --build
```

### Acessar banco de dados
```bash
docker exec -it pbc_postgres psql -U pbc_user -d pbc_db
```

---

## 📊 Dados de Teste

### Usuários Pré-cadastrados

| ID | Nome | Username | Senha | Papel | Status |
|----|------|----------|-------|-------|--------|
| 1 | Maria Santos | maria | 123456 | COLABORADOR | ATIVO |
| 2 | João Silva | joao | 123456 | GESTOR_RH | ATIVO |
| 3 | Ana Admin | admin | admin123 | ADMIN | ATIVO |
| 4 | Carlos Oliveira | carlos | 123456 | COLABORADOR | ATIVO |
| 5 | Fernanda Lima | fernanda | 123456 | COLABORADOR | INATIVO |

### Dados Bancários (todos os usuários possuem)
- Banco, Agência, Conta

### Benefícios Pré-cadastrados
- Vale Refeição, Plano de Saúde, Vale Transporte, etc.
- Distribuídos entre os usuários
- Categorias: ALIMENTACAO, SAUDE, OUTROS
- Status: ATIVO, SUSPENSO

### Mensagens Pré-cadastradas
- 3 mensagens de exemplo
- Status: PENDENTE, EM_ANALISE

### Logs Pré-cadastrados
- ~10 eventos de teste
- Tipos: LOGIN, UPDATE_DATA, NEW_MESSAGE, CHANGE_ROLE

---

## 🔍 URLs Importantes

- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **PostgreSQL**: localhost:5432

---

## 🎓 Vulnerabilidades Intencionais

Este projeto contém vulnerabilidades para fins didáticos:

### Autenticação
- ✗ Senhas fracas aceitas sem validação
- ✗ Mensagens de erro informativas (revelam se usuário existe)
- ✗ Sem limite de tentativas de login

### Sessão
- ✗ Tokens com expiração longa (24h)
- ✗ Sem mecanismo de revogação de tokens
- ✗ Logout apenas no cliente

### Auditoria
- ✗ Logs básicos (não capturam todas as ações)
- ✗ Sem logs de falhas de autenticação detalhados

### Manipulação
- ✗ Sem sanitização completa de inputs
- ✗ Potencial para injection em queries (SQLAlchemy protege, mas...)
- ✗ Sem proteção CSRF
- ✗ Exposição de dados sensíveis (CPF completo)
- ✗ Validação apenas no backend (permitindo burla por cliente)

### Outros
- ✗ Sem rate limiting
- ✗ Sem proteção contra força bruta
- ✗ Secret key hardcoded no docker-compose

**IMPORTANTE**: Use estas vulnerabilidades apenas para fins educacionais em ambiente controlado.

---

## 📚 Recursos Adicionais

### Documentação de Ferramentas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Docker](https://docs.docker.com/)

### Tutoriais Relacionados

- FastAPI Authentication: https://fastapi.tiangolo.com/tutorial/security/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/en/14/orm/
- Docker Compose: https://docs.docker.com/compose/

---

## 🤝 Contribuindo

Este é um projeto educacional. Se encontrar bugs ou tiver sugestões:

1. Documente o comportamento observado
2. Proponha a correção ou melhoria
3. Lembre-se que algumas "falhas" são intencionais

---

## 📧 Suporte

Para dúvidas sobre o projeto:

1. Consulte esta documentação
2. Verifique o [QUICKSTART.md](QUICKSTART.md) para problemas comuns
3. Use o Swagger UI para testar endpoints
4. Verifique os logs: `docker compose logs -f`

---

## ⚖️ Licença e Uso

Este projeto foi desenvolvido para fins educacionais como parte do **Assert Consulting Labs - Workshop de QA + Segurança**.

**⚠️ ATENÇÃO**: Este projeto contém vulnerabilidades intencionais e **NÃO DEVE SER USADO EM AMBIENTE DE PRODUÇÃO**.

---

**Última atualização**: Novembro 2025  
**Versão**: 1.0.0  
**Desenvolvido por**: Assert Consulting Labs

