from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from enum import Enum


class PlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"


class PeriodizationStyle(str, Enum):
    LINEAR = "linear"
    UNDULATING = "undulating"
    BLOCK = "block"


class IntensityPreference(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class CoachPreferences(BaseModel):
    focus_areas: list[str] = []
    plan_duration_weeks: int = 4
    periodization_style: PeriodizationStyle = PeriodizationStyle.LINEAR
    intensity_preference: IntensityPreference = IntensityPreference.MODERATE


class PlanGenerateRequest(BaseModel):
    assessment_id: str
    coach_preferences: CoachPreferences


class WorkoutExercise(BaseModel):
    exercise_id: str
    exercise_name: str
    order: int
    sets: Optional[int] = None
    reps: Optional[str] = None
    weight_kg: Optional[float] = None
    rest_seconds: Optional[int] = None
    rpe: Optional[int] = None
    duration_minutes: Optional[int] = None
    distance_km: Optional[float] = None
    target_hr: Optional[int] = None
    target_pace: Optional[str] = None
    notes: Optional[str] = None


class WorkoutDayResponse(BaseModel):
    id: str
    plan_id: str
    week_number: int
    day_of_week: int
    name: str
    focus: str
    exercises: list[WorkoutExercise] = []
    notes: Optional[str] = None


class PlanCreate(BaseModel):
    client_id: str
    name: str
    start_date: datetime
    weeks: int = 4
    status: PlanStatus = PlanStatus.DRAFT
    coach_notes: Optional[str] = None


class PlanResponse(BaseModel):
    id: str
    client_id: str
    coach_id: str
    name: str
    start_date: datetime
    weeks: int
    status: str
    coach_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
