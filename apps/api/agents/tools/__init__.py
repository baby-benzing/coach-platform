"""
Tool definitions for the workout planning agent.

These tools enable the agent to:
1. Query the exercise library
2. Analyze FMS scores
3. Calculate training volumes
4. Generate structured workout days
"""

from typing import Any
import json

# Tool definitions for Anthropic API
WORKOUT_PLANNING_TOOLS = [
    {
        "name": "analyze_fms_scores",
        "description": """Analyze Functional Movement Screen (FMS) scores to identify
movement limitations, injury risk, and exercise contraindications. Use this tool
when you need to understand a client's movement quality and determine what exercises
are appropriate or should be avoided.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "fms_scores": {
                    "type": "object",
                    "description": "FMS test scores (0-3 for each)",
                    "properties": {
                        "deep_squat": {"type": "integer", "minimum": 0, "maximum": 3},
                        "hurdle_step": {"type": "integer", "minimum": 0, "maximum": 3},
                        "inline_lunge": {"type": "integer", "minimum": 0, "maximum": 3},
                        "shoulder_mobility": {"type": "integer", "minimum": 0, "maximum": 3},
                        "active_straight_leg_raise": {"type": "integer", "minimum": 0, "maximum": 3},
                        "trunk_stability_pushup": {"type": "integer", "minimum": 0, "maximum": 3},
                        "rotary_stability": {"type": "integer", "minimum": 0, "maximum": 3},
                    },
                    "required": ["deep_squat", "hurdle_step", "inline_lunge",
                                "shoulder_mobility", "active_straight_leg_raise",
                                "trunk_stability_pushup", "rotary_stability"]
                },
                "injury_history": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of past injuries and current limitations"
                }
            },
            "required": ["fms_scores"]
        }
    },
    {
        "name": "query_exercise_library",
        "description": """Search the exercise database to find suitable exercises
based on movement pattern, target muscle, equipment, and skill level. Use this
when you need to find specific exercises that match client capabilities and goals.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "movement_pattern": {
                    "type": "string",
                    "enum": ["squat", "hinge", "push", "pull", "carry", "core", "mobility", "cardio"],
                    "description": "Primary movement pattern to search for"
                },
                "target_muscles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Target muscle groups (e.g., quadriceps, glutes, chest)"
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["beginner", "intermediate", "advanced"],
                    "description": "Exercise difficulty level"
                },
                "equipment_available": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Available equipment (e.g., barbell, dumbbells, bodyweight)"
                },
                "exclude_patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Movement patterns or exercises to exclude based on limitations"
                }
            },
            "required": ["movement_pattern"]
        }
    },
    {
        "name": "calculate_training_volume",
        "description": """Calculate appropriate training volume (sets, reps, intensity)
based on client experience level, goals, and current training phase. Use this to
ensure volume prescriptions are appropriate.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "experience_level": {
                    "type": "string",
                    "enum": ["beginner", "intermediate", "advanced"],
                    "description": "Client's training experience level"
                },
                "training_phase": {
                    "type": "string",
                    "enum": ["anatomical_adaptation", "hypertrophy", "strength", "power", "deload"],
                    "description": "Current periodization phase"
                },
                "primary_goal": {
                    "type": "string",
                    "enum": ["strength", "hypertrophy", "endurance", "fat_loss", "general_fitness"],
                    "description": "Primary training goal"
                },
                "days_per_week": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 6,
                    "description": "Training days per week"
                },
                "muscle_group": {
                    "type": "string",
                    "description": "Target muscle group for volume calculation"
                }
            },
            "required": ["experience_level", "training_phase", "primary_goal", "days_per_week"]
        }
    },
    {
        "name": "generate_workout_day",
        "description": """Generate a complete workout for a specific training day
with exercises, sets, reps, rest periods, and coaching cues. Use this to create
individual training sessions.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "day_focus": {
                    "type": "string",
                    "description": "Primary focus of the training day (e.g., 'Upper Body Push', 'Lower Body')"
                },
                "movement_patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Movement patterns to include in this session"
                },
                "training_phase": {
                    "type": "string",
                    "enum": ["anatomical_adaptation", "hypertrophy", "strength", "power"],
                    "description": "Current training phase for volume/intensity prescription"
                },
                "session_duration_minutes": {
                    "type": "integer",
                    "description": "Target session duration in minutes"
                },
                "exercises": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "category": {"type": "string"}
                        }
                    },
                    "description": "Specific exercises to include (from exercise library query)"
                }
            },
            "required": ["day_focus", "movement_patterns", "training_phase"]
        }
    },
    {
        "name": "check_exercise_compatibility",
        "description": """Check if a specific exercise is compatible with client's
FMS findings and limitations. Use this before including an exercise in a plan
to ensure safety.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "exercise_name": {
                    "type": "string",
                    "description": "Name of the exercise to check"
                },
                "movement_pattern": {
                    "type": "string",
                    "description": "Primary movement pattern of the exercise"
                },
                "fms_limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of FMS-identified limitations"
                },
                "injury_history": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Relevant injury history"
                }
            },
            "required": ["exercise_name", "movement_pattern"]
        }
    },
    {
        "name": "save_workout_plan",
        "description": """Save the completed workout plan in the structured format
required by the system. Use this when you have finalized the complete 4-week plan
and are ready to save it.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "plan_name": {
                    "type": "string",
                    "description": "Name for the workout plan"
                },
                "weeks": {
                    "type": "integer",
                    "description": "Number of weeks in the plan"
                },
                "workout_days": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "week_number": {"type": "integer"},
                            "day_of_week": {"type": "integer"},
                            "name": {"type": "string"},
                            "focus": {"type": "string"},
                            "exercises": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "exercise_name": {"type": "string"},
                                        "sets": {"type": "integer"},
                                        "reps": {"type": "string"},
                                        "rest_seconds": {"type": "integer"},
                                        "rpe": {"type": "integer"},
                                        "notes": {"type": "string"}
                                    }
                                }
                            },
                            "notes": {"type": "string"}
                        }
                    },
                    "description": "Array of workout days with exercises"
                },
                "coach_notes": {
                    "type": "string",
                    "description": "Overall notes and instructions for the plan"
                }
            },
            "required": ["plan_name", "weeks", "workout_days"]
        }
    }
]


