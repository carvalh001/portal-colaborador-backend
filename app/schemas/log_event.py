from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogEventBase(BaseModel):
    tipoEvento: str
    descricao: str


class LogEventResponse(LogEventBase):
    id: int
    dataHora: datetime
    userId: Optional[int] = None
    usuario: Optional[str] = None
    
    class Config:
        from_attributes = True

