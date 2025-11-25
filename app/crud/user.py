from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User, UserRole
from app.core.security import get_password_hash


class UserCRUD:
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Busca usuário por username"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_username_or_email(self, db: Session, identifier: str) -> Optional[User]:
        """Busca usuário por username ou email"""
        return db.query(User).filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[User]:
        """Lista usuários com filtros opcionais"""
        query = db.query(User)
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (User.name.ilike(search_pattern)) |
                (User.email.ilike(search_pattern)) |
                (User.username.ilike(search_pattern))
            )
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, user_data: dict) -> User:
        """Cria novo usuário"""
        # Hash da senha
        password = user_data.pop("senha", None) or user_data.pop("password", None)
        hashed_password = get_password_hash(password)
        
        # Mapeamento de campos PT -> EN
        user_db = User(
            name=user_data.get("nome") or user_data.get("name"),
            email=user_data.get("email"),
            username=user_data.get("username"),
            password_hash=hashed_password,
            role=user_data.get("papel", UserRole.COLABORADOR) or user_data.get("role", UserRole.COLABORADOR),
            cpf=user_data.get("cpf"),
            phone=user_data.get("telefone") or user_data.get("phone"),
            bank_name=None,
            bank_agency=None,
            bank_account=None,
            is_active=user_data.get("is_active", True)
        )
        
        # Dados bancários se fornecidos
        dados_bancarios = user_data.get("dadosBancarios")
        if dados_bancarios:
            user_db.bank_name = dados_bancarios.get("banco")
            user_db.bank_agency = dados_bancarios.get("agencia")
            user_db.bank_account = dados_bancarios.get("conta")
        
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    
    def update(self, db: Session, user_id: int, user_data: dict) -> Optional[User]:
        """Atualiza usuário"""
        user = self.get_by_id(db, user_id)
        if not user:
            return None
        
        # Atualizar campos básicos
        if "nome" in user_data:
            user.name = user_data["nome"]
        if "email" in user_data:
            user.email = user_data["email"]
        if "telefone" in user_data:
            user.phone = user_data["telefone"]
        
        # Atualizar dados bancários
        if "dadosBancarios" in user_data:
            dados = user_data["dadosBancarios"]
            if dados:
                user.bank_name = dados.get("banco")
                user.bank_agency = dados.get("agencia")
                user.bank_account = dados.get("conta")
        
        db.commit()
        db.refresh(user)
        return user
    
    def update_role(self, db: Session, user_id: int, role: str) -> Optional[User]:
        """Atualiza papel do usuário"""
        user = self.get_by_id(db, user_id)
        if not user:
            return None
        
        user.role = UserRole(role)
        db.commit()
        db.refresh(user)
        return user


user_crud = UserCRUD()

