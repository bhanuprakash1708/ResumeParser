# Location: /src/worker/tasks.py

import time
import datetime
import uuid
import os
import json

# --- AI IMPORTS ---
import google.generativeai as genai
from src.core.config import settings

# --- PARSING LIBRARIES ---
import pdfplumber 
import docx

# --- NEW OCR IMPORTS ---
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
# ------------------------

from src.worker.celery_app import celery_app
from src.db.session import SessionLocal
from src.db.models import Resume

# --- CONFIGURE THE GEMINI CLIENT ---
try:
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # This is the model name you verified:
        gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        print("--- Gemini Pro model configured successfully ---")
    else:
        print("!!! WARNING: GEMINI_API_KEY is not set. AI extraction will be skipped. !!!")
        gemini_model = None
except Exception as e:
    print(f"!!! CRITICAL: FAILED TO CONFIGURE GEMINI API. {e} !!!")
    gemini_model = None

# --- HELPER FUNCTIONS (WITH OCR) ---

def ocr_pdf(file_path: str) -> str:
    """
    Extracts text from a scanned/image-based PDF using Tesseract OCR.
    """
    print(f"Running OCR on PDF: {file_path}")
    try:
        images = convert_from_path(file_path, poppler_path=None)
        full_text = ""
        for img in images:
            full_text += pytesseract.image_to_string(img) + "\n"
        print(f"OCR extraction successful, {len(full_text)} chars.")
        return full_text
    except Exception as e:
        print(f"Error during OCR: {e}")
        raise

def parse_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    Tries fast text extraction first, then falls back to slow OCR.
    """
    print(f"Parsing PDF: {file_path}")
    text = ""
    try:
        # 1. Try fast text-based extraction
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        # 2. If it's empty, it's a scanned PDF. Fallback to OCR.
        if len(text.strip()) < 10: 
            print("No text found. Assuming scanned PDF. Falling back to OCR...")
            text = ocr_pdf(file_path)
        else:
            print(f"Text-based PDF extraction successful, {len(text)} chars.")
        
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        try:
            print("pdfplumber failed. Trying OCR as a last resort...")
            text = ocr_pdf(file_path)
            return text
        except Exception as ocr_e:
            print(f"Both text extraction and OCR failed: {ocr_e}")
            raise ocr_e

def parse_docx(file_path: str) -> str:
    print(f"Parsing DOCX: {file_path}")
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        print(f"DOCX extraction successful, {len(text)} chars.")
        return text
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        raise

def parse_txt(file_path: str) -> str:
    print(f"Parsing TXT: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"TXT extraction successful, {len(text)} chars.")
        return text
    except Exception as e:
        print(f"Error parsing TXT: {e}")
        raise

# --- AI PROMPT ENGINEERING ---

def get_gemini_extraction_prompt(raw_text: str) -> str:
    """
    Creates the master prompt to send to the Gemini API.
    This is the most important part of the AI logic.
    """
    
    # --- THIS IS THE FIX ---
    # This template now *perfectly* matches your schemas.py file
    json_format_template = """
    {
      "personalInfo": {
        "name": { "first": "John", "last": "Doe", "full": "John Doe" },
        "contact": {
          "email": "john.doe@example.com",
          "phone": "+1-555-123-4567",
          "address": { "city": "San Francisco", "state": "CA", "country": "USA" },
          "linkedin": "https.linkedin.com/in/johndoe"
        }
      },
      "summary": {
        "text": "Experienced software engineer with 5+ years...",
        "careerLevel": "mid-level"
      },
      "experience": [
        {
          "title": "Senior Software Engineer",
          "company": "Tech Corp",
          "location": "San Francisco, CA",
          "startDate": "2021-03-01",
          "endDate": "2025-09-01",
          "description": "Led development of microservices...",
          "technologies": ["Python", "Docker", "AWS"]
        }
      ],
      "education": [
        {
          "degree": "Bachelor of Science",
          "field": "Computer Science",
          "institution": "University of California, Berkeley",
          "graduationDate": "2018-05-15"
        }
      ],
      "skills": {
        "technical": [
          {
            "category": "Programming Languages",
            "items": ["Python", "JavaScript", "Java", "Go"]
          },
          {
            "category": "Frameworks",
            "items": ["Django", "React", "Node.js"]
          }
        ],
        "soft": ["Leadership", "Communication", "Problem Solving"],
        "languages": [
          {
            "language": "English",
            "proficiency": "Native"
          }
        ]
      },
      "certifications": [
         {
           "name": "AWS Certified Solutions Architect",
           "issuer": "Amazon Web Services",
           "issueDate": "2023-06-15"
         }
      ]
    }
    """
    
    # The prompt tells the AI what to do
    prompt = f"""
    You are an expert AI resume parser. Your task is to analyze the following resume text and extract the key information.
    You MUST return the output *only* as a single, valid JSON object.
    Do not include any text, markdown (like ```json), or explanations before or after the JSON block.
    
    JSON FORMAT TEMPLATE:
    {json_format_template}
    
    ---
    RESUME TEXT TO PARSE:
    {raw_text}
    ---
    
    Now, parse the resume text and provide the output in the requested JSON format.
    If a field is not found, return null or an empty list [].
    """
    return prompt


# --- THE MAIN TASK ---

@celery_app.task
def parse_resume_task(resume_id_str: str):
    """
    This background task now does:
    1. Text extraction (PDF, DOCX, TXT)
    2. AI-powered JSON parsing (using Gemini Pro)
    """
    print(f"--- [TASK_STARTED] for resume_id: {resume_id_str} ---")
    db = SessionLocal()
    file_name = "Unknown" 
    
    try:
        resume_id = uuid.UUID(resume_id_str)
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        file_name = resume.file_name if resume else "Unknown"

        if not resume:
            print(f"[TASK_ERROR] Resume with id {resume_id_str} not found.")
            return f"Failed: Resume {resume_id_str} not found"
        if not resume.file_path or not os.path.exists(resume.file_path):
            print(f"[TASK_ERROR] File not found at path: {resume.file_path}")
            raise Exception("File not found on server.")

        resume.processing_status = "processing"
        db.commit()

        # --- STEP A: REAL TEXT EXTRACTION (NOW WITH OCR) ---
        raw_text = ""
        file_type = resume.file_type.lower()
        print(f"Dispatching task for file type: {file_type}")
        
        if 'pdf' in file_type:
            raw_text = parse_pdf(resume.file_path)
        elif 'word' in file_type or 'officedocument' in file_type:
            raw_text = parse_docx(resume.file_path)
        elif 'text' in file_type:
            raw_text = parse_txt(resume.file_path)
        else:
            raise Exception(f"Unsupported file type: {file_type}")
        
        resume.raw_text = raw_text
        
        # --- STEP B: AI JSON EXTRACTION ---
        if not gemini_model:
            print("!!! WARNING: Gemini model not configured. Skipping AI extraction. !!!")
            extracted_json = {"error": "AI model not configured."}
        else:
            print(f"Sending {len(raw_text)} chars to Gemini Pro for extraction...")
            
            if len(raw_text.strip()) < 10:
                print("[TASK_WARNING] Skipping AI call due to empty extracted text.")
                extracted_json = {"error": "No text could be extracted from the document."}
            else:
                extraction_prompt = get_gemini_extraction_prompt(raw_text)
                
                # Set safety settings to be less restrictive
                generation_config = genai.types.GenerationConfig(
                    temperature=0.1 
                )
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                response = gemini_model.generate_content(
                    extraction_prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                
                # Clean the response - AI sometimes wraps output in ```json ... ```
                ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
                
                # Convert the text response to a real JSON object
                extracted_json = json.loads(ai_response_text)
                
                print("--- [AI_SUCCESS] Gemini extraction complete ---")

        # --- STEP C: SAVE RESULTS ---
        resume.processing_status = "completed"
        resume.processed_at = datetime.datetime.now(datetime.timezone.utc)
        resume.structured_data = extracted_json # <-- STORE THE AI's JSON
        db.commit()
        
        print(f"--- [TASK_COMPLETED] for {resume.file_name} ---")
        return f"Successfully processed {resume.file_name}"

    except Exception as e:
        print(f"[TASK_FAILED] Error processing {resume_id_str}: {e}")
        db.rollback() 
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            resume.processing_status = "failed"
            db.commit()
        return f"Failed to process {file_name}"
            
    finally:
        db.close()