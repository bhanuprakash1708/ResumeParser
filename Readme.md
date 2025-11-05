# 🚀 AI-Powered Resume Parser Hackathon

An intelligent **Resume Parsing and Evaluation System** that extracts key information from resumes, stores structured data in a database, and provides a foundation for AI-based evaluation and matching.

---

## 📘 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [System Architecture](#system-architecture)
5. [Installation & Setup](#installation--setup)
6. [Project Structure](#project-structure)
7. [API Endpoints](#api-endpoints)
8. [Database Schema](#database-schema)
9. [Running with Docker](#running-with-docker)
10. [Future Enhancements](#future-enhancements)

---

## 🧠 Project Overview

This project was developed as part of the **AI-Powered Resume Parser Hackathon**.  
The system parses uploaded resumes, extracts relevant details such as name, contact info, skills, education, and experience, and stores them in a PostgreSQL database.  
It uses **FastAPI** for backend APIs and integrates with **AI models (Gemini API planned)** for intelligent parsing and scoring.

---

## ✨ Features

- 📤 **Resume Upload API** — Supports PDF and DOCX formats.  
- 🧾 **Automatic Parsing** — Extracts candidate information like:
  - Name, Email, Phone, Location
  - Education, Experience, Skills
- 🧠 **AI-Driven Extraction (Planned)** — Intelligent field detection using LLMs.
- 💾 **Database Integration** — Stores parsed resume data in PostgreSQL.
- ⚙️ **Docker Support** — Fully containerized setup.
- 📂 **RESTful API Endpoints** — Clean FastAPI routes.
- 🧪 **Swagger UI** for testing and documentation.

---

## 🛠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | FastAPI (Python) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **AI Integration** | Gemini API (planned) |
| **Containerization** | Docker & Docker Compose |
| **Frontend (optional)** | React.js (future) |

---

## 🧩 System Architecture

      ┌──────────────────────┐
      │      Frontend        │
      │ (React - optional)   │
      └──────────┬───────────┘
                 │ API Calls (JSON)
                 ▼
      ┌──────────────────────┐
      │     FastAPI Backend  │
      │  (Resume Parser API) │
      └──────────┬───────────┘
                 │ SQLAlchemy ORM
                 ▼
      ┌──────────────────────┐
      │     PostgreSQL DB    │
      │  (Structured Resume) │
      └──────────────────────┘

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/resume-parser-hackathon.git
cd resume-parser-hackathon
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # On Mac/Linux
venv\Scripts\activate        # On Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Configure Environment Variables
Create a .env file in the root directory:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/resume_parser
PORT=8000
```
### 5️⃣ Run the Application
```bash
uvicorn main:app --reload
```
Access API docs at:
```bash
👉 http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure
```bash
resume-parser-hackathon/
/
├── README.md
├── setup.sh
├── docs/
│   ├── api-specification.yaml
│   ├── architecture.md
│   └── deployment-guide.md
├── src/
│   └── [source code]
├── tests/
│   └── [test files]
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── .env.example
```
---
## 🧾 API Endpoints
### 1️⃣ Upload Resume

POST /api/v1/resume/upload

Description: Upload a resume file (PDF or DOCX) to parse.

Request:

Content-Type: multipart/form-data

File: resume

Response Example:
```bash
{
  "message": "Resume uploaded and parsed successfully.",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "FastAPI", "SQL"],
    "experience": [
      {"company": "ABC Corp", "role": "Backend Developer", "years": 2}
    ]
  }
}
```
### 2️⃣ Get Resume by ID
GET /api/v1/resume/{id}

Description: Fetch details of a specific resume.

Response Example:
```bash
{
  "id": 3,
  "name": "Alice Brown",
  "email": "alice@xyz.com",
  "skills": ["C++", "DSA", "Flask"]
}
```
---
## 🗄️ Database Schema

Table: resumes

Column Name	Type	Description
id	SERIAL PRIMARY KEY	Unique resume ID
name	VARCHAR(255)	Candidate name
email	VARCHAR(255)	Candidate email
phone	VARCHAR(20)	Contact number
skills	TEXT[]	List of skills
education	TEXT	Education details
experience	TEXT	Work experience
created_at	TIMESTAMP	Record creation time

---

## 🐳 Running with Docker
1️⃣ Build Containers
```bash
docker-compose build
```

2️⃣ Run Containers
```
docker-compose up
```

3️⃣ Stop Containers
```
docker-compose down
```

Ensure docker-compose.yml has both FastAPI and PostgreSQL services defined:
```bash
version: "3.8"
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: resume_parser
    ports:
      - "5432:5432"
```

---

## 🔮 Future Enhancements

🤖 AI Scoring Engine — Use Gemini API to evaluate resumes based on role requirements.

🧠 Job-Resume Matching — Intelligent candidate ranking.

📊 Dashboard UI — Interactive visualization of parsed data.

📈 Admin Panel — Resume management & analytics.

☁️ Cloud Deployment — Host on Render or AWS ECS.



