-- Coach Platform Database Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Exercises table
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    youtube_url TEXT,
    manual_tags TEXT[] DEFAULT '{}',
    ai_tags TEXT[] DEFAULT '{}',
    category TEXT NOT NULL DEFAULT 'strength',
    equipment TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Clients table
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    date_of_birth TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Assessments table
CREATE TABLE IF NOT EXISTS assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    assessment_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    personal_info JSONB,
    body_metrics JSONB,
    health_history JSONB,
    injuries JSONB,
    fitness_goals JSONB,
    exercise_history JSONB,
    lifestyle JSONB,
    availability JSONB,
    strength_baseline JSONB,
    cardio_baseline JSONB,
    fms_scores JSONB,
    custom_fields JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Workout Plans table
CREATE TABLE IF NOT EXISTS workout_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    coach_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    weeks INTEGER NOT NULL DEFAULT 4,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'completed')),
    coach_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Workout Days table
CREATE TABLE IF NOT EXISTS workout_days (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plan_id UUID NOT NULL REFERENCES workout_plans(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    name TEXT NOT NULL,
    focus TEXT NOT NULL,
    exercises JSONB NOT NULL DEFAULT '[]',
    notes TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_exercises_coach_id ON exercises(coach_id);
CREATE INDEX IF NOT EXISTS idx_clients_coach_id ON clients(coach_id);
CREATE INDEX IF NOT EXISTS idx_assessments_client_id ON assessments(client_id);
CREATE INDEX IF NOT EXISTS idx_assessments_date ON assessments(assessment_date DESC);
CREATE INDEX IF NOT EXISTS idx_workout_plans_client_id ON workout_plans(client_id);
CREATE INDEX IF NOT EXISTS idx_workout_plans_coach_id ON workout_plans(coach_id);
CREATE INDEX IF NOT EXISTS idx_workout_days_plan_id ON workout_days(plan_id);

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_days ENABLE ROW LEVEL SECURITY;

-- Exercises policies
CREATE POLICY "Coaches can view own exercises"
    ON exercises FOR SELECT
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can insert own exercises"
    ON exercises FOR INSERT
    WITH CHECK (coach_id = auth.uid());

CREATE POLICY "Coaches can update own exercises"
    ON exercises FOR UPDATE
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can delete own exercises"
    ON exercises FOR DELETE
    USING (coach_id = auth.uid());

-- Clients policies
CREATE POLICY "Coaches can view own clients"
    ON clients FOR SELECT
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can insert own clients"
    ON clients FOR INSERT
    WITH CHECK (coach_id = auth.uid());

CREATE POLICY "Coaches can update own clients"
    ON clients FOR UPDATE
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can delete own clients"
    ON clients FOR DELETE
    USING (coach_id = auth.uid());

-- Assessments policies (via client ownership)
CREATE POLICY "Coaches can view assessments of own clients"
    ON assessments FOR SELECT
    USING (
        client_id IN (
            SELECT id FROM clients WHERE coach_id = auth.uid()
        )
    );

CREATE POLICY "Coaches can insert assessments for own clients"
    ON assessments FOR INSERT
    WITH CHECK (
        client_id IN (
            SELECT id FROM clients WHERE coach_id = auth.uid()
        )
    );

-- Workout Plans policies
CREATE POLICY "Coaches can view own workout plans"
    ON workout_plans FOR SELECT
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can insert own workout plans"
    ON workout_plans FOR INSERT
    WITH CHECK (coach_id = auth.uid());

CREATE POLICY "Coaches can update own workout plans"
    ON workout_plans FOR UPDATE
    USING (coach_id = auth.uid());

CREATE POLICY "Coaches can delete own workout plans"
    ON workout_plans FOR DELETE
    USING (coach_id = auth.uid());

-- Workout Days policies (via plan ownership)
CREATE POLICY "Coaches can view workout days of own plans"
    ON workout_days FOR SELECT
    USING (
        plan_id IN (
            SELECT id FROM workout_plans WHERE coach_id = auth.uid()
        )
    );

CREATE POLICY "Coaches can insert workout days for own plans"
    ON workout_days FOR INSERT
    WITH CHECK (
        plan_id IN (
            SELECT id FROM workout_plans WHERE coach_id = auth.uid()
        )
    );

CREATE POLICY "Coaches can update workout days of own plans"
    ON workout_days FOR UPDATE
    USING (
        plan_id IN (
            SELECT id FROM workout_plans WHERE coach_id = auth.uid()
        )
    );

CREATE POLICY "Coaches can delete workout days of own plans"
    ON workout_days FOR DELETE
    USING (
        plan_id IN (
            SELECT id FROM workout_plans WHERE coach_id = auth.uid()
        )
    );

-- Service role bypass for backend API
-- The backend uses supabase_service_key which bypasses RLS
