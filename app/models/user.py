from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    COLABORADOR = "COLABORADOR"
    GESTOR_RH = "GESTOR_RH"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.COLABORADOR, nullable=False)
    cpf = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    bank_name = Column(String, nullable=True)
    bank_agency = Column(String, nullable=True)
    bank_account = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    benefits = relationship("Benefit", back_populates="user")
    messages = relationship("Message", back_populates="user")
    log_events = relationship("LogEvent", back_populates="user")

