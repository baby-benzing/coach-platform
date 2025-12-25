from supabase import create_client, Client
from config import get_settings


def get_supabase_client() -> Client:
    """Get Supabase client with service key for backend operations."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_supabase_admin() -> Client:
    """Alias for service client."""
    return get_supabase_client()