# Exercise database (would be from Supabase in production)
EXERCISE_DATABASE = {
    "squat": {
        "beginner": [
            {"name": "Goblet Squat", "equipment": ["dumbbell", "kettlebell"], "cues": ["chest up", "knees track toes", "sit back"]},
            {"name": "Box Squat", "equipment": ["box", "bench"], "cues": ["control descent", "pause on box", "drive through heels"]},
            {"name": "Bodyweight Squat", "equipment": [], "cues": ["arms forward for balance", "full depth if able"]},
            {"name": "Wall Squat Hold", "equipment": [], "cues": ["back flat against wall", "thighs parallel"]},
        ],
        "intermediate": [
            {"name": "Front Squat", "equipment": ["barbell"], "cues": ["elbows high", "upright torso", "full depth"]},
            {"name": "Bulgarian Split Squat", "equipment": ["dumbbells", "bench"], "cues": ["90/90 position", "vertical shin"]},
            {"name": "Leg Press", "equipment": ["machine"], "cues": ["lower back stays on pad", "full range"]},
        ],
        "advanced": [
            {"name": "Back Squat", "equipment": ["barbell", "rack"], "cues": ["brace core", "break at hips and knees", "drive up"]},
            {"name": "Pause Squat", "equipment": ["barbell"], "cues": ["3 second pause at bottom", "no bounce"]},
            {"name": "Pistol Squat", "equipment": [], "cues": ["counterbalance with arms", "control descent"]},
        ]
    },
    "hinge": {
        "beginner": [
            {"name": "Hip Hinge with Dowel", "equipment": ["dowel"], "cues": ["dowel contacts head, back, tailbone", "push hips back"]},
            {"name": "Romanian Deadlift (Light)", "equipment": ["dumbbells"], "cues": ["soft knees", "hips back", "feel hamstring stretch"]},
            {"name": "Glute Bridge", "equipment": [], "cues": ["squeeze glutes at top", "don't hyperextend back"]},
            {"name": "Hip Thrust", "equipment": ["bench"], "cues": ["chin tucked", "drive through heels"]},
        ],
        "intermediate": [
            {"name": "Romanian Deadlift", "equipment": ["barbell"], "cues": ["bar close to legs", "hinge at hips", "neutral spine"]},
            {"name": "Single-Leg Romanian Deadlift", "equipment": ["dumbbell"], "cues": ["hinge pattern", "balance challenge"]},
            {"name": "Kettlebell Swing", "equipment": ["kettlebell"], "cues": ["hip snap", "arms are ropes", "don't squat"]},
        ],
        "advanced": [
            {"name": "Conventional Deadlift", "equipment": ["barbell"], "cues": ["wedge into bar", "leg drive then hip extension"]},
            {"name": "Trap Bar Deadlift", "equipment": ["trap bar"], "cues": ["handles at sides", "push floor away"]},
            {"name": "Good Morning", "equipment": ["barbell"], "cues": ["bar on back", "hinge pattern", "feel hamstrings"]},
        ]
    },
    "push": {
        "beginner": [
            {"name": "Wall Push-Up", "equipment": [], "cues": ["body straight", "control movement"]},
            {"name": "Incline Push-Up", "equipment": ["bench"], "cues": ["hands on bench", "full range"]},
            {"name": "Dumbbell Floor Press", "equipment": ["dumbbells"], "cues": ["elbows at 45 degrees", "pause at bottom"]},
            {"name": "Landmine Press", "equipment": ["barbell", "landmine"], "cues": ["shoulder-friendly", "one arm at a time"]},
        ],
        "intermediate": [
            {"name": "Push-Up", "equipment": [], "cues": ["body straight", "chest to floor", "full lockout"]},
            {"name": "Dumbbell Bench Press", "equipment": ["dumbbells", "bench"], "cues": ["retract scapulae", "controlled descent"]},
            {"name": "Dumbbell Shoulder Press", "equipment": ["dumbbells"], "cues": ["neutral grip option", "core braced"]},
        ],
        "advanced": [
            {"name": "Barbell Bench Press", "equipment": ["barbell", "bench", "rack"], "cues": ["leg drive", "arch back", "touch chest"]},
            {"name": "Overhead Press", "equipment": ["barbell"], "cues": ["squeeze glutes", "head through at top"]},
            {"name": "Dips", "equipment": ["dip bars"], "cues": ["lean forward for chest", "upright for triceps"]},
        ]
    },
    "pull": {
        "beginner": [
            {"name": "Face Pull", "equipment": ["cable", "band"], "cues": ["pull to face", "external rotation at end"]},
            {"name": "Band Pull-Apart", "equipment": ["band"], "cues": ["squeeze shoulder blades", "arms straight"]},
            {"name": "Seated Cable Row", "equipment": ["cable"], "cues": ["chest up", "pull to sternum"]},
            {"name": "Lat Pulldown", "equipment": ["cable"], "cues": ["lean back slightly", "pull to chest"]},
        ],
        "intermediate": [
            {"name": "Dumbbell Row", "equipment": ["dumbbell", "bench"], "cues": ["pull to hip", "no rotation"]},
            {"name": "Inverted Row", "equipment": ["bar", "TRX"], "cues": ["body straight", "pull chest to bar"]},
            {"name": "Cable Row", "equipment": ["cable"], "cues": ["squeeze at end", "controlled return"]},
        ],
        "advanced": [
            {"name": "Barbell Row", "equipment": ["barbell"], "cues": ["hip hinge position", "pull to lower chest"]},
            {"name": "Pull-Up", "equipment": ["pull-up bar"], "cues": ["dead hang start", "chin over bar"]},
            {"name": "Weighted Pull-Up", "equipment": ["pull-up bar", "weight belt"], "cues": ["control the weight"]},
        ]
    },
    "carry": {
        "beginner": [
            {"name": "Farmer's Carry", "equipment": ["dumbbells", "kettlebells"], "cues": ["tall posture", "shoulders back", "controlled steps"]},
            {"name": "Suitcase Carry", "equipment": ["dumbbell"], "cues": ["one side", "resist lateral flexion"]},
        ],
        "intermediate": [
            {"name": "Goblet Carry", "equipment": ["kettlebell", "dumbbell"], "cues": ["front loaded", "upright posture"]},
            {"name": "Overhead Carry", "equipment": ["kettlebell"], "cues": ["arm locked out", "core braced"]},
        ],
        "advanced": [
            {"name": "Heavy Farmer's Carry", "equipment": ["trap bar", "farmer handles"], "cues": ["grip strength challenge"]},
            {"name": "Yoke Walk", "equipment": ["yoke"], "cues": ["small steps", "brace hard"]},
        ]
    },
    "core": {
        "beginner": [
            {"name": "Dead Bug", "equipment": [], "cues": ["low back pressed down", "opposite arm/leg", "breathe out on extension"]},
            {"name": "Bird Dog", "equipment": [], "cues": ["neutral spine", "opposite arm/leg", "don't rotate"]},
            {"name": "Plank", "equipment": [], "cues": ["straight line", "squeeze everything", "breathe"]},
            {"name": "Side Plank", "equipment": [], "cues": ["stack hips", "straight line", "don't sag"]},
        ],
        "intermediate": [
            {"name": "Pallof Press", "equipment": ["cable", "band"], "cues": ["resist rotation", "press and hold"]},
            {"name": "Ab Wheel Rollout", "equipment": ["ab wheel"], "cues": ["hips forward", "control the descent"]},
            {"name": "Hanging Knee Raise", "equipment": ["pull-up bar"], "cues": ["no swinging", "curl pelvis up"]},
        ],
        "advanced": [
            {"name": "Hanging Leg Raise", "equipment": ["pull-up bar"], "cues": ["straight legs", "control descent"]},
            {"name": "Dragon Flag", "equipment": ["bench"], "cues": ["straight body", "lower slowly"]},
            {"name": "L-Sit", "equipment": ["parallettes", "dip bars"], "cues": ["legs straight", "push down hard"]},
        ]
    },
    "cardio": {
        "beginner": [
            {"name": "Walking", "equipment": [], "cues": ["Zone 2 heart rate", "nasal breathing if possible"]},
            {"name": "Stationary Bike", "equipment": ["bike"], "cues": ["comfortable resistance", "steady pace"]},
        ],
        "intermediate": [
            {"name": "Rowing", "equipment": ["rower"], "cues": ["legs-back-arms", "steady state"]},
            {"name": "Running", "equipment": [], "cues": ["conversational pace for Zone 2"]},
            {"name": "Stair Climber", "equipment": ["stair machine"], "cues": ["don't lean on rails"]},
        ],
        "advanced": [
            {"name": "Interval Sprints", "equipment": [], "cues": ["work:rest ratio", "full recovery between"]},
            {"name": "Assault Bike Intervals", "equipment": ["assault bike"], "cues": ["all out effort", "complete rest"]},
        ]
    },
    "mobility": {
        "beginner": [
            {"name": "Cat-Cow", "equipment": [], "cues": ["breathe with movement", "full range"]},
            {"name": "World's Greatest Stretch", "equipment": [], "cues": ["lunge, rotate, reach"]},
            {"name": "90/90 Hip Stretch", "equipment": [], "cues": ["sit tall", "feel stretch in both hips"]},
            {"name": "Wall Ankle Stretch", "equipment": [], "cues": ["knee to wall", "heel down"]},
        ],
        "intermediate": [
            {"name": "Foam Rolling", "equipment": ["foam roller"], "cues": ["slow passes", "pause on tender spots"]},
            {"name": "Banded Hip Distraction", "equipment": ["band"], "cues": ["band in hip crease", "rock back and forth"]},
            {"name": "Thoracic Rotation", "equipment": [], "cues": ["hand behind head", "rotate to ceiling"]},
        ],
        "advanced": [
            {"name": "Jefferson Curl", "equipment": ["light weight"], "cues": ["very slow", "segment by segment"]},
            {"name": "Loaded Progressive Stretch", "equipment": [], "cues": ["use load to deepen stretch"]},
        ]
    }
}


