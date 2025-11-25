from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CTFDifficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class CTFFlag(Base):
    """Modelo para armazenar flags do CTF"""
    __tablename__ = "ctf_flags"
    
    id = Column(Integer, primary_key=True, index=True)
    flag_hash = Column(String(64), unique=True, nullable=False, index=True)  # SHA256 hash
    difficulty = Column(SQLEnum(CTFDifficulty), nullable=False, index=True)
    points = Column(Integer, nullable=False)
    hint = Column(String(500), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CTFFlag(id={self.id}, difficulty={self.difficulty}, points={self.points})>"


class CTFSubmission(Base):
    """Modelo para armazenar submissões de flags pelos usuários"""
    __tablename__ = "ctf_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(200), nullable=False)
    user_email = Column(String(255), nullable=False, index=True)
    flag_id = Column(Integer, ForeignKey("ctf_flags.id"), nullable=False)
    difficulty = Column(SQLEnum(CTFDifficulty), nullable=False)
    points = Column(Integer, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Constraint: cada usuário pode submeter apenas uma flag por dificuldade
    __table_args__ = (
        UniqueConstraint('user_email', 'difficulty', name='uq_user_difficulty'),
    )
    
    def __repr__(self):
        return f"<CTFSubmission(id={self.id}, user={self.user_name}, difficulty={self.difficulty}, points={self.points})>"

