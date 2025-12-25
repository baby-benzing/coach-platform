// Exercise types
export interface Exercise {
  id: string;
  coach_id: string;
  name: string;
  description: string;
  youtube_url?: string;
  manual_tags: string[];
  ai_tags: string[];
  category: ExerciseCategory;
  equipment: string[];
  created_at: string;
  updated_at: string;
}

export type ExerciseCategory =
  | "strength"
  | "cardio"
  | "mobility"
  | "flexibility"
  | "balance"
  | "plyometric"
  | "core"
  | "warm_up"
  | "cool_down";

export interface ExerciseFormData {
  name: string;
  description: string;
  youtube_url?: string;
  manual_tags: string[];
  category: ExerciseCategory;
  equipment: string[];
}

// Client types
export interface Client {
  id: string;
  coach_id: string;
  email: string;
  name: string;
  phone?: string;
  date_of_birth?: string;
  created_at: string;
  updated_at: string;
}

// Assessment types
export interface Assessment {
  id: string;
  client_id: string;
  assessment_date: string;
  personal_info: PersonalInfo;
  body_metrics: BodyMetrics;
  health_history: HealthHistory;
  injuries: InjuryInfo;
  fitness_goals: FitnessGoals;
  exercise_history: ExerciseHistoryData;
  lifestyle: LifestyleInfo;
  availability: AvailabilityInfo;
  strength_baseline: StrengthBaseline;
  cardio_baseline: CardioBaseline;
  fms_scores: FMSScores;
  custom_fields: Record<string, unknown>;
  created_at: string;
}

export interface PersonalInfo {
  emergency_contact_name: string;
  emergency_contact_phone: string;
  occupation: string;
}

export interface BodyMetrics {
  height_cm: number;
  weight_kg: number;
  body_fat_percentage?: number;
}

export interface HealthHistory {
  medical_conditions: string[];
  medications: string[];
  surgeries: string[];
  allergies: string[];
}

export interface InjuryInfo {
  past_injuries: string[];
  current_limitations: string[];
  pain_areas: string[];
}

export interface FitnessGoals {
  short_term: string; // 3 months
  long_term: string; // 1 year
  priority_focus: PriorityFocus[];
}

export type PriorityFocus =
  | "fat_loss"
  | "muscle_gain"
  | "strength"
  | "endurance"
  | "flexibility"
  | "mobility"
  | "sports_performance"
  | "general_fitness"
  | "injury_rehab";

export interface ExerciseHistoryData {
  experience_level: "beginner" | "intermediate" | "advanced";
  current_frequency: number; // days per week
  past_sports: string[];
  current_activities: string[];
}

export interface LifestyleInfo {
  sleep_hours: number;
  sleep_quality: "poor" | "fair" | "good" | "excellent";
  stress_level: "low" | "moderate" | "high" | "very_high";
  diet_type: string;
  hydration_liters: number;
}

export interface AvailabilityInfo {
  days_per_week: number;
  minutes_per_session: number;
  preferred_days: string[];
  equipment_access: string[];
  training_location: "gym" | "home" | "outdoor" | "hybrid";
}

export interface StrengthBaseline {
  squat_1rm_kg?: number;
  bench_1rm_kg?: number;
  deadlift_1rm_kg?: number;
  push_up_max?: number;
  pull_up_max?: number;
  plank_hold_seconds?: number;
}

export interface CardioBaseline {
  resting_hr?: number;
  max_hr?: number;
  estimated_vo2max?: number;
  run_5k_minutes?: number;
  run_1mile_minutes?: number;
}

export interface FMSScores {
  deep_squat: number; // 0-3
  hurdle_step: number;
  inline_lunge: number;
  shoulder_mobility: number;
  active_straight_leg_raise: number;
  trunk_stability_pushup: number;
  rotary_stability: number;
  total_score: number; // 0-21
}

// Workout Plan types
export interface WorkoutPlan {
  id: string;
  client_id: string;
  coach_id: string;
  name: string;
  start_date: string;
  weeks: number;
  status: "draft" | "active" | "completed";
  coach_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface WorkoutDay {
  id: string;
  plan_id: string;
  week_number: number;
  day_of_week: number; // 0-6, 0 = Sunday
  name: string;
  focus: string;
  exercises: WorkoutExercise[];
  notes?: string;
}

export interface WorkoutExercise {
  exercise_id: string;
  exercise_name: string;
  order: number;
  // For strength
  sets?: number;
  reps?: string; // Can be "8-12" or "8"
  weight_kg?: number;
  rest_seconds?: number;
  rpe?: number; // 1-10
  // For cardio/endurance
  duration_minutes?: number;
  distance_km?: number;
  target_hr?: number;
  target_pace?: string;
  notes?: string;
}

// Coach types
export interface Coach {
  id: string;
  email: string;
  name: string;
  training_philosophy?: string;
  specializations: string[];
  created_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Agent workflow input types
export interface PlanGenerationInput {
  client_id: string;
  assessment_id: string;
  coach_preferences: CoachPreferences;
  training_philosophy: string;
}

export interface CoachPreferences {
  focus_areas: PriorityFocus[];
  plan_duration_weeks: number;
  periodization_style: "linear" | "undulating" | "block";
  intensity_preference: "conservative" | "moderate" | "aggressive";
}
