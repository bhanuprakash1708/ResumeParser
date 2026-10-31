from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.session import engine
from src.db import models
from src.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- API is starting up! ---")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("--- Database tables initialized ---")
    except Exception as e:
        print(f"Warning: could not connect to database on startup: {e}")
    yield

app = FastAPI(
    title="AI-Powered Resume Parser",
    version="1.0",
    description="Hackathon project for parsing resumes with AI.",
    lifespan=lifespan
)

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static files for the frontend dashboard
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- Health Check Endpoint ---
@app.get("/health", tags=["General"])
async def get_health():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "API is healthy"}

# --- Include the v1 API routes ---
# All routes in api_router will be prefixed with /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint serving the interactive ResumeAI Studio frontend.
    """
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to the AI Resume Parser API"}