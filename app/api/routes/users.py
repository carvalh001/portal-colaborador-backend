from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.user import user_crud
from app.crud.benefit import benefit_crud
from app.crud.log_event import log_event_crud
from app.schemas.user import UserResponse, UserUpdate, UserRoleUpdate
from app.schemas.benefit import BenefitResponse
from app.api.deps import get_current_user, require_role
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


@router.get("/me", response_model=UserResponse)
def get_my_info(
    current_user: User = Depends(get_current_user)
):
    """Retorna informações do usuário autenticado"""
    return user_to_response(current_user)


@router.put("/me", response_model=UserResponse)
def update_my_info(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza dados do usuário autenticado"""
    # Atualizar usuário
    updated_user = user_crud.update(db, current_user.id, user_data.model_dump(exclude_unset=True))
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Registrar log de atualização
    # ⚠️ VULNERABILIDADE (TC-AUDIT-001): Log genérico, sem detalhes
    # Falta: quais campos alterados, valores antigos/novos, IP origem
    try:
        log_event_crud.create(db, {
            "user_id": current_user.id,
            "event_type": "UPDATE_DATA",
            "description": "Dados atualizados"  # Muito genérico!
        })
    except:
        pass
    
    return user_to_response(updated_user)


@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_role(["GESTOR_RH", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Lista usuários (apenas GESTOR_RH ou ADMIN)"""
    users = user_crud.get_multi(
        db, 
        skip=skip, 
        limit=limit,
        role=role,
        is_active=is_active,
        search=search
    )
    
    return [user_to_response(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(require_role(["GESTOR_RH", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um usuário específico (apenas GESTOR_RH ou ADMIN)"""
    user = user_crud.get_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user_to_response(user)


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db)
):
    """Atualiza papel de um usuário (apenas ADMIN)"""
    # Validar papel
    valid_roles = ["COLABORADOR", "GESTOR_RH", "ADMIN"]
    if role_data.papel not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Papel inválido. Deve ser um de: {', '.join(valid_roles)}"
        )
    
    user = user_crud.get_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    old_role = user.role.value
    updated_user = user_crud.update_role(db, user_id, role_data.papel)
    
    # Registrar log de mudança de papel
    # ⚠️ VULNERABILIDADE PARCIAL: Log tem info, mas falta IP, justificativa
    try:
        log_event_crud.create(db, {
            "user_id": user_id,
            "event_type": "CHANGE_ROLE",
            "description": f"Papel alterado de {old_role} para {role_data.papel}"
            # Falta: quem alterou, IP origem, justificativa
        })
    except:
        pass
    
    return user_to_response(updated_user)


@router.get("/{user_id}/benefits", response_model=List[BenefitResponse])
def get_user_benefits(
    user_id: int,
    current_user: User = Depends(require_role(["GESTOR_RH", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Lista benefícios de um usuário específico (apenas GESTOR_RH ou ADMIN)"""
    # Verificar se o usuário existe
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    benefits = benefit_crud.get_by_user_id(db, user_id)
    
    return [
        {
            "id": benefit.id,
            "userId": benefit.user_id,
            "nome": benefit.name,
            "categoria": benefit.category,
            "status": benefit.status,
            "valor": benefit.value or "",
            "descricao": benefit.description or ""
        }
        for benefit in benefits
    ]

