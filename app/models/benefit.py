from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Benefit(Base):
    __tablename__ = "benefits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # ALIMENTACAO, SAUDE, OUTROS
    status = Column(String, nullable=False)  # ATIVO, SUSPENSO
    value = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="benefits")

