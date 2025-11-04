# Location: /src/api/v1/endpoints/resumes.py

import shutil
import hashlib
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models import Resume
from src.worker.tasks import parse_resume_task 

# --- IMPORT OUR NEW RESPONSE MODELS ---
from src.api.v1.schemas import ResumeDataResponse, ResumeMetadata
# ------------------------------------

router = APIRouter()

# Define the upload directory (relative to the /app directory in container)
UPLOAD_DIR = "/app/uploads"

def get_file_hash(file):
    """Calculates the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_sha256.update(chunk)  
    file.seek(0)
    return hash_sha256.hexdigest()

def save_upload_file(file: UploadFile, resume_id: uuid.UUID) -> str:
    """
    Saves the uploaded file to the UPLOAD_DIR using its resume_id as the filename.
    Returns the file path.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension: # Handle cases like 'Resume' with no extension
        file_extension = ".dat" # Use a generic extension
        
    file_path = os.path.join(UPLOAD_DIR, f"{str(resume_id)}{file_extension}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    return file_path


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Upload a resume file.

    This endpoint now:
    1. Validates the file.
    2. Creates a 'pending' DB record.
    3. Saves the file to disk.
    4. Dispatches a background job to Celery for processing.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # --- 1. Calculate hash to check for duplicates ---
    file_hash = get_file_hash(file.file)
    
    existing_resume = db.query(Resume).filter(Resume.file_hash == file_hash).first()
    if existing_resume:
        raise HTTPException(
            status_code=400, 
            detail=f"Duplicate file. Resume already exists with ID: {existing_resume.id}"
        )

    # --- 2. Create the new resume record in the DB ---
    new_resume = Resume(
        id=uuid.uuid4(), # Generate a new UUID
        file_name=file.filename,
        file_size=file.size,
        file_type=file.content_type,
        file_hash=file_hash,
        processing_status='pending'
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    # --- 3. Save the file to disk using its new ID ---
    # We save *after* creating the DB entry so we can use the ID
    try:
        saved_file_path = save_upload_file(file, new_resume.id)
        
        # --- Store the path in the DB ---
        new_resume.file_path = saved_file_path 
        db.commit() # Save this new path
        
    except Exception as e:
        print(f"Error saving file: {e}")
        new_resume.processing_status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # --- 4. Dispatch the background task ---
    # We pass the ID as a string, as it's best practice for Celery
    parse_resume_task.delay(str(new_resume.id))
    print(f"Dispatched task for resume_id: {new_resume.id}")

    # This response matches the hackathon spec
    return {
        "id": new_resume.id,
        "status": new_resume.processing_status,
        "message": "Resume uploaded successfully, queued for processing.",
        "estimatedProcessingTime": 30 # Placeholder
    }

# --- THIS IS THE NEW ENDPOINT ---
@router.get("/{id}", response_model=ResumeDataResponse)
async def get_parsed_resume(
    id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve the full, structured JSON data for a processed resume.
    """
    try:
        resume_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resume ID format.")

    resume = db.query(Resume).filter(Resume.id == resume_uuid).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    if resume.processing_status != "completed":
        raise HTTPException(
            status_code=202, # 202 "Accepted" is a good code for "not ready yet"
            detail=f"Resume processing is not complete. Current status: {resume.processing_status}"
        )

    # --- Build the response model ---
    # FastAPI will automatically validate this against our schema.
    
    # Get the structured data (which is a dict) from the DB
    ai_data = resume.structured_data or {}

    # Build the metadata
    metadata = ResumeMetadata(
        fileName=resume.file_name,
        fileSize=resume.file_size,
        uploadedAt=resume.uploaded_at,
        processedAt=resume.processed_at,
        processingTime=(resume.processed_at - resume.uploaded_at).total_seconds() if resume.processed_at else None
    )

    # Use the `get` method on the dict to safely get keys that might not exist
    response_data = ResumeDataResponse(
        id=resume.id,
        metadata=metadata,
        personalInfo=ai_data.get("personalInfo"),
        summary=ai_data.get("summary"),
        experience=ai_data.get("experience"),
        education=ai_data.get("education"),
        skills=ai_data.get("skills"),
        certifications=ai_data.get("certifications"),
        aiEnhancements=ai_data.get("aiEnhancements") # This will be null for now
    )
    
    return response_data
# -----------------------------------


@router.get("/{id}/status")
async def get_resume_status(
    id: str, 
    db: Session = Depends(get_db)
):
    """
    Get the processing status of a resume by its ID.
    """
    try:
        resume_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resume ID format.")

    resume = db.query(Resume).filter(Resume.id == resume_uuid).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    return {
        "id": resume.id,
        "status": resume.processing_status,
        "fileName": resume.file_name,
        "uploadedAt": resume.uploaded_at,
        "processedAt": resume.processed_at
    }