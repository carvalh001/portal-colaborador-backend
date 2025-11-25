from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.log_event import LogEvent


class LogEventCRUD:
    def get_by_id(self, db: Session, log_id: int) -> Optional[LogEvent]:
        """Busca log por ID"""
        return db.query(LogEvent).filter(LogEvent.id == log_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[int] = None,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[LogEvent]:
        """Lista logs com filtros opcionais"""
        query = db.query(LogEvent)
        
        if user_id:
            query = query.filter(LogEvent.user_id == user_id)
        
        if event_type:
            query = query.filter(LogEvent.event_type == event_type)
        
        if start_date:
            query = query.filter(LogEvent.created_at >= start_date)
        
        if end_date:
            query = query.filter(LogEvent.created_at <= end_date)
        
        return query.order_by(LogEvent.created_at.desc()).offset(skip).limit(limit).all()
    
    def create(self, db: Session, log_data: dict) -> LogEvent:
        """Cria novo log"""
        log = LogEvent(
            user_id=log_data.get("user_id"),
            event_type=log_data.get("event_type") or log_data.get("tipoEvento"),
            description=log_data.get("description") or log_data.get("descricao")
        )
        
        db.add(log)
        db.commit()
        db.refresh(log)
        return log


log_event_crud = LogEventCRUD()

