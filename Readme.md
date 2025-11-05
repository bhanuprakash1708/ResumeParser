# AI-Powered Resume Parser (Hackathon Submission)

This is a high-performance, asynchronous resume parsing API built with Python, FastAPI, and Docker. It uses a Celery worker and Redis queue to process file uploads in the background, calling the Google Gemini Pro API to extract and analyze resume data from multiple file formats (including scanned PDFs via Tesseract OCR).

---

## Tech Stack

* **Backend:** Python 3.11, FastAPI
* **Database:** PostgreSQL
* **Async Processing:** Celery & Redis
* **AI Model:** Google Gemini 2.5 Pro (via `google-generativeai`)
* **Parsing:** `pdfplumber`, `python-docx`
* **OCR:** `pytesseract`, `pdf2image`
* **Containerization:** Docker & Docker Compose

---

## How to Run

### Prerequisites

* Git
* Docker Desktop (must be running)
* Python 3.11+ (for local editor support)

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name