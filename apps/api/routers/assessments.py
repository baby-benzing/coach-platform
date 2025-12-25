from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone

from auth import get_current_user, get_coach_id
from database import get_supabase_client
from schemas import AssessmentCreate, AssessmentResponse

router = APIRouter()


@router.get("/clients/{client_id}/assessments", response_model=dict)
async def list_assessments(client_id: str, coach_id: str = Depends(get_coach_id)):
    """List all assessments for a client."""
    supabase = get_supabase_client()

    # Verify client ownership
    client = (
        supabase.table("clients")
        .select("id")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")

    response = (
        supabase.table("assessments")
        .select("*")
        .eq("client_id", client_id)
        .order("assessment_date", desc=True)
        .execute()
    )

    return {"assessments": response.data}


@router.get(
    "/clients/{client_id}/assessments/{assessment_id}",
    response_model=AssessmentResponse,
)
async def get_assessment(
    client_id: str, assessment_id: str, coach_id: str = Depends(get_coach_id)
):
    """Get a specific assessment."""
    supabase = get_supabase_client()

    # Verify client ownership
    client = (
        supabase.table("clients")
        .select("id")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")

    response = (
        supabase.table("assessments")
        .select("*")
        .eq("id", assessment_id)
        .eq("client_id", client_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Assessment not found")

    return response.data


@router.post("/clients/{client_id}/assessments", response_model=AssessmentResponse)
async def create_assessment(
    client_id: str,
    assessment: AssessmentCreate,
    coach_id: str = Depends(get_coach_id),
):
    """Create a new assessment for a client."""
    supabase = get_supabase_client()

    # Verify client ownership
    client = (
        supabase.table("clients")
        .select("id")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")

    now = datetime.now(timezone.utc)

    assessment_data = {
        "client_id": client_id,
        "assessment_date": (
            assessment.assessment_date.isoformat()
            if assessment.assessment_date
            else now.isoformat()
        ),
        "personal_info": (
            assessment.personal_info.model_dump() if assessment.personal_info else None
        ),
        "body_metrics": (
            assessment.body_metrics.model_dump() if assessment.body_metrics else None
        ),
        "health_history": (
            assessment.health_history.model_dump() if assessment.health_history else None
        ),
        "injuries": assessment.injuries.model_dump() if assessment.injuries else None,
        "fitness_goals": (
            assessment.fitness_goals.model_dump() if assessment.fitness_goals else None
        ),
        "exercise_history": (
            assessment.exercise_history.model_dump()
            if assessment.exercise_history
            else None
        ),
        "lifestyle": assessment.lifestyle.model_dump() if assessment.lifestyle else None,
        "availability": (
            assessment.availability.model_dump() if assessment.availability else None
        ),
        "strength_baseline": (
            assessment.strength_baseline.model_dump()
            if assessment.strength_baseline
            else None
        ),
        "cardio_baseline": (
            assessment.cardio_baseline.model_dump()
            if assessment.cardio_baseline
            else None
        ),
        "fms_scores": (
            assessment.fms_scores.model_dump() if assessment.fms_scores else None
        ),
        "custom_fields": assessment.custom_fields,
        "created_at": now.isoformat(),
    }

    response = supabase.table("assessments").insert(assessment_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create assessment")

    return response.data[0]
