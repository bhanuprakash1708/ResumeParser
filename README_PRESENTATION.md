# 📽️ Automated Resume Parser and Email Notifier
## Technical Presentation Deck & DevOps Architecture Suite

This repository contains the presentation suite, source generation script, CI/CD pipeline definition, and architectural documentation for the **Automated Resume Parser and Email Notifier**.

---

### 📦 Presentation Deliverables
* **Editable PowerPoint File**: [`Automated_Resume_Parser_and_Email_Notifier.pptx`](file:///c:/Users/bhanu/OneDrive/Desktop/Devops/resume-parser-hackathon/Automated_Resume_Parser_and_Email_Notifier.pptx)
* **Python Generator Script**: [`generate_presentation.py`](file:///c:/Users/bhanu/OneDrive/Desktop/Devops/resume-parser-hackathon/generate_presentation.py)
* **Jenkins Pipeline Definition**: [`Jenkinsfile`](file:///c:/Users/bhanu/OneDrive/Desktop/Devops/resume-parser-hackathon/Jenkinsfile)
* **Slide Aspect Ratio**: 16:9 Widescreen (13.333" × 7.5")
* **Color Palette**: Deep Obsidian Navy (`#0B1120`), Slate Navy Containers (`#182136`), Vibrant Cyan (`#06B6D4`), Electric Indigo (`#6366F1`), and Emerald Green (`#10B981`).

---

### 📑 16-Slide Technical Structure & Synopsis

| Slide # | Category | Slide Title | Key Technical Content |
| :---: | :--- | :--- | :--- |
| **01** | **Title Slide** | Project Title & Metadata | Capstone credentials, Tech Stack: Python + FastAPI + Celery + Redis + Jenkins, DevOps Focus, and Outcome. |
| **02** | **Executive Overview** | Bridging Talent Acquisition & DevOps Automation | Eliminating hiring latency via sub-50ms async ingestion, distributed job offloading, and continuous deployment. |
| **03** | **Problem Statement** | The Recruiter Dilemma & Architectural Bottlenecks | Recruiter manual overhead, synchronous web server freezing (HTTP 504), communication black hole, and deployment drift. |
| **04** | **Tech Stack** | Production-Grade Tech Stack Breakdown | 4-quadrant breakdown: Core Backend (FastAPI, Python 3.11+), Queue (Celery, Redis), DevOps (Jenkins, Docker), AI/OCR (Gemini Pro, Tesseract). |
| **05** | **Architecture** | End-to-End Microservice Topology & Data Flow | 5-stage decoupled data flow: Client Ingestion → FastAPI Gateway → Redis Broker → Celery Worker → PostgreSQL & Email Notifier. |
| **06** | **DevOps Focus #1** | Background Job Automation with Celery & Redis | Decoupling I/O from compute, task state lifecycles (`pending` → `processing` → `completed`), worker concurrency pools, and retry policies. |
| **07** | **DevOps Focus #2** | Jenkins CI/CD Pipeline Automation | 6-stage declarative `Jenkinsfile`: Checkout, Flake8 linting, Pytest test suite, Docker build, security scan, and curl health check. |
| **08** | **DevOps Focus #3** | Dual-Tier Automated Notification System | Tier 1: Candidate receipts, scorecards, and recruiter high-match alerts. Tier 2: Jenkins pipeline failure/success webhooks. |
| **09** | **Ingestion Engine** | Universal Multi-Format Ingestion & Tesseract OCR | Digital PDFs (`pdfplumber`), Scanned/Image PDFs (`pytesseract` + `poppler`), Word docs (`python-docx`), SHA-256 deduplication, 10MB limits. |
| **10** | **AI Cognition** | AI-Powered Structured Extraction & Analysis | Google Gemini 2.5 Pro with strict JSON schema prompts, extracting personalInfo, experience, skills, and the `aiEnhancements` block. |
| **11** | **Automated Filtering** | Intelligent Resume-Job Filtering & Semantic Match | `POST /resumes/{id}/match` engine: multidimensional compatibility scoring, automated gap analysis, and candidate shortlisting. |
| **12** | **Orchestration** | Docker & Multi-Container Topology | 4-service Docker Compose mesh (`api`, `worker`, `redis`, `db`), shared volumes, persistent data, and non-root container security. |
| **13** | **Quality Assurance** | Automated Pytest Suite & Pipeline Guardrails | Asynchronous test client (`httpx`), Celery task mocking (`mocker.patch`), 10MB boundary validation, and CI deployment gates. |
| **14** | **Project Deliverables**| Automating Job Queues & Filtering via CI | Direct fulfillment of project outcome: automated job queue that ingests, OCR-extracts, filters, and notifies using CI. |
| **15** | **User Experience** | Interactive ResumeAI Studio Dashboard | Glassmorphic web UI, drag-and-drop file upload, real-time polling spinner, interactive scorecard, and Job Matcher studio. |
| **16** | **Future Scope** | Production Roadmap & Executive Takeaways | Kubernetes autoscaling with KEDA, cloud object storage (S3), enterprise ATS webhooks (Workday, Greenhouse), and summary. |

---

### 🎙️ Embedded Speaker Notes & Evaluation Preparation
Every single slide in [`Automated_Resume_Parser_and_Email_Notifier.pptx`](file:///c:/Users/bhanu/OneDrive/Desktop/Devops/resume-parser-hackathon/Automated_Resume_Parser_and_Email_Notifier.pptx) includes comprehensive speaker notes with:
1. **`[SPEAKER SCRIPT: WHAT TO SAY]`**: Verbatim, professional presentation script for the speaker.
2. **`[WHY THIS SLIDE MATTERS TO EVALUATORS]`**: Evaluation justification and architectural significance.
3. **`[DEVOPS & UNDER-THE-HOOD TECHNICAL MECHANICS]`**: Concurrency models, broker protocols, and pipeline execution mechanics.
4. **`[LIKELY VIVA / EVALUATOR QUESTIONS & BULLETPROOF ANSWERS]`**: Exact questions technical judges ask paired with precise model answers.

---

### 🛠️ How to Regenerate or Customize the Presentation
To regenerate the PowerPoint file or adjust color themes and metadata, run:
```powershell
# Using the project's virtual environment:
.\venv\Scripts\python generate_presentation.py
```
This will compile and update [`Automated_Resume_Parser_and_Email_Notifier.pptx`](file:///c:/Users/bhanu/OneDrive/Desktop/Devops/resume-parser-hackathon/Automated_Resume_Parser_and_Email_Notifier.pptx) in seconds.
