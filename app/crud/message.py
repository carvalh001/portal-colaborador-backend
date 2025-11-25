from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.message import Message


class MessageCRUD:
    def get_by_id(self, db: Session, message_id: int) -> Optional[Message]:
        """Busca mensagem por ID"""
        return db.query(Message).filter(Message.id == message_id).first()
    
    def get_by_user_id(self, db: Session, user_id: int) -> List[Message]:
        """Lista mensagens de um usuário específico"""
        return db.query(Message).filter(Message.user_id == user_id).order_by(Message.created_at.desc()).all()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Message]:
        """Lista mensagens com filtros opcionais"""
        query = db.query(Message)
        
        if user_id:
            query = query.filter(Message.user_id == user_id)
        
        if status:
            query = query.filter(Message.status == status)
        
        return query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    def create(self, db: Session, message_data: dict, user_id: int) -> Message:
        """Cria nova mensagem"""
        message = Message(
            user_id=user_id,
            title=message_data.get("titulo") or message_data.get("title"),
            content=message_data.get("conteudo") or message_data.get("content"),
            status="PENDENTE"
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def update_status(self, db: Session, message_id: int, status: str) -> Optional[Message]:
        """Atualiza status da mensagem"""
        message = self.get_by_id(db, message_id)
        if not message:
            return None
        
        message.status = status
        db.commit()
        db.refresh(message)
        return message


message_crud = MessageCRUD()

