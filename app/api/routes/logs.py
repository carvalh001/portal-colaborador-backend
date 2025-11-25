from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.crud.log_event import log_event_crud
from app.crud.user import user_crud
from app.schemas.log_event import LogEventResponse
from app.api.deps import require_role
from app.models.user import User

router = APIRouter()


def log_to_response(log, db: Session) -> dict:
    """Converte LogEvent model para formato de resposta da API"""
    usuario_nome = ""
    if log.user_id:
        user = user_crud.get_by_id(db, log.user_id)
        if user:
            usuario_nome = user.name
    
    return {
        "id": log.id,
        "dataHora": log.created_at.isoformat(),
        "usuario": usuario_nome,
        "userId": log.user_id,  # Retorna None se não houver user_id
        "tipoEvento": log.event_type,
        "descricao": log.description
    }


@router.get("", response_model=List[LogEventResponse])
def list_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = None,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(require_role(["GESTOR_RH", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Lista logs de eventos (apenas GESTOR_RH ou ADMIN)"""
    # Converter strings de data para datetime se fornecidas
    start_datetime = None
    end_datetime = None
    
    if start_date:
        try:
            start_datetime = datetime.fromisoformat(start_date)
        except:
            pass
    
    if end_date:
        try:
            end_datetime = datetime.fromisoformat(end_date)
        except:
            pass
    
    logs = log_event_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        event_type=event_type,
        start_date=start_datetime,
        end_date=end_datetime
    )
    
    return [log_to_response(log, db) for log in logs]

