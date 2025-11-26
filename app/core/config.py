from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://pbc_user:pbc_password@db:5432/pbc_db"
    SECRET_KEY: str = "seu-secret-key-super-secreto-aqui-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

