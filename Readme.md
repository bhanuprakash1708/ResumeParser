🧠 AI-Powered Resume Parser (Hackathon Submission)

An AI-driven, high-performance Resume Parsing API, built in 48 hours for the AI-Powered Resume Parser Hackathon.

It’s designed for speed, scalability, and intelligence, featuring an asynchronous backend powered by FastAPI, Celery, Redis, and PostgreSQL.
The system automatically extracts and structures information from resumes — even scanned PDFs — using Google Gemini 2.5 Pro for advanced understanding and structured JSON output.

🚀 Core Features

✅ Asynchronous API

Non-blocking /upload endpoint — returns instantly (<1s).

Heavy tasks like OCR and AI calls are handled in the background.

✅ Background Worker (Celery)

A separate worker process handles long-running parsing jobs.

Keeps the main API responsive under heavy load.

✅ Multi-Format Ingestion

.pdf (text-based): via pdfplumber

.pdf (scanned/image): via Tesseract OCR fallback

.docx: via python-docx

.txt: via standard Python I/O

✅ AI-Powered Extraction (Gemini 2.5 Pro)

Uses gemini-2.5-pro model for accurate, structured parsing.

Returns output conforming to a strict Pydantic schema (using Gemini’s response_schema).

✅ Guaranteed Structured Output

AI is forced to return valid JSON that matches the schema exactly.

✅ Intelligent Enhancements

Generates an aiEnhancements block with:

qualityScore

completenessScore

industryFit

careerProgressionAnalysis

✅ Database Storage

Uses PostgreSQL with a JSONB column for efficient structured data storage.

✅ Full RESTful API Documentation

Auto-generated OpenAPI 3.1.x docs available at /docs.

🧩 Tech Stack & Architecture

A microservice-oriented architecture ensures performance, scalability, and modularity.
The system consists of four Docker containers:

Service	Technology	Role
api	FastAPI	Handles HTTP requests, validates uploads, manages job lifecycle
worker	Celery	Processes queued parsing tasks, runs OCR + AI calls
redis	Redis	Message broker between API and Worker
db	PostgreSQL	Stores metadata and parsed JSON results
🔄 Data Flow (Step-by-Step)

Upload → User POSTs a file to /api/v1/resumes/upload.

Validation → API hashes the file (duplicate check) and stores it in /uploads/.

Database Entry → Adds a row with status: "pending".

Queue Job → Sends a message to Redis:

{"task": "parse_resume", "resume_id": "..."}


Instant Response → Returns a 200 OK in ~50ms with job ID.

⚙️ Background Processing

Worker Activation → Celery worker detects the new task in Redis.

Status Update → Changes status to "processing".

Text Extraction →

Uses pdfplumber → fallback to Tesseract OCR if image-based.

AI Parsing →

Sends extracted text to Gemini 2.5 Pro

Enforces structured JSON via response_schema

Store Results → Saves JSON in DB under structured_data.

Mark Complete → Sets status to "completed".

Retrieve → User calls GET /api/v1/resumes/{id} to view results.

🛠️ How to Run Locally
Prerequisites

Git

Docker Desktop
 (must be running)

1️⃣ Clone the Repository
git clone https://github.com/gouravez/ai-resume-parser.git
cd ai-resume-parser

2️⃣ Configure Environment

A Google Gemini API key is required.

Copy the example env file:

cp .env.example .env


Then open .env and set your Gemini API key:

# --- AI Model API Keys ---
GEMINI_API_KEY="AIzaSy...your...key...here"

3️⃣ Run the Application

This process ensures a clean build with all dependencies (including Tesseract).

Step 1: Clean Old Data
docker compose -f docker/docker-compose.yml down -v

Step 2: Force Rebuild
docker compose -f docker/docker-compose.yml build --no-cache

Step 3: Launch the System
docker compose -f docker/docker-compose.yml up

✅ You’re Live!

Once logs show:

[AI_SUCCESS] Gemini Pro model configured successfully (Structured Output Enabled)


Access your API docs at:
👉 http://localhost:8000/docs

🧪 Testing the Pipeline
Step 1: Upload a Resume

Open http://localhost:8000/docs

Go to POST /api/v1/resumes/upload

Click “Try it out”

Upload a resume file (e.g., Gourav_Resume.pdf)

Click Execute

💡 You’ll get a 200 OK response:

{
  "id": "bdf12c34-...",
  "status": "pending"
}

Step 2: Watch the Worker Logs

In your Docker terminal, you’ll see logs like:

[WORKER] Picked up job: parse_resume (id=bdf12c34)
[AI_SUCCESS] JSON Parsed Successfully
[TASK_COMPLETED] Resume parsing complete.

Step 3: Retrieve Final JSON

Copy the job ID from Step 1 and call:
GET /api/v1/resumes/{id}

Example output:

{
  "name": "Gourav Juneja",
  "email": "gourav@example.com",
  "skills": ["Python", "FastAPI", "Docker"],
  "experience": [...],
  "aiEnhancements": {
    "qualityScore": 0.92,
    "completenessScore": 0.87,
    "industryFit": "Software Engineering",
    "careerProgressionAnalysis": "Strong upward trend in backend development."
  }
}

🧰 Tech Summary
Component	Tool
Backend	FastAPI
Task Queue	Celery
Message Broker	Redis
Database	PostgreSQL (JSONB)
AI Model	Google Gemini 2.5 Pro
OCR	Tesseract
Document Parsing	pdfplumber, python-docx
Containerization	Docker Compose
🧑‍💻 Team & Credits

Built by: Gourav Juneja
Hackathon: AI-Powered Resume Parser (48-hour build)
Tech Focus: Distributed architecture, AI integration, and structured data extraction.
