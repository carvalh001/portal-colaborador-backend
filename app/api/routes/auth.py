from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.crud.user import user_crud
from app.crud.log_event import log_event_crud
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse, DadosBancarios
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


def user_to_response(user: User) -> dict:
    """Converte User model para formato de resposta da API"""
    return {
        "id": user.id,
        "nome": user.name,
        "email": user.email,
        "username": user.username,
        "cpf": user.cpf,
        "papel": user.role.value,
        "telefone": user.phone,
        "status": "ATIVO" if user.is_active else "INATIVO",
        "dadosBancarios": {
            "banco": user.bank_name or "",
            "agencia": user.bank_agency or "",
            "conta": user.bank_account or ""
        }
    }


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Endpoint de login - retorna JWT token"""
    # Buscar usuário por username ou email
    user = user_crud.get_by_username_or_email(db, credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Usuário '{credentials.username}' não encontrado"
        )
    
    if not verify_password(credentials.senha, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Criar token JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Registrar log de login (opcional, mas vamos adicionar)
    try:
        log_event_crud.create(db, {
            "user_id": user.id,
            "event_type": "LOGIN",
            "description": f"Login realizado por {user.name}"
        })
    except:
        pass  # Não falhar login se log falhar
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_to_response(user)
    }


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Endpoint de registro - cria novo usuário com papel COLABORADOR"""
    # Verificar se email já existe
    existing_user = user_crud.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Verificar se username já existe
    existing_user = user_crud.get_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já cadastrado"
        )
    
    # Criar usuário (sempre com papel COLABORADOR no registro)
    user_dict = user_data.model_dump()
    user_dict["papel"] = "COLABORADOR"  # Forçar papel COLABORADOR
    
    user = user_crud.create(db, user_dict)
    
    return user_to_response(user)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Retorna informações do usuário autenticado"""
    return user_to_response(current_user)

