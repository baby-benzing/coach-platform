from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_service_key: str
    supabase_jwt_secret: str

    # Anthropic
    anthropic_api_key: str

    # Email
    resend_api_key: str
    from_email: str = "noreply@coach-platform.com"

    # App
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
