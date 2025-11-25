from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.benefit import benefit_crud
from app.schemas.benefit import BenefitResponse
from app.api.deps import get_current_user, require_role
from app.models.user import User

router = APIRouter()


def benefit_to_response(benefit) -> dict:
    """Converte Benefit model para formato de resposta da API"""
    return {
        "id": benefit.id,
        "userId": benefit.user_id,
        "nome": benefit.name,
        "categoria": benefit.category,
        "status": benefit.status,
        "valor": benefit.value or "",
        "descricao": benefit.description or ""
    }


@router.get("", response_model=List[BenefitResponse])
def list_benefits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista benefícios
    - Se COLABORADOR: retorna apenas seus próprios benefícios
    - Se GESTOR_RH ou ADMIN: pode filtrar por user_id ou ver todos
    """
    # Se o usuário é COLABORADOR, forçar filtro pelo seu próprio ID
    if current_user.role.value == "COLABORADOR":
        user_id = current_user.id
    
    benefits = benefit_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        category=category,
        status=status
    )
    
    return [benefit_to_response(benefit) for benefit in benefits]

