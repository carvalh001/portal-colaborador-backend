from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict
from app.models.ctf import CTFFlag, CTFSubmission, CTFDifficulty
from app.schemas.ctf import CTFFlagCreate, CTFSubmissionCreate
import hashlib


def hash_flag(flag: str) -> str:
    """Gera hash SHA256 de uma flag"""
    return hashlib.sha256(flag.encode()).hexdigest()


# CRUD Operations for CTFFlag
def create_flag(db: Session, flag_data: CTFFlagCreate) -> CTFFlag:
    """Cria uma nova flag no banco"""
    db_flag = CTFFlag(**flag_data.model_dump())
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag


def get_flag_by_hash(db: Session, flag_hash: str) -> Optional[CTFFlag]:
    """Busca uma flag pelo hash"""
    return db.query(CTFFlag).filter(
        CTFFlag.flag_hash == flag_hash,
        CTFFlag.active == True
    ).first()


def get_flags_by_difficulty(db: Session, difficulty: CTFDifficulty) -> List[CTFFlag]:
    """Retorna todas as flags de uma dificuldade"""
    return db.query(CTFFlag).filter(
        CTFFlag.difficulty == difficulty,
        CTFFlag.active == True
    ).all()


def get_all_flags(db: Session, active_only: bool = True) -> List[CTFFlag]:
    """Retorna todas as flags"""
    query = db.query(CTFFlag)
    if active_only:
        query = query.filter(CTFFlag.active == True)
    return query.all()


# CRUD Operations for CTFSubmission
def create_submission(
    db: Session,
    user_name: str,
    user_email: str,
    flag: CTFFlag
) -> CTFSubmission:
    """Cria uma nova submissão de flag"""
    db_submission = CTFSubmission(
        user_name=user_name,
        user_email=user_email.lower(),  # Normalizar email
        flag_id=flag.id,
        difficulty=flag.difficulty,
        points=flag.points
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_user_submission_by_difficulty(
    db: Session,
    user_email: str,
    difficulty: CTFDifficulty
) -> Optional[CTFSubmission]:
    """Verifica se usuário já submeteu uma flag desta dificuldade"""
    return db.query(CTFSubmission).filter(
        CTFSubmission.user_email == user_email.lower(),
        CTFSubmission.difficulty == difficulty
    ).first()


def get_user_submissions(db: Session, user_email: str) -> List[CTFSubmission]:
    """Retorna todas as submissões de um usuário"""
    return db.query(CTFSubmission).filter(
        CTFSubmission.user_email == user_email.lower()
    ).order_by(CTFSubmission.submitted_at.desc()).all()


def count_submissions_by_difficulty(db: Session, difficulty: CTFDifficulty) -> int:
    """Conta quantas submissões existem para uma dificuldade"""
    return db.query(CTFSubmission).filter(
        CTFSubmission.difficulty == difficulty
    ).count()


def get_leaderboard(db: Session, limit: Optional[int] = None) -> List[Dict]:
    """
    Retorna o leaderboard com ranking dos participantes
    Agrupa por usuário e soma os pontos
    """
    # Query agregada: agrupa por usuário e soma pontos
    query = db.query(
        CTFSubmission.user_name,
        CTFSubmission.user_email,
        func.sum(CTFSubmission.points).label('total_points'),
        func.count(CTFSubmission.id).label('submission_count')
    ).group_by(
        CTFSubmission.user_email,
        CTFSubmission.user_name
    ).order_by(
        desc('total_points'),
        CTFSubmission.submitted_at
    )
    
    if limit:
        query = query.limit(limit)
    
    results = query.all()
    
    # Buscar detalhes das submissões de cada usuário
    leaderboard = []
    for rank, result in enumerate(results, start=1):
        submissions = db.query(CTFSubmission).filter(
            CTFSubmission.user_email == result.user_email
        ).order_by(CTFSubmission.submitted_at).all()
        
        submission_details = [
            {
                'difficulty': sub.difficulty.value,
                'points': sub.points,
                'submitted_at': sub.submitted_at.isoformat()
            }
            for sub in submissions
        ]
        
        leaderboard.append({
            'rank': rank,
            'name': result.user_name,
            'email': result.user_email,
            'total_points': int(result.total_points),
            'submissions': submission_details
        })
    
    return leaderboard


def get_stats(db: Session) -> Dict:
    """Retorna estatísticas gerais do CTF"""
    from app.core.config import settings
    
    # Total de participantes únicos
    total_participants = db.query(
        func.count(func.distinct(CTFSubmission.user_email))
    ).scalar() or 0
    
    # Total de submissões
    total_submissions = db.query(func.count(CTFSubmission.id)).scalar() or 0
    
    # Estatísticas por dificuldade
    difficulties_config = {
        CTFDifficulty.EASY: {
            'total_slots': settings.CTF_EASY_FLAGS,
            'points': settings.CTF_EASY_POINTS
        },
        CTFDifficulty.MEDIUM: {
            'total_slots': settings.CTF_MEDIUM_FLAGS,
            'points': settings.CTF_MEDIUM_POINTS
        },
        CTFDifficulty.HARD: {
            'total_slots': settings.CTF_HARD_FLAGS,
            'points': settings.CTF_HARD_POINTS
        }
    }
    
    difficulty_stats = []
    for difficulty, config in difficulties_config.items():
        used_slots = count_submissions_by_difficulty(db, difficulty)
        difficulty_stats.append({
            'difficulty': difficulty.value,
            'total_slots': config['total_slots'],
            'used_slots': used_slots,
            'available_slots': max(0, config['total_slots'] - used_slots),
            'points_per_flag': config['points']
        })
    
    return {
        'total_participants': total_participants,
        'total_submissions': total_submissions,
        'difficulties': difficulty_stats
    }

