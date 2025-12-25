from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum


class ExerciseCategory(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    MOBILITY = "mobility"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    PLYOMETRIC = "plyometric"
    CORE = "core"
    WARM_UP = "warm_up"
    COOL_DOWN = "cool_down"


class ExerciseCreate(BaseModel):
    name: str
    description: str
    youtube_url: Optional[str] = None
    manual_tags: list[str] = []
    category: ExerciseCategory = ExerciseCategory.STRENGTH
    equipment: list[str] = []


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    youtube_url: Optional[str] = None
    manual_tags: Optional[list[str]] = None
    category: Optional[ExerciseCategory] = None
    equipment: Optional[list[str]] = None


class ExerciseResponse(BaseModel):
    id: str
    coach_id: str
    name: str
    description: str
    youtube_url: Optional[str] = None
    manual_tags: list[str] = []
    ai_tags: list[str] = []
    category: str
    equipment: list[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
