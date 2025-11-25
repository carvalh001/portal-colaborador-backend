from pydantic import BaseModel
from typing import Optional


class BenefitBase(BaseModel):
    nome: str
    categoria: str
    status: str
    valor: Optional[str] = None
    descricao: Optional[str] = None


class BenefitCreate(BenefitBase):
    userId: int


class BenefitResponse(BenefitBase):
    id: int
    userId: int
    
    class Config:
        from_attributes = True

