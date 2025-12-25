from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import get_settings
from routers import exercises, clients, assessments, plans


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Coach Platform API...")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Coach Platform API",
    description="Backend API for the Coach Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
settings = get_settings()
origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(exercises.router, prefix="/api/v1", tags=["exercises"])
app.include_router(clients.router, prefix="/api/v1", tags=["clients"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])
app.include_router(plans.router, prefix="/api/v1", tags=["plans"])


@app.get("/")
async def root():
    return {"message": "Coach Platform API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
