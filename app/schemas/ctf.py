from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CTFDifficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


# Flag Schemas
class CTFFlagBase(BaseModel):
    difficulty: CTFDifficulty
    points: int
    hint: Optional[str] = None
    active: bool = True


class CTFFlagCreate(CTFFlagBase):
    flag_hash: str = Field(..., min_length=64, max_length=64)  # SHA256 hash


class CTFFlag(CTFFlagBase):
    id: int
    flag_hash: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Submission Schemas
class CTFSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    flag: str = Field(..., min_length=5, max_length=100)


class CTFSubmissionResponse(BaseModel):
    success: bool
    message: str
    points: Optional[int] = None
    difficulty: Optional[CTFDifficulty] = None
    submitted_at: Optional[datetime] = None


class CTFSubmission(BaseModel):
    id: int
    user_name: str
    user_email: str
    flag_id: int
    difficulty: CTFDifficulty
    points: int
    submitted_at: datetime
    
    class Config:
        from_attributes = True


# Leaderboard Schemas
class CTFLeaderboardEntry(BaseModel):
    rank: int
    name: str
    email: str
    total_points: int
    submissions: List[dict]  # Lista com {difficulty, points, submitted_at}


class CTFLeaderboard(BaseModel):
    entries: List[CTFLeaderboardEntry]
    total_participants: int


# Stats Schemas
class CTFDifficultyStats(BaseModel):
    difficulty: CTFDifficulty
    total_slots: int
    used_slots: int
    available_slots: int
    points_per_flag: int


class CTFStats(BaseModel):
    total_participants: int
    total_submissions: int
    difficulties: List[CTFDifficultyStats]
    leaderboard_preview: List[CTFLeaderboardEntry]  # Top 3

