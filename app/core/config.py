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
    # CORS: SEMPRE definir no .env (dev e produção). Nada fixo no código.
    CORS_ORIGINS: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        # Normalizar: remover barra final (o browser envia Origin sem barra)
        def normalize_origin(o: str) -> str:
            o = o.strip()
            return o.rstrip("/") if o else o

        origins = [normalize_origin(o) for o in self.CORS_ORIGINS.split(",") if o.strip()]
        if not origins:
            import warnings
            warnings.warn(
                "CORS_ORIGINS está vazio. Defina no .env (ex.: http://localhost:5173 para dev).",
                UserWarning,
                stacklevel=2,
            )
        return list(origins)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

