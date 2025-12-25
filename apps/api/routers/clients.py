from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone

from auth import get_current_user, get_coach_id
from database import get_supabase_client
from schemas import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter()


@router.get("/clients", response_model=dict)
async def list_clients(coach_id: str = Depends(get_coach_id)):
    """List all clients for the coach."""
    supabase = get_supabase_client()

    response = (
        supabase.table("clients")
        .select("*")
        .eq("coach_id", coach_id)
        .order("created_at", desc=True)
        .execute()
    )

    return {"clients": response.data}


@router.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: str, coach_id: str = Depends(get_coach_id)):
    """Get a specific client."""
    supabase = get_supabase_client()

    response = (
        supabase.table("clients")
        .select("*")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Client not found")

    return response.data


@router.post("/clients", response_model=ClientResponse)
async def create_client(client: ClientCreate, coach_id: str = Depends(get_coach_id)):
    """Create a new client."""
    supabase = get_supabase_client()

    now = datetime.now(timezone.utc).isoformat()

    client_data = {
        "coach_id": coach_id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
        "date_of_birth": client.date_of_birth,
        "created_at": now,
        "updated_at": now,
    }

    response = supabase.table("clients").insert(client_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create client")

    return response.data[0]


@router.patch("/clients/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    client: ClientUpdate,
    coach_id: str = Depends(get_coach_id),
):
    """Update a client."""
    supabase = get_supabase_client()

    # Verify ownership
    existing = (
        supabase.table("clients")
        .select("id")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not existing.data:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = {k: v for k, v in client.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    response = (
        supabase.table("clients").update(update_data).eq("id", client_id).execute()
    )

    return response.data[0]


@router.delete("/clients/{client_id}")
async def delete_client(client_id: str, coach_id: str = Depends(get_coach_id)):
    """Delete a client."""
    supabase = get_supabase_client()

    # Verify ownership
    existing = (
        supabase.table("clients")
        .select("id")
        .eq("id", client_id)
        .eq("coach_id", coach_id)
        .single()
        .execute()
    )

    if not existing.data:
        raise HTTPException(status_code=404, detail="Client not found")

    supabase.table("clients").delete().eq("id", client_id).execute()

    return {"message": "Client deleted"}
