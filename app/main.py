from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, SessionLocal, Base
from app.api.routes import auth, users, benefits, messages, logs
from app.seed import seed_database

# Criar aplicação FastAPI
app = FastAPI(
    title="Portal de Benefícios do Colaborador API",
    description="API Backend para o Portal de Benefícios do Colaborador (PBC)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _run_db_init():
    """Cria tabelas e executa seed em background (não bloqueia o server)."""
    import time
    from sqlalchemy.exc import OperationalError

    print("Iniciando aplicação (init do banco em background)...")
    last_error = None
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError as e:
            last_error = e
            if attempt == max_retries:
                print("ERRO: não foi possível conectar ao banco após várias tentativas.")
                print("  Dica: no Railway, defina DATABASE_URL (variável do plugin PostgreSQL ou referência ao serviço).")
                detail = getattr(e, "orig", e)
                print(f"  Detalhe: {detail}")
                return
            print(f"Aguardando banco de dados... tentativa {attempt}/{max_retries}")
            time.sleep(2)

    print("Verificando necessidade de seed...")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    print("Aplicação iniciada com sucesso!")


@app.on_event("startup")
def startup_event():
    """Inicia o server logo; create_all + seed rodam em background para /health responder cedo."""
    import threading
    thread = threading.Thread(target=_run_db_init, daemon=True)
    thread.start()


# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/users", tags=["Usuários"])
app.include_router(benefits.router, prefix="/api/benefits", tags=["Benefícios"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensagens"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])


@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "Portal de Benefícios do Colaborador API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}