def execute_tool(tool_name: str, tool_input: dict, context: dict = None) -> dict:
    """
    Execute a tool and return the result.

    Args:
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
        context: Optional context (e.g., exercise database from Supabase)

    Returns:
        Tool execution result
    """
    context = context or {}

    if tool_name == "analyze_fms_scores":
        return _analyze_fms_scores(tool_input)
    elif tool_name == "query_exercise_library":
        return _query_exercise_library(tool_input, context.get("exercises", EXERCISE_DATABASE))
    elif tool_name == "calculate_training_volume":
        return _calculate_training_volume(tool_input)
    elif tool_name == "generate_workout_day":
        return _generate_workout_day(tool_input)
    elif tool_name == "check_exercise_compatibility":
        return _check_exercise_compatibility(tool_input)
    elif tool_name == "save_workout_plan":
        return _save_workout_plan(tool_input, context)
    else:
        return {"error": f"Unknown tool: {tool_name}"}


def _analyze_fms_scores(input: dict) -> dict:
    """Analyze FMS scores and return insights."""
    scores = input["fms_scores"]
    injuries = input.get("injury_history", [])

    total_score = sum(scores.values())

    # Identify limitations (scores < 3)
    limitations = []
    contraindications = []
    recommendations = []

    if scores.get("deep_squat", 3) < 3:
        limitations.append("Squat pattern limitation")
        contraindications.append("Heavy bilateral squats")
        recommendations.append("Goblet squats, box squats, hip/ankle mobility work")

    if scores.get("hurdle_step", 3) < 3:
        limitations.append("Single-leg stance limitation")
        contraindications.append("Advanced single-leg exercises")
        recommendations.append("Progress single-leg work gradually")

    if scores.get("inline_lunge", 3) < 3:
        limitations.append("Lunge pattern limitation")
        contraindications.append("Walking lunges, dynamic lunges")
        recommendations.append("Static split squats before dynamic lunges")

    if scores.get("shoulder_mobility", 3) < 3:
        limitations.append("Shoulder mobility limitation")
        contraindications.append("Overhead pressing, behind-neck movements")
        recommendations.append("Landmine press, floor press, thoracic mobility")

    if scores.get("active_straight_leg_raise", 3) < 3:
        limitations.append("Hamstring/hip flexor limitation")
        contraindications.append("Aggressive hip hinging")
        recommendations.append("RDLs with limited range, active flexibility work")

    if scores.get("trunk_stability_pushup", 3) < 3:
        limitations.append("Core stability limitation")
        contraindications.append("Heavy compound lifts without core prep")
        recommendations.append("Dead bugs, planks, anti-extension work")

    if scores.get("rotary_stability", 3) < 3:
        limitations.append("Rotational stability limitation")
        contraindications.append("Rotational power exercises")
        recommendations.append("Pallof press, bird dogs, anti-rotation work")

    # Risk level
    if total_score < 14:
        risk_level = "HIGH"
        risk_note = "Focus on corrective exercise before progressing load"
    elif total_score < 18:
        risk_level = "MODERATE"
        risk_note = "Address limitations while training, monitor closely"
    else:
        risk_level = "LOW"
        risk_note = "Can pursue more aggressive training progression"

    return {
        "total_score": total_score,
        "max_score": 21,
        "risk_level": risk_level,
        "risk_note": risk_note,
        "limitations": limitations,
        "contraindications": contraindications,
        "recommendations": recommendations,
        "injury_considerations": injuries
    }


def _query_exercise_library(input: dict, exercise_db: dict) -> dict:
    """Query the exercise database."""
    pattern = input.get("movement_pattern", "")
    difficulty = input.get("difficulty", "intermediate")
    equipment = input.get("equipment_available", [])
    exclude = input.get("exclude_patterns", [])

    results = []

    if pattern in exercise_db:
        exercises = exercise_db[pattern].get(difficulty, [])

        for ex in exercises:
            # Filter by equipment if specified
            if equipment:
                ex_equipment = ex.get("equipment", [])
                if not ex_equipment or any(e in equipment for e in ex_equipment):
                    results.append(ex)
            else:
                results.append(ex)

    return {
        "movement_pattern": pattern,
        "difficulty": difficulty,
        "exercises": results,
        "count": len(results)
    }


def _calculate_training_volume(input: dict) -> dict:
    """Calculate appropriate training volume."""
    experience = input.get("experience_level", "intermediate")
    phase = input.get("training_phase", "hypertrophy")
    goal = input.get("primary_goal", "general_fitness")
    days = input.get("days_per_week", 3)

    # Base sets per muscle group per week
    base_sets = {
        "beginner": 10,
        "intermediate": 15,
        "advanced": 20
    }

    # Rep ranges by phase
    rep_ranges = {
        "anatomical_adaptation": "12-15",
        "hypertrophy": "8-12",
        "strength": "4-6",
        "power": "3-5",
        "deload": "8-12 (50% volume)"
    }

    # RPE by phase
    rpe_targets = {
        "anatomical_adaptation": "6-7",
        "hypertrophy": "7-8",
        "strength": "8-9",
        "power": "7-8 (speed focus)",
        "deload": "5-6"
    }

    # Rest periods by phase
    rest_periods = {
        "anatomical_adaptation": "60-90 seconds",
        "hypertrophy": "60-120 seconds",
        "strength": "2-4 minutes",
        "power": "2-5 minutes",
        "deload": "as needed"
    }

    return {
        "weekly_sets_per_muscle": base_sets.get(experience, 15),
        "rep_range": rep_ranges.get(phase, "8-12"),
        "rpe_target": rpe_targets.get(phase, "7-8"),
        "rest_period": rest_periods.get(phase, "60-90 seconds"),
        "training_days": days,
        "sets_per_session": base_sets.get(experience, 15) // days
    }


def _generate_workout_day(input: dict) -> dict:
    """Generate a workout day structure."""
    focus = input.get("day_focus", "Full Body")
    patterns = input.get("movement_patterns", [])
    phase = input.get("training_phase", "hypertrophy")
    duration = input.get("session_duration_minutes", 60)
    exercises = input.get("exercises", [])

    # Phase-specific parameters
    phase_params = {
        "anatomical_adaptation": {"sets": 3, "reps": "12-15", "rpe": 6},
        "hypertrophy": {"sets": 4, "reps": "8-12", "rpe": 7},
        "strength": {"sets": 4, "reps": "4-6", "rpe": 8},
        "power": {"sets": 3, "reps": "3-5", "rpe": 7}
    }

    params = phase_params.get(phase, phase_params["hypertrophy"])

    workout = {
        "focus": focus,
        "phase": phase,
        "estimated_duration": duration,
        "structure": [
            {
                "section": "Warm-Up",
                "duration": "10 min",
                "exercises": ["Dynamic stretching", "Movement prep"]
            },
            {
                "section": "Main Work",
                "duration": f"{duration - 20} min",
                "exercises": []
            },
            {
                "section": "Cool-Down",
                "duration": "5-10 min",
                "exercises": ["Static stretching", "Foam rolling"]
            }
        ],
        "volume_parameters": params
    }

    # Add exercises to main work
    for ex in exercises:
        workout["structure"][1]["exercises"].append({
            "name": ex.get("name", "Exercise"),
            "sets": params["sets"],
            "reps": params["reps"],
            "rpe": params["rpe"]
        })

    return workout


