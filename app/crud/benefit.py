from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.benefit import Benefit


class BenefitCRUD:
    def get_by_id(self, db: Session, benefit_id: int) -> Optional[Benefit]:
        """Busca benefício por ID"""
        return db.query(Benefit).filter(Benefit.id == benefit_id).first()
    
    def get_by_user_id(self, db: Session, user_id: int) -> List[Benefit]:
        """Lista benefícios de um usuário específico"""
        return db.query(Benefit).filter(Benefit.user_id == user_id).all()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[int] = None,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Benefit]:
        """Lista benefícios com filtros opcionais"""
        query = db.query(Benefit)
        
        if user_id:
            query = query.filter(Benefit.user_id == user_id)
        
        if category:
            query = query.filter(Benefit.category == category)
        
        if status:
            query = query.filter(Benefit.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, benefit_data: dict) -> Benefit:
        """Cria novo benefício"""
        benefit = Benefit(
            user_id=benefit_data.get("userId") or benefit_data.get("user_id"),
            name=benefit_data.get("nome") or benefit_data.get("name"),
            category=benefit_data.get("categoria") or benefit_data.get("category"),
            status=benefit_data.get("status"),
            value=benefit_data.get("valor") or benefit_data.get("value"),
            description=benefit_data.get("descricao") or benefit_data.get("description")
        )
        
        db.add(benefit)
        db.commit()
        db.refresh(benefit)
        return benefit


benefit_crud = BenefitCRUD()

