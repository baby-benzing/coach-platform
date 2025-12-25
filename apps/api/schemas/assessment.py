from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class PersonalInfo(BaseModel):
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    occupation: Optional[str] = None


class BodyMetrics(BaseModel):
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None


class HealthHistory(BaseModel):
    medical_conditions: list[str] = []
    medications: list[str] = []
    surgeries: list[str] = []
    allergies: list[str] = []


class InjuryInfo(BaseModel):
    past_injuries: list[str] = []
    current_limitations: list[str] = []
    pain_areas: list[str] = []


class FitnessGoals(BaseModel):
    short_term: Optional[str] = None
    long_term: Optional[str] = None
    priority_focus: list[str] = []


class ExerciseHistory(BaseModel):
    experience_level: Optional[str] = None
    current_frequency: Optional[int] = None
    past_sports: list[str] = []
    current_activities: list[str] = []


class LifestyleInfo(BaseModel):
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[str] = None
    stress_level: Optional[str] = None
    diet_type: Optional[str] = None
    hydration_liters: Optional[float] = None


class AvailabilityInfo(BaseModel):
    days_per_week: Optional[int] = None
    minutes_per_session: Optional[int] = None
    preferred_days: list[str] = []
    equipment_access: list[str] = []
    training_location: Optional[str] = None


class StrengthBaseline(BaseModel):
    squat_1rm_kg: Optional[float] = None
    bench_1rm_kg: Optional[float] = None
    deadlift_1rm_kg: Optional[float] = None
    push_up_max: Optional[int] = None
    pull_up_max: Optional[int] = None
    plank_hold_seconds: Optional[int] = None


class CardioBaseline(BaseModel):
    resting_hr: Optional[int] = None
    max_hr: Optional[int] = None
    estimated_vo2max: Optional[float] = None
    run_5k_minutes: Optional[float] = None
    run_1mile_minutes: Optional[float] = None


class FMSScores(BaseModel):
    deep_squat: int = 0
    hurdle_step: int = 0
    inline_lunge: int = 0
    shoulder_mobility: int = 0
    active_straight_leg_raise: int = 0
    trunk_stability_pushup: int = 0
    rotary_stability: int = 0
    total_score: int = 0


class AssessmentCreate(BaseModel):
    assessment_date: Optional[datetime] = None
    personal_info: Optional[PersonalInfo] = None
    body_metrics: Optional[BodyMetrics] = None
    health_history: Optional[HealthHistory] = None
    injuries: Optional[InjuryInfo] = None
    fitness_goals: Optional[FitnessGoals] = None
    exercise_history: Optional[ExerciseHistory] = None
    lifestyle: Optional[LifestyleInfo] = None
    availability: Optional[AvailabilityInfo] = None
    strength_baseline: Optional[StrengthBaseline] = None
    cardio_baseline: Optional[CardioBaseline] = None
    fms_scores: Optional[FMSScores] = None
    custom_fields: Optional[dict[str, Any]] = None


class AssessmentResponse(BaseModel):
    id: str
    client_id: str
    assessment_date: datetime
    personal_info: Optional[dict] = None
    body_metrics: Optional[dict] = None
    health_history: Optional[dict] = None
    injuries: Optional[dict] = None
    fitness_goals: Optional[dict] = None
    exercise_history: Optional[dict] = None
    lifestyle: Optional[dict] = None
    availability: Optional[dict] = None
    strength_baseline: Optional[dict] = None
    cardio_baseline: Optional[dict] = None
    fms_scores: Optional[dict] = None
    custom_fields: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
