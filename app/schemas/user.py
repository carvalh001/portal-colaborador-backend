from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class DadosBancarios(BaseModel):
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None


class UserBase(BaseModel):
    nome: str
    email: EmailStr
    username: str
    cpf: str
    telefone: str


class UserCreate(UserBase):
    senha: str
    dadosBancarios: Optional[DadosBancarios] = None


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    dadosBancarios: Optional[DadosBancarios] = None


class UserResponse(UserBase):
    id: int
    papel: str
    status: str
    dadosBancarios: DadosBancarios
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    senha: str


class UserRoleUpdate(BaseModel):
    papel: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

