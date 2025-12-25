from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone

from auth import get_current_user, get_coach_id
from database import get_supabase_client
from schemas import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from services import AIService

router = APIRouter()
ai_service = AIService()


@router.get("/exercises", response_model=dict)
async def list_exercises(coach_id: str = Depends(get_coach_id)):
    """List all exercises for the coach."""
    supabase = get_supabase_client()

    response = (
        supabase.table("exercises")
        .select("*")
        .eq("coach_id", coach_id)
        .order("created_at", desc=True)
        .execute()
    )

    return {"exercises": response.data}


@router.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: str, coach_id: str = Depends(get_coach_id)):
    """Get a specific exercise."""
    supabase = get_supabase_client()

    response = (
        supabase.table("exercises")
        .select("*")
        .eq("id", exercise_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return response.data


@router.post("/exercises", response_model=ExerciseResponse)
async def create_exercise(
    exercise: ExerciseCreate, coach_id: str = Depends(get_coach_id)
):
    """Create a new exercise with AI-generated tags."""
    supabase = get_supabase_client()

    # Generate AI tags
    ai_tags = await ai_service.generate_exercise_tags(
        name=exercise.name,
        description=exercise.description,
        category=exercise.category.value,
        equipment=exercise.equipment,
    )

    now = datetime.now(timezone.utc).isoformat()

    exercise_data = {
        "coach_id": coach_id,
        "name": exercise.name,
        "description": exercise.description,
        "youtube_url": exercise.youtube_url,
        "manual_tags": exercise.manual_tags,
        "ai_tags": ai_tags,
        "category": exercise.category.value,
        "equipment": exercise.equipment,
        "created_at": now,
        "updated_at": now,
    }

    response = supabase.table("exercises").insert(exercise_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create exercise")

    return response.data[0]


@router.patch("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: str,
    exercise: ExerciseUpdate,
    coach_id: str = Depends(get_coach_id),
):
    """Update an exercise."""
    supabase = get_supabase_client()

    # Verify ownership
    existing = (
        supabase.table("exercises")
        .select("id")
        .eq("id", exercise_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not existing.data:
        raise HTTPException(status_code=404, detail="Exercise not found")

    update_data = {k: v for k, v in exercise.model_dump().items() if v is not None}

    if "category" in update_data:
        update_data["category"] = update_data["category"].value

    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Regenerate AI tags if relevant fields changed
    if any(k in update_data for k in ["name", "description", "category", "equipment"]):
        # Get current data
        current = (
            supabase.table("exercises")
            .select("*")
            .eq("id", exercise_id)
            .single()
            .execute()
        )

        merged = {**current.data, **update_data}
        ai_tags = await ai_service.generate_exercise_tags(
            name=merged["name"],
            description=merged["description"],
            category=merged["category"],
            equipment=merged.get("equipment", []),
        )
        update_data["ai_tags"] = ai_tags

    response = (
        supabase.table("exercises")
        .update(update_data)
        .eq("id", exercise_id)
        .execute()
    )

    return response.data[0]


@router.delete("/exercises/{exercise_id}")
async def delete_exercise(exercise_id: str, coach_id: str = Depends(get_coach_id)):
    """Delete an exercise."""
    supabase = get_supabase_client()

    # Verify ownership
    existing = (
        supabase.table("exercises")
        .select("id")
        .eq("id", exercise_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not existing.data:
        raise HTTPException(status_code=404, detail="Exercise not found")

    supabase.table("exercises").delete().eq("id", exercise_id).execute()

    return {"message": "Exercise deleted"}
