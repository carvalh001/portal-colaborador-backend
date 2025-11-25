from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://pbc_user:pbc_password@db:5432/pbc_db"
    SECRET_KEY: str = "seu-secret-key-super-secreto-aqui-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    
    # CTF Configuration
    CTF_EASY_FLAGS: int = 10
    CTF_MEDIUM_FLAGS: int = 5
    CTF_HARD_FLAGS: int = 3
    CTF_EASY_POINTS: int = 10
    CTF_MEDIUM_POINTS: int = 20
    CTF_HARD_POINTS: int = 30
    CTF_SECRET_KEY: str = "ctf-secret-validation-key-change-in-production"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

