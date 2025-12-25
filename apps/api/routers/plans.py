from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timezone
from typing import Optional
import asyncio

from auth import get_current_user, get_coach_id
from database import get_supabase_client
from schemas import PlanCreate, PlanResponse, WorkoutDayResponse, PlanGenerateRequest
from services import EmailService
from agents import WorkoutPlanningAgent

router = APIRouter()
email_service = EmailService()


@router.get("/plans", response_model=dict)
async def list_plans(
    client_id: Optional[str] = Query(None),
    coach_id: str = Depends(get_coach_id),
):
    """List all workout plans, optionally filtered by client."""
    supabase = get_supabase_client()

    query = supabase.table("workout_plans").select("*").eq("coach_id", coach_id)

    if client_id:
        query = query.eq("client_id", client_id)

    response = query.order("created_at", desc=True).execute()

    return {"plans": response.data}


@router.get("/plans/{plan_id}", response_model=dict)
async def get_plan(plan_id: str, coach_id: str = Depends(get_coach_id)):
    """Get a specific workout plan with all days."""
    supabase = get_supabase_client()

    # Get plan
    plan_response = (
        supabase.table("workout_plans")
        .select("*")
        .eq("id", plan_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not plan_response.data:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Get workout days
    days_response = (
        supabase.table("workout_days")
        .select("*")
        .eq("plan_id", plan_id)
        .order("week_number")
        .order("day_of_week")
        .execute()
    )

    return {"plan": plan_response.data, "days": days_response.data}


@router.post(
    "/clients/{client_id}/assessments/{assessment_id}/generate-plan",
    response_model=dict,
)
async def generate_plan(
    client_id: str,
    assessment_id: str,
    request: PlanGenerateRequest,
    user: dict = Depends(get_current_user),
):
    """Generate a workout plan from an assessment."""
    supabase = get_supabase_client()
    coach_id = user["id"]

    # Verify client ownership
    client = (
        supabase.table("clients")
        .select("*")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get assessment
    assessment = (
        supabase.table("assessments")
        .select("*")
        .eq("id", assessment_id)
        .eq("client_id", client_id)
        .single()
        .execute()
    )

    if not assessment.data:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Get coach's exercises
    exercises = (
        supabase.table("exercises").select("*").eq("coach_id", coach_id).execute()
    )

    # Get coach's training philosophy
    training_philosophy = user.get("user_metadata", {}).get("training_philosophy", "")

    # Generate plan using the agentic workflow
    agent = WorkoutPlanningAgent(coach_philosophy=training_philosophy)

    # Prepare assessment data for agent
    agent_assessment = {
        **assessment.data,
        "client_name": client.data.get("name", "Client"),
    }

    # Run the agent to generate the plan
    plan_data = await agent.generate_plan(
        assessment=agent_assessment,
        coach_preferences=request.coach_preferences.model_dump(),
        exercises=exercises.data if exercises.data else None,
    )

    now = datetime.now(timezone.utc)

    # Create workout plan
    plan_record = {
        "client_id": client_id,
        "coach_id": coach_id,
        "name": plan_data["name"],
        "start_date": now.isoformat(),
        "weeks": plan_data["weeks"],
        "status": "draft",
        "coach_notes": plan_data.get("notes"),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }

    plan_response = supabase.table("workout_plans").insert(plan_record).execute()

    if not plan_response.data:
        raise HTTPException(status_code=500, detail="Failed to create plan")

    plan_id = plan_response.data[0]["id"]

    # Create workout days
    for day_data in plan_data.get("workout_days", []):
        day_record = {
            "plan_id": plan_id,
            "week_number": day_data["week_number"],
            "day_of_week": day_data["day_of_week"],
            "name": day_data["name"],
            "focus": day_data["focus"],
            "exercises": day_data["exercises"],
            "notes": day_data.get("notes"),
        }
        supabase.table("workout_days").insert(day_record).execute()

    return {
        "plan": plan_response.data[0],
        "message": "Workout plan generated successfully",
    }


@router.post("/plans/{plan_id}/send-email", response_model=dict)
async def send_plan_email(plan_id: str, user: dict = Depends(get_current_user)):
    """Send workout plan via email to coach and client."""
    supabase = get_supabase_client()
    coach_id = user["id"]

    # Get plan
    plan = (
        supabase.table("workout_plans")
        .select("*")
        .eq("id", plan_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not plan.data:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Get client
    client = (
        supabase.table("clients")
        .select("*")
        .eq("id", plan.data["client_id"])
        .single()
        .execute()
    )

    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get workout days
    days = (
        supabase.table("workout_days")
        .select("*")
        .eq("plan_id", plan_id)
        .order("week_number")
        .order("day_of_week")
        .execute()
    )

    plan_data_for_email = {
        **plan.data,
        "days": days.data,
    }

    coach_name = user.get("user_metadata", {}).get("name", "Your Coach")
    coach_email = user.get("email", "")

    success = await email_service.send_workout_plan(
        coach_email=coach_email,
        coach_name=coach_name,
        client_email=client.data["email"],
        client_name=client.data["name"],
        plan_name=plan.data["name"],
        plan_data=plan_data_for_email,
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")

    # Update plan status to active
    supabase.table("workout_plans").update(
        {"status": "active", "updated_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", plan_id).execute()

    return {"message": "Plan sent successfully"}


@router.patch("/plans/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: str,
    status: Optional[str] = None,
    coach_notes: Optional[str] = None,
    coach_id: str = Depends(get_coach_id),
):
    """Update a workout plan."""
    supabase = get_supabase_client()

    # Verify ownership
    existing = (
        supabase.table("workout_plans")
        .select("id")
        .eq("id", plan_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not existing.data:
        raise HTTPException(status_code=404, detail="Plan not found")

    update_data = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if status:
        update_data["status"] = status
    if coach_notes is not None:
        update_data["coach_notes"] = coach_notes

    response = (
        supabase.table("workout_plans").update(update_data).eq("id", plan_id).execute()
    )

    return response.data[0]
