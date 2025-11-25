from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageBase(BaseModel):
    titulo: str
    conteudo: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    status: str


class MessageResponse(MessageBase):
    id: int
    userId: int
    status: str
    dataHora: datetime
    
    class Config:
        from_attributes = True

