from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, SessionLocal, Base
from app.api.routes import auth, users, benefits, messages, logs, ctf
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


@app.on_event("startup")
def startup_event():
    """Evento executado na inicialização da aplicação"""
    print("Iniciando aplicação...")
    
    # Criar tabelas no banco de dados
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    
    # Executar seed se banco estiver vazio
    print("Verificando necessidade de seed...")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    
    print("Aplicação iniciada com sucesso!")


# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/users", tags=["Usuários"])
app.include_router(benefits.router, prefix="/api/benefits", tags=["Benefícios"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensagens"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
app.include_router(ctf.router, prefix="/api/ctf", tags=["CTF - Capture The Flag"])


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

