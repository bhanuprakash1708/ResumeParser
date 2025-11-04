# Location: /src/worker/tasks.py
import time
import datetime
import uuid

from src.worker.celery_app import celery_app
from src.db.session import SessionLocal
from src.db.models import Resume

@celery_app.task
def parse_resume_task(resume_id_str: str):
    """
    This is the background task that does the heavy lifting.
    """
    print(f"--- [TASK_STARTED] for resume_id: {resume_id_str} ---")
    
    # The worker is a separate app, so it needs its own DB session
    db = SessionLocal()
    try:
        resume_id = uuid.UUID(resume_id_str)
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not resume:
            print(f"[TASK_ERROR] Resume with id {resume_id_str} not found.")
            return

        # 1. Update status to 'processing'
        resume.processing_status = "processing"
        db.commit()

        # --- THIS IS THE "BRAIN" ---
        # For Phase 3, we just sleep for 10 seconds to simulate work.
        # In Phase 4, we'll replace this with real PDF parsing logic.
        print(f"[TASK_PROCESSING] Parsing {resume.file_name}... This will take 10 seconds.")
        time.sleep(10)
        fake_raw_text = f"This is the parsed text for {resume.file_name}."
        # -----------------------------

        # 2. Update status to 'completed'
        resume.processing_status = "completed"
        resume.processed_at = datetime.datetime.now(datetime.timezone.utc)
        resume.raw_text = fake_raw_text # Store the "parsed" text
        db.commit()
        
        print(f"--- [TASK_COMPLETED] for {resume.file_name} ---")

    except Exception as e:
        print(f"[TASK_FAILED] Error processing {resume_id_str}: {e}")
        # Rollback changes and set status to 'failed'
        db.rollback()
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            resume.processing_status = "failed"
            db.commit()
    finally:
        # Always close the session
        db.close()

    return f"Successfully processed {resume.file_name}"