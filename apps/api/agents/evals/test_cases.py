"""
Test cases for evaluating the workout planning agent.

Each test case represents a realistic client scenario with expected
characteristics that the generated plan should exhibit.
"""

EVALUATION_TEST_CASES = [
    {
        "name": "Beginner with Movement Limitations",
        "description": "Client new to training with poor FMS scores",
        "assessment": {
            "fms_scores": {
                "deep_squat": 1,
                "hurdle_step": 2,
                "inline_lunge": 2,
                "shoulder_mobility": 1,
                "active_straight_leg_raise": 2,
                "trunk_stability_pushup": 2,
                "rotary_stability": 2,
                "total_score": 12
            },
            "body_metrics": {
                "height_cm": 175,
                "weight_kg": 85,
                "body_fat_percentage": 28
            },
            "fitness_goals": {
                "short_term": "Lose 5kg, improve movement quality",
                "long_term": "Build sustainable exercise habit",
                "priority_focus": ["fat_loss", "mobility", "general_fitness"]
            },
            "exercise_history": {
                "experience_level": "beginner",
                "current_frequency": 0,
                "past_sports": [],
                "current_activities": ["walking"]
            },
            "availability": {
                "days_per_week": 3,
                "minutes_per_session": 45,
                "preferred_days": ["Monday", "Wednesday", "Friday"],
                "equipment_access": ["dumbbells", "resistance bands"],
                "training_location": "home"
            },
            "injuries": {
                "past_injuries": ["lower back pain 2 years ago"],
                "current_limitations": ["shoulder stiffness"],
                "pain_areas": []
            }
        },
        "coach_preferences": {
            "focus_areas": ["movement_quality", "fat_loss"],
            "plan_duration_weeks": 4,
            "periodization_style": "linear",
            "intensity_preference": "conservative"
        },
        "expected_characteristics": {
            "should_avoid": ["overhead press", "heavy squats", "behind neck movements"],
            "should_include": ["mobility work", "goblet squat", "landmine press", "plank"],
            "volume_level": "low_to_moderate",
            "rpe_range": [5, 7],
            "session_duration_max": 45
        }
    },
    {
        "name": "Intermediate Strength Focus",
        "description": "Experienced lifter wanting to build strength",
        "assessment": {
            "fms_scores": {
                "deep_squat": 3,
                "hurdle_step": 3,
                "inline_lunge": 2,
                "shoulder_mobility": 3,
                "active_straight_leg_raise": 3,
                "trunk_stability_pushup": 3,
                "rotary_stability": 2,
                "total_score": 19
            },
            "body_metrics": {
                "height_cm": 180,
                "weight_kg": 82,
                "body_fat_percentage": 15
            },
            "fitness_goals": {
                "short_term": "Increase squat 1RM by 10kg",
                "long_term": "Compete in powerlifting",
                "priority_focus": ["strength", "muscle_gain"]
            },
            "exercise_history": {
                "experience_level": "intermediate",
                "current_frequency": 4,
                "past_sports": ["football"],
                "current_activities": ["weight training"]
            },
            "strength_baseline": {
                "squat_1rm_kg": 120,
                "bench_1rm_kg": 90,
                "deadlift_1rm_kg": 140,
                "push_up_max": 40,
                "pull_up_max": 12
            },
            "availability": {
                "days_per_week": 4,
                "minutes_per_session": 75,
                "preferred_days": ["Monday", "Tuesday", "Thursday", "Friday"],
                "equipment_access": ["barbell", "dumbbells", "rack", "bench", "cable machine"],
                "training_location": "gym"
            },
            "injuries": {
                "past_injuries": [],
                "current_limitations": [],
                "pain_areas": []
            }
        },
        "coach_preferences": {
            "focus_areas": ["strength", "muscle_gain"],
            "plan_duration_weeks": 4,
            "periodization_style": "undulating",
            "intensity_preference": "moderate"
        },
        "expected_characteristics": {
            "should_include": ["back squat", "bench press", "deadlift", "barbell row"],
            "should_have": ["progressive_overload", "compound_movements"],
            "volume_level": "moderate_to_high",
            "rpe_range": [7, 9],
            "session_duration_max": 90
        }
    },
    {
        "name": "Senior Client Health Focus",
        "description": "Older adult focused on health and function",
        "assessment": {
            "fms_scores": {
                "deep_squat": 2,
                "hurdle_step": 2,
                "inline_lunge": 2,
                "shoulder_mobility": 2,
                "active_straight_leg_raise": 2,
                "trunk_stability_pushup": 1,
                "rotary_stability": 2,
                "total_score": 13
            },
            "body_metrics": {
                "height_cm": 170,
                "weight_kg": 75,
                "body_fat_percentage": 25
            },
            "fitness_goals": {
                "short_term": "Improve balance and energy",
                "long_term": "Maintain independence and health",
                "priority_focus": ["general_fitness", "mobility", "flexibility"]
            },
            "exercise_history": {
                "experience_level": "beginner",
                "current_frequency": 1,
                "past_sports": ["tennis 20 years ago"],
                "current_activities": ["walking", "gardening"]
            },
            "lifestyle": {
                "sleep_hours": 7,
                "sleep_quality": "fair",
                "stress_level": "low",
                "diet_type": "balanced"
            },
            "availability": {
                "days_per_week": 3,
                "minutes_per_session": 40,
                "preferred_days": ["Monday", "Wednesday", "Friday"],
                "equipment_access": ["resistance bands", "light dumbbells"],
                "training_location": "home"
            },
            "injuries": {
                "past_injuries": ["knee replacement 5 years ago"],
                "current_limitations": ["reduced grip strength", "balance issues"],
                "pain_areas": ["occasional knee stiffness"]
            },
            "health_history": {
                "medical_conditions": ["hypertension (controlled)", "osteoarthritis"],
                "medications": ["blood pressure medication"]
            }
        },
        "coach_preferences": {
            "focus_areas": ["mobility", "balance", "general_fitness"],
            "plan_duration_weeks": 4,
            "periodization_style": "linear",
            "intensity_preference": "conservative"
        },
        "expected_characteristics": {
            "should_avoid": ["high impact", "heavy loading", "deep squats", "jumping"],
            "should_include": ["balance work", "chair exercises", "band exercises", "mobility"],
            "volume_level": "low",
            "rpe_range": [4, 6],
            "session_duration_max": 40
        }
    },
    {
        "name": "Athlete Return to Sport",
        "description": "Athlete returning from injury, needs sport-specific prep",
        "assessment": {
            "fms_scores": {
                "deep_squat": 3,
                "hurdle_step": 2,  # Affected by injury
                "inline_lunge": 2,
                "shoulder_mobility": 3,
                "active_straight_leg_raise": 3,
                "trunk_stability_pushup": 3,
                "rotary_stability": 3,
                "total_score": 19
            },
            "body_metrics": {
                "height_cm": 185,
                "weight_kg": 78,
                "body_fat_percentage": 12
            },
            "fitness_goals": {
                "short_term": "Return to full training without pain",
                "long_term": "Compete at previous level",
                "priority_focus": ["injury_rehab", "sports_performance", "strength"]
            },
            "exercise_history": {
                "experience_level": "advanced",
                "current_frequency": 2,  # Reduced due to injury
                "past_sports": ["basketball"],
                "current_activities": ["rehab exercises", "swimming"]
            },
            "strength_baseline": {
                "squat_1rm_kg": 100,  # Reduced from 130
                "push_up_max": 50,
                "pull_up_max": 15
            },
            "availability": {
                "days_per_week": 5,
                "minutes_per_session": 60,
                "preferred_days": ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday"],
                "equipment_access": ["full gym", "bands", "medicine balls"],
                "training_location": "gym"
            },
            "injuries": {
                "past_injuries": ["ACL reconstruction 6 months ago"],
                "current_limitations": ["single leg stability still rebuilding"],
                "pain_areas": []
            }
        },
        "coach_preferences": {
            "focus_areas": ["injury_rehab", "strength", "sports_performance"],
            "plan_duration_weeks": 4,
            "periodization_style": "block",
            "intensity_preference": "moderate"
        },
        "expected_characteristics": {
            "should_include": ["single leg progressions", "stability work", "landing mechanics"],
            "should_have": ["gradual_progression", "sport_specific"],
            "volume_level": "moderate",
            "rpe_range": [6, 8],
            "session_duration_max": 60
        }
    },
    {
        "name": "Busy Professional Minimal Time",
        "description": "Time-constrained client needing efficient workouts",
        "assessment": {
            "fms_scores": {
                "deep_squat": 2,
                "hurdle_step": 3,
                "inline_lunge": 3,
                "shoulder_mobility": 2,
                "active_straight_leg_raise": 2,
                "trunk_stability_pushup": 2,
                "rotary_stability": 2,
                "total_score": 16
            },
            "body_metrics": {
                "height_cm": 172,
                "weight_kg": 80,
                "body_fat_percentage": 22
            },
            "fitness_goals": {
                "short_term": "Feel more energetic, reduce stress",
                "long_term": "Maintain fitness, prevent health issues",
                "priority_focus": ["general_fitness", "fat_loss", "endurance"]
            },
            "exercise_history": {
                "experience_level": "intermediate",
                "current_frequency": 1,
                "past_sports": ["running"],
                "current_activities": ["occasional running"]
            },
            "lifestyle": {
                "sleep_hours": 6,
                "sleep_quality": "fair",
                "stress_level": "high",
                "diet_type": "irregular",
                "occupation": "desk job with long hours"
            },
            "availability": {
                "days_per_week": 2,
                "minutes_per_session": 30,
                "preferred_days": ["Saturday", "Sunday"],
                "equipment_access": ["dumbbells", "pull-up bar"],
                "training_location": "home"
            },
            "injuries": {
                "past_injuries": [],
                "current_limitations": ["tight hip flexors from sitting"],
                "pain_areas": ["occasional neck tension"]
            }
        },
        "coach_preferences": {
            "focus_areas": ["general_fitness", "fat_loss"],
            "plan_duration_weeks": 4,
            "periodization_style": "linear",
            "intensity_preference": "moderate"
        },
        "expected_characteristics": {
            "should_include": ["compound movements", "circuits", "hip mobility"],
            "should_have": ["time_efficient", "full_body"],
            "volume_level": "moderate",
            "rpe_range": [6, 8],
            "session_duration_max": 30
        }
    }
]


# Quick test cases for faster iteration
QUICK_TEST_CASES = [
    {
        "name": "Basic Beginner Test",
        "assessment": {
            "fms_scores": {
                "deep_squat": 2,
                "hurdle_step": 2,
                "inline_lunge": 2,
                "shoulder_mobility": 2,
                "active_straight_leg_raise": 2,
                "trunk_stability_pushup": 2,
                "rotary_stability": 2,
                "total_score": 14
            },
            "fitness_goals": {
                "priority_focus": ["general_fitness"]
            },
            "exercise_history": {
                "experience_level": "beginner"
            },
            "availability": {
                "days_per_week": 3,
                "minutes_per_session": 45,
                "equipment_access": ["dumbbells"]
            }
        },
        "coach_preferences": {
            "focus_areas": ["general_fitness"],
            "plan_duration_weeks": 4,
            "periodization_style": "linear",
            "intensity_preference": "conservative"
        },
        "expected_characteristics": {
            "volume_level": "low_to_moderate",
            "rpe_range": [5, 7]
        }
    }
]
