from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.ctf import (
    CTFSubmissionCreate,
    CTFSubmissionResponse,
    CTFLeaderboard,
    CTFStats,
    CTFFlag
)
from app.crud import ctf as ctf_crud
from app.core.config import settings
import re


router = APIRouter()


def validate_flag_format(flag: str) -> bool:
    """Valida o formato da flag FLAG{...}"""
    pattern = r'^FLAG\{[a-zA-Z0-9_\-@!#$%&*+=]{5,80}\}$'
    return bool(re.match(pattern, flag))


@router.post("/submit", response_model=CTFSubmissionResponse)
def submit_flag(
    submission: CTFSubmissionCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para submissão de flags
    Valida a flag, verifica disponibilidade e registra a submissão
    """
    # Validar formato da flag
    if not validate_flag_format(submission.flag):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de flag inválido. Use: FLAG{...}"
        )
    
    # Gerar hash da flag submetida
    flag_hash = ctf_crud.hash_flag(submission.flag)
    
    # Buscar flag no banco
    flag = ctf_crud.get_flag_by_hash(db, flag_hash)
    
    if not flag:
        return CTFSubmissionResponse(
            success=False,
            message="Flag incorreta! Tente novamente. 🔍"
        )
    
    # Verificar se usuário já submeteu uma flag desta dificuldade
    existing_submission = ctf_crud.get_user_submission_by_difficulty(
        db,
        submission.email,
        flag.difficulty
    )
    
    if existing_submission:
        return CTFSubmissionResponse(
            success=False,
            message=f"Você já submeteu uma flag {flag.difficulty.value}! Tente outra dificuldade. 🎯"
        )
    
    # Verificar se ainda há slots disponíveis
    difficulty_limits = {
        "EASY": settings.CTF_EASY_FLAGS,
        "MEDIUM": settings.CTF_MEDIUM_FLAGS,
        "HARD": settings.CTF_HARD_FLAGS
    }
    
    current_count = ctf_crud.count_submissions_by_difficulty(db, flag.difficulty)
    max_slots = difficulty_limits.get(flag.difficulty.value, 0)
    
    if current_count >= max_slots:
        return CTFSubmissionResponse(
            success=False,
            message=f"Todos os slots de flags {flag.difficulty.value} já foram preenchidos! 😢"
        )
    
    # Criar submissão
    try:
        new_submission = ctf_crud.create_submission(
            db,
            user_name=submission.name,
            user_email=submission.email,
            flag=flag
        )
        
        return CTFSubmissionResponse(
            success=True,
            message=f"🎉 Parabéns! Flag {flag.difficulty.value} encontrada! +{flag.points} pontos!",
            points=flag.points,
            difficulty=flag.difficulty,
            submitted_at=new_submission.submitted_at
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao registrar submissão. Tente novamente."
        )


@router.get("/leaderboard")
def get_leaderboard(
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para visualizar o leaderboard
    Retorna ranking dos participantes ordenado por pontos
    """
    leaderboard_data = ctf_crud.get_leaderboard(db, limit)
    total_participants = len(leaderboard_data)
    
    return {
        "entries": leaderboard_data,
        "total_participants": total_participants
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Endpoint público para visualizar estatísticas gerais do CTF
    """
    stats = ctf_crud.get_stats(db)
    leaderboard_preview = ctf_crud.get_leaderboard(db, limit=3)
    
    return {
        **stats,
        "leaderboard_preview": leaderboard_preview
    }


@router.get("/easter-egg")
def easter_egg(db: Session = Depends(get_db)):
    """
    Endpoint oculto - Easter Egg para flag média
    A flag está escondida no header HTTP customizado
    """
    # Flag média escondida no header
    medium_flag = "FLAG{h1dd3n_3ndp01nt_m4st3r}"
    
    response = JSONResponse(content={
        "message": "🐰 Você encontrou o Easter Egg! Verifique os headers HTTP...",
        "hint": "Procure por headers customizados começando com X-CTF-",
        "hint2": "Use as DevTools do navegador ou ferramentas como curl/Postman"
    })
    
    response.headers["X-CTF-Flag"] = medium_flag
    response.headers["X-CTF-Difficulty"] = "MEDIUM"
    response.headers["X-CTF-Points"] = "20"
    
    return response


@router.get("/flags", response_model=list[CTFFlag])
def list_flags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint admin apenas para listar todas as flags
    Requer autenticação como ADMIN
    """
    if current_user.papel != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores."
        )
    
    flags = ctf_crud.get_all_flags(db, active_only=False)
    return flags


@router.get("/my-submissions")
def get_my_submissions(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint público para usuário verificar suas próprias submissões
    """
    submissions = ctf_crud.get_user_submissions(db, email)
    
    return {
        "email": email.lower(),
        "total_submissions": len(submissions),
        "total_points": sum(s.points for s in submissions),
        "submissions": [
            {
                "difficulty": s.difficulty.value,
                "points": s.points,
                "submitted_at": s.submitted_at.isoformat()
            }
            for s in submissions
        ]
    }