def _check_exercise_compatibility(input: dict) -> dict:
    """Check if an exercise is compatible with client limitations."""
    exercise = input.get("exercise_name", "")
    pattern = input.get("movement_pattern", "")
    limitations = input.get("fms_limitations", [])
    injuries = input.get("injury_history", [])

    is_compatible = True
    warnings = []
    alternatives = []

    # Check for pattern conflicts
    pattern_conflicts = {
        "squat": ["Squat pattern limitation", "Heavy bilateral squats"],
        "hinge": ["Hamstring/hip flexor limitation", "Aggressive hip hinging"],
        "push": ["Shoulder mobility limitation", "Overhead pressing"],
        "pull": ["Shoulder mobility limitation"],
        "core": ["Core stability limitation"]
    }

    for limitation in limitations:
        if any(conflict in limitation for conflict in pattern_conflicts.get(pattern, [])):
            is_compatible = False
            warnings.append(f"Exercise conflicts with: {limitation}")

    # Check injury history
    injury_keywords = {
        "shoulder": ["overhead", "press", "pull-up"],
        "knee": ["squat", "lunge", "jump"],
        "back": ["deadlift", "good morning", "row"],
        "hip": ["hinge", "squat", "lunge"]
    }

    exercise_lower = exercise.lower()
    for injury in injuries:
        injury_lower = injury.lower()
        for body_part, exercise_keywords in injury_keywords.items():
            if body_part in injury_lower:
                for keyword in exercise_keywords:
                    if keyword in exercise_lower:
                        warnings.append(f"Caution: {exercise} may aggravate {injury}")

    return {
        "exercise": exercise,
        "is_compatible": is_compatible and len(warnings) == 0,
        "warnings": warnings,
        "alternatives": alternatives
    }


def _save_workout_plan(input: dict, context: dict) -> dict:
    """Save the workout plan (returns structure for API to save)."""
    return {
        "status": "ready_to_save",
        "plan": {
            "name": input.get("plan_name", "4-Week Training Plan"),
            "weeks": input.get("weeks", 4),
            "workout_days": input.get("workout_days", []),
            "coach_notes": input.get("coach_notes", "")
        }
    }
