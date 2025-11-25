from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.message import message_crud
from app.crud.log_event import log_event_crud
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse
from app.api.deps import get_current_user, require_role
from app.models.user import User

router = APIRouter()


def message_to_response(message) -> dict:
    """Converte Message model para formato de resposta da API"""
    return {
        "id": message.id,
        "userId": message.user_id,
        "titulo": message.title,
        "conteudo": message.content,
        "status": message.status,
        "dataHora": message.created_at.isoformat()
    }


@router.get("", response_model=List[MessageResponse])
def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista mensagens
    - Se COLABORADOR: retorna apenas suas próprias mensagens
    - Se GESTOR_RH ou ADMIN: pode filtrar por user_id ou ver todas
    """
    # Se o usuário é COLABORADOR, forçar filtro pelo seu próprio ID
    if current_user.role.value == "COLABORADOR":
        user_id = current_user.id
    
    messages = message_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        status=status
    )
    
    return [message_to_response(msg) for msg in messages]


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria nova mensagem do usuário autenticado para o RH"""
    # Criar mensagem
    message = message_crud.create(db, message_data.model_dump(), current_user.id)
    
    # Registrar log
    try:
        log_event_crud.create(db, {
            "user_id": current_user.id,
            "event_type": "NEW_MESSAGE",
            "description": f"{current_user.name} enviou mensagem: {message.title}"
        })
    except:
        pass
    
    return message_to_response(message)


@router.patch("/{message_id}", response_model=MessageResponse)
def update_message_status(
    message_id: int,
    message_data: MessageUpdate,
    current_user: User = Depends(require_role(["GESTOR_RH", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Atualiza status da mensagem (apenas GESTOR_RH ou ADMIN)"""
    message = message_crud.update_status(db, message_id, message_data.status)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensagem não encontrada"
        )
    
    return message_to_response(message)

