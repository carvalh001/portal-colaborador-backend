from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://pbc_user:pbc_password@db:5432/pbc_db"

    def get_database_url(self) -> str:
        """Retorna DATABASE_URL no formato esperado pelo SQLAlchemy (postgresql+psycopg2)."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://") and "+psycopg2" not in url:
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    SECRET_KEY: str = "seu-secret-key-super-secreto-aqui-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    
    # Hosts permitidos fixos (sempre incluídos)
    ALLOWED_HOSTS_FIXED: List[str] = [
        "https://lab.assert.com.br",           # Produção
        "https://portal-colaboradores.up.railway.app",  # Railway frontend
        "http://localhost:5173",                # Desenvolvimento local
        "http://127.0.0.1:5173",                # Desenvolvimento local
        "http://localhost:8080",                # Vite preview local
        "http://127.0.0.1:8080",               # Vite preview local
    ]
    
    @property
    def cors_origins_list(self) -> List[str]:
        # Normalizar: remover barra final (o browser envia Origin sem barra)
        def normalize_origin(o: str) -> str:
            o = o.strip()
            return o.rstrip("/") if o else o

        # Combinar hosts fixos com hosts da variável de ambiente
        env_origins = [normalize_origin(origin) for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        fixed_normalized = [normalize_origin(o) for o in self.ALLOWED_HOSTS_FIXED]

        # Criar conjunto para evitar duplicatas
        all_origins = set(fixed_normalized + env_origins)
        return list(all_origins)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

