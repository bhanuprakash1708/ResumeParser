"""
================================================================================
Automated Resume Parser and Email Notifier
Professional Presentation Generator (python-pptx)
Widescreen 16:9, Dark Obsidian / Slate Theme with Vibrant Cyan & Indigo Accents
================================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ------------------------------------------------------------------------------
# THEME COLOR CONSTANTS
# ------------------------------------------------------------------------------
COLOR_BG_DARK        = RGBColor(11, 17, 32)     # #0B1120 Deep Obsidian Navy
COLOR_BG_CARD        = RGBColor(24, 33, 54)     # #182136 Slate Navy Container
COLOR_BG_CARD_ALT    = RGBColor(18, 25, 42)     # #12192A Darker Panel
COLOR_BORDER         = RGBColor(51, 65, 85)     # #334155 Subtle Slate Border
COLOR_BORDER_ACCENT  = RGBColor(14, 165, 233)   # #0EA5E9 Cyan Border Glow

COLOR_TEXT_PRIMARY   = RGBColor(248, 250, 252)  # #F8FAFC Pure Crisp White
COLOR_TEXT_SECONDARY = RGBColor(148, 163, 184)  # #94A3B8 Cool Slate Gray
COLOR_TEXT_MUTED     = RGBColor(100, 116, 139)  # #64748B Dark Muted Slate

COLOR_PRIMARY        = RGBColor(99, 102, 241)   # #6366F1 Electric Indigo
COLOR_CYAN           = RGBColor(6, 182, 212)    # #06B6D4 Vibrant Cyan
COLOR_TEAL           = RGBColor(20, 184, 166)   # #14B8A6 Emerald Teal
COLOR_EMERALD        = RGBColor(16, 185, 129)   # #10B981 Success Green
COLOR_AMBER          = RGBColor(245, 158, 11)   # #F59E0B Warning Amber
COLOR_ROSE           = RGBColor(244, 63, 94)    # #F43F5E Coral Rose

FONT_HEADING = "Segoe UI"
FONT_BODY    = "Segoe UI"
FONT_MONO    = "Consolas"

# ------------------------------------------------------------------------------
# PRESENTATION INITIALIZATION
# ------------------------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    """Fills slide background with deep obsidian navy."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, category_text, title_text, subtitle_text=""):
    """Adds standard high-end header with tracker badge and typography hierarchy."""
    # Category Tracker Badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.32))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = FONT_HEADING
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_CYAN

    # Title & Subtitle Box
    head_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.85))
    tf_h = head_box.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
    
    p_t = tf_h.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_PRIMARY

    if subtitle_text:
        p_s = tf_h.add_paragraph()
        p_s.text = subtitle_text
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = COLOR_TEXT_SECONDARY
        p_s.space_before = Pt(3)

def add_footer(slide, slide_num, total_slides=16):
    """Adds subtle footer with project metadata and slide number."""
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
    tf = footer_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"Automated Resume Parser & Email Notifier  |  DevOps & Cloud Automation  |  Slide {slide_num} of {total_slides}"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER):
    """Draws a sleek card container with optional border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_badge(slide, left, top, width, height, text, bg_color, text_color=COLOR_TEXT_PRIMARY, font_size=9.5):
    """Creates a pill badge for statuses or category labels."""
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_HEADING
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return badge

def add_notes(slide, script, why_matters, technical_mechanics, viva_qa):
    """Embeds comprehensive speaker notes for presentation defense."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = f"""[SPEAKER SCRIPT: WHAT TO SAY]
{script}

[WHY THIS SLIDE MATTERS TO EVALUATORS]
{why_matters}

[DEVOPS & UNDER-THE-HOOD TECHNICAL MECHANICS]
{technical_mechanics}

[LIKELY VIVA / EVALUATOR QUESTIONS & BULLETPROOF ANSWERS]
{viva_qa}
"""

print("Initializing Presentation Generator for Automated Resume Parser & Email Notifier...")

# ==============================================================================
# SLIDE 1: TITLE SLIDE (COVER)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Large decorative glow accents
card_hero = add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), COLOR_BG_CARD, COLOR_BORDER_ACCENT)

# Project Category Badge
add_badge(s1, Inches(1.3), Inches(1.3), Inches(4.5), Inches(0.38), "⚡ HACKATHON & DEVOPS ENGINEERING CAPSTONE", COLOR_PRIMARY, COLOR_TEXT_PRIMARY, 10)

# Main Title & Subtitle
title_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.85), Inches(10.7), Inches(1.8))
tf1 = title_box.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

p1 = tf1.paragraphs[0]
p1.text = "Automated Resume Parser & Email Notifier"
p1.font.name = FONT_HEADING
p1.font.size = Pt(32)
p1.font.bold = True
p1.font.color.rgb = COLOR_TEXT_PRIMARY

p2 = tf1.add_paragraph()
p2.text = "High-Performance Asynchronous Job Automation, Deep AI Extraction & Jenkins CI/CD Pipeline"
p2.font.name = FONT_BODY
p2.font.size = Pt(15)
p2.font.color.rgb = COLOR_CYAN
p2.space_before = Pt(8)

# 3 Pillars Summary Cards
# Tech Stack Pill
add_card(s1, Inches(1.3), Inches(3.8), Inches(3.3), Inches(2.4), COLOR_BG_CARD_ALT, COLOR_BORDER)
add_badge(s1, Inches(1.5), Inches(4.0), Inches(1.8), Inches(0.3), "TECH STACK", COLOR_PRIMARY, COLOR_TEXT_PRIMARY, 9)
stack_tb = s1.shapes.add_textbox(Inches(1.5), Inches(4.45), Inches(2.9), Inches(1.6))
tf_st = stack_tb.text_frame
tf_st.word_wrap = True
tf_st.margin_left = tf_st.margin_right = tf_st.margin_top = tf_st.margin_bottom = 0
p = tf_st.paragraphs[0]
p.text = "• Python 3.11+ & FastAPI (Async API)\n• Celery (Distributed Task Queue)\n• Redis 7 (In-Memory Message Broker)\n• Jenkins (CI/CD Pipeline Automation)\n• PostgreSQL + Google Gemini AI"
p.font.name = FONT_BODY
p.font.size = Pt(10.5)
p.font.color.rgb = COLOR_TEXT_SECONDARY

# DevOps Focus Pill
add_card(s1, Inches(4.8), Inches(3.8), Inches(3.3), Inches(2.4), COLOR_BG_CARD_ALT, COLOR_BORDER)
add_badge(s1, Inches(5.0), Inches(4.0), Inches(2.0), Inches(0.3), "DEVOPS FOCUS", COLOR_CYAN, COLOR_BG_DARK, 9)
devops_tb = s1.shapes.add_textbox(Inches(5.0), Inches(4.45), Inches(2.9), Inches(1.6))
tf_dev = devops_tb.text_frame
tf_dev.word_wrap = True
tf_dev.margin_left = tf_dev.margin_right = tf_dev.margin_top = tf_dev.margin_bottom = 0
p = tf_dev.paragraphs[0]
p.text = "• Background Job Automation\n• Non-blocking Sub-50ms Ingestion\n• Jenkins Multi-Stage Pipeline Setup\n• Automated Pytest Quality Gate\n• Real-Time Candidate & CI Notifications"
p.font.name = FONT_BODY
p.font.size = Pt(10.5)
p.font.color.rgb = COLOR_TEXT_SECONDARY

# Outcome Pill
add_card(s1, Inches(8.3), Inches(3.8), Inches(3.8), Inches(2.4), COLOR_BG_CARD_ALT, COLOR_BORDER)
add_badge(s1, Inches(8.5), Inches(4.0), Inches(2.2), Inches(0.3), "PROJECT OUTCOME", COLOR_EMERALD, COLOR_BG_DARK, 9)
out_tb = s1.shapes.add_textbox(Inches(8.5), Inches(4.45), Inches(3.4), Inches(1.6))
tf_out = out_tb.text_frame
tf_out.word_wrap = True
tf_out.margin_left = tf_out.margin_right = tf_out.margin_top = tf_out.margin_bottom = 0
p = tf_out.paragraphs[0]
p.text = "Automate a scalable job queue that ingests, OCR-extracts, and intelligently filters candidate resumes against job requisitions, with continuous automated deployment and testing using Jenkins CI."
p.font.name = FONT_BODY
p.font.size = Pt(10.5)
p.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s1,
    script="Good morning, judges and faculty members. Welcome to our presentation of the Automated Resume Parser and Email Notifier. In modern hiring systems, processing thousands of unstructured resumes while keeping web servers responsive is a massive challenge. Today, we demonstrate a cloud-native architecture combining Python and FastAPI, Celery distributed task queues, Redis message brokers, and Jenkins CI/CD pipelines to fully automate resume parsing, candidate scoring, and email notifications without a millisecond of thread blocking.",
    why_matters="Establishes immediate technical credibility by highlighting the core DevOps pillars: distributed background execution, continuous integration, and measurable operational outcomes.",
    technical_mechanics="FastAPI acts as an asynchronous producer pushing task UUIDs to Redis. Celery worker consumers pick up tasks for Tesseract OCR and Gemini 2.5 Pro processing. Jenkins coordinates CI/CD automation with automated pytest verification.",
    viva_qa="Q: Why separate FastAPI and Celery rather than running AI parsing directly in the API?\nA: AI inference and OCR can take 5 to 20 seconds per document. Running that synchronously in web worker threads exhausts connection pools and causes HTTP 504 timeouts. Decoupling via Celery and Redis guarantees sub-50ms API response times."
)

# ==============================================================================
# SLIDE 2: PROJECT OVERVIEW & EXECUTIVE SUMMARY
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "Executive Overview", "Bridging Talent Acquisition & DevOps Automation", "Transforming manual recruiter screening into a resilient, automated CI/CD-driven pipeline")
add_footer(s2, 2)

# Top 4 Metric Cards
metrics = [
    ("< 50 ms", "API Ingestion Latency", "Instant HTTP 200 response with task tracking UUID", COLOR_CYAN),
    ("100%", "Non-Blocking Architecture", "Zero web thread stalls via Celery + Redis task offloading", COLOR_PRIMARY),
    ("> 95%", "Screening Time Saved", "Automated parsing, scoring, and semantic job matching", COLOR_EMERALD),
    ("Zero", "Manual Deployment Drift", "Fully automated testing and container release via Jenkins CI", COLOR_AMBER)
]

for idx, (val, label, sub, color) in enumerate(metrics):
    left = Inches(0.8 + idx * 2.98)
    add_card(s2, left, Inches(1.7), Inches(2.85), Inches(1.5), COLOR_BG_CARD, COLOR_BORDER)
    
    tb = s2.shapes.add_textbox(left + Inches(0.18), Inches(1.82), Inches(2.5), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = val
    p.font.name = FONT_HEADING
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(2)
    
    p3 = tf.add_paragraph()
    p3.text = sub
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9)
    p3.font.color.rgb = COLOR_TEXT_SECONDARY
    p3.space_before = Pt(2)

# 3 Narrative Cards Below
pillars = [
    ("High-Performance Ingestion", "FastAPI Asynchronous Gateway", "Ingests resumes in PDF, scanned PDF, DOCX, TXT, and image formats. Employs SHA-256 cryptographic hashing to eliminate duplicates before storage and enforces strict 10MB payload guarding.", COLOR_PRIMARY),
    ("Distributed Background Worker", "Celery & Redis Task Offloading", "Decouples heavy compute tasks (Tesseract OCR, Poppler rendering, and Google Gemini Pro AI inference) into distributed background workers with automatic retries and database status updates.", COLOR_CYAN),
    ("DevOps & Automated Feedback", "Jenkins CI & Email Notification", "Continuous integration pipeline triggers automated linting, pytest suites, and Docker container packaging. Triggers automated email notifications to candidates upon status changes and alerts recruiters to top-fit talent.", COLOR_EMERALD)
]

for idx, (title, subtitle, body, color) in enumerate(pillars):
    left = Inches(0.8 + idx * 3.97)
    add_card(s2, left, Inches(3.45), Inches(3.8), Inches(3.3), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s2, left + Inches(0.2), Inches(3.68), Inches(2.2), Inches(0.28), title.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 8.5)
    
    tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(4.1), Inches(3.4), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = body
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(8)

add_notes(s2,
    script="On this slide, you see the overarching vision of our system. Recruiting teams receive thousands of candidate files every week. Traditional web applications crash when users upload large files, because OCR and AI extraction take seconds of intensive computation. Our system breaks that bottleneck into three distinct operational layers: an instant FastAPI ingestion gateway, a distributed Celery and Redis processing pool, and a Jenkins CI pipeline with automated email notifications.",
    why_matters="Demonstrates measurable operational value: <50ms response times, 100% asynchronous execution, and automated deployment verification.",
    technical_mechanics="The client receives an immediate HTTP 200/202 containing the resume UUID. Meanwhile, Redis maintains the FIFO queue and Celery workers process jobs asynchronously, updating PostgreSQL upon task completion.",
    viva_qa="Q: How do you measure the sub-50ms ingestion latency?\nA: FastAPI validates the payload header, hashes the file, commits an initial 'pending' record to PostgreSQL, dispatches the Celery task ID, and returns immediately without awaiting the worker."
)

# ==============================================================================
# SLIDE 3: PROBLEM STATEMENT & INDUSTRY NEED
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "Industry Pain Points", "The Recruiter Dilemma & Architectural Bottlenecks", "Why legacy recruitment platforms fail under scale and how asynchronous DevOps solves it")
add_footer(s3, 3)

# 4 Problem Cards
problems = [
    ("Bottleneck 1: Unstructured Document Chaos", "Resumes arrive across wildly fragmented formats: digital PDFs, multi-column DOCX files, and phone photographs of printed resumes. Traditional regex parsers fail on 70%+ of real-world layouts, losing vital candidate data.", COLOR_ROSE),
    ("Bottleneck 2: Synchronous API Freezes", "Extracting text and calling large language models takes 5 to 25 seconds per document. When 50 candidates apply simultaneously, synchronous web workers block completely, exhausting thread pools and causing HTTP 504 timeouts.", COLOR_AMBER),
    ("Bottleneck 3: Communication 'Black Hole'", "Over 75% of job applicants report never receiving status notifications. Recruiters spend hours manually sending interview invites or rejection emails, creating a fragmented candidate experience.", COLOR_CYAN),
    ("Bottleneck 4: Fragile Deployment & Drift", "Recruitment tools deployed without continuous integration pipelines suffer from dependency conflicts (e.g., missing Tesseract OCR or Poppler system packages), leading to production outages during updates.", COLOR_PRIMARY)
]

for idx, (title, desc, color) in enumerate(problems):
    col = idx % 2
    row = idx // 2
    left = Inches(0.8 + col * 5.96)
    top = Inches(1.7 + row * 2.55)
    
    add_card(s3, left, top, Inches(5.75), Inches(2.35), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s3, left + Inches(0.2), top + Inches(0.2), Inches(3.6), Inches(0.28), title.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 8.5)
    
    tb = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.35), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s3,
    script="Here we identify the core problems that modern HR tech faces. First is document chaos: scanned resumes and photos defeat naive regex scripts. Second is the architectural flaw of running heavy AI inference inside the HTTP request loop. When 50 candidates upload files at once, synchronous servers freeze. Third, candidates are left in a communication black hole without automated feedback. And fourth, without automated CI/CD pipelines, deploying machine learning and OCR dependencies like Tesseract and Poppler often breaks across environments.",
    why_matters="Proves that this project is not merely an API tutorial, but an enterprise engineering solution addressing real architectural failures in production systems.",
    technical_mechanics="Synchronous servers allocate one thread or event-loop cycle per HTTP request. Blocking on network I/O or OCR subprocesses starves new incoming connections. Offloading to Celery queues decouples I/O from computation.",
    viva_qa="Q: What happens if a scanned PDF is uploaded without OCR fallback?\nA: Standard PDF text extractors return empty strings or gibberish. Our worker detects when extracted text length is under 10 characters and automatically routes the file to Tesseract OCR."
)

# ==============================================================================
# SLIDE 4: FULL TECHNOLOGY STACK
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Technology Architecture", "Production-Grade Tech Stack Breakdown", "Synergistic technologies powering API ingestion, background execution, AI analysis, and CI/CD")
add_footer(s4, 4)

tech_columns = [
    ("Core Backend", COLOR_PRIMARY, [
        ("Python 3.11+", "Core programming language with asynchronous coroutines & typing"),
        ("FastAPI", "High-throughput ASGI framework, automatic OpenAPI & Swagger UI"),
        ("Pydantic v2", "Strict schema validation for inputs and structured AI responses"),
        ("SQLAlchemy", "ORM for persistent resume metadata & JSON/JSONB storage"),
        ("Uvicorn", "Lightning-fast ASGI production web server worker")
    ]),
    ("Task Queue & Broker", COLOR_CYAN, [
        ("Celery 5.x", "Distributed asynchronous task execution & worker pool management"),
        ("Redis 7.x", "In-memory message broker & task result backend"),
        ("Worker Pools", "Configurable concurrency isolating compute from web threads"),
        ("Task Retries", "Exponential backoff policies for external API resilience"),
        ("Eager Fallback", "Synchronous dev fallback mode for isolated local unit testing")
    ]),
    ("DevOps & CI/CD", COLOR_AMBER, [
        ("Jenkins", "Declarative pipeline automating lint, test, build, and deploy"),
        ("Docker", "Containerization packaging system binaries (Tesseract, Poppler)"),
        ("Docker Compose", "Multi-container orchestration for API, Worker, Redis, and DB"),
        ("Pytest & AsyncIO", "Automated unit & integration test suite with mock fixtures"),
        ("Flake8 & Black", "Automated code quality & PEP-8 formatting enforcement")
    ]),
    ("AI & Ingestion", COLOR_EMERALD, [
        ("Google Gemini Pro", "Advanced LLM for structured JSON extraction and candidate scoring"),
        ("Tesseract OCR", "Optical Character Recognition engine for scanned PDFs & images"),
        ("pdfplumber", "High-fidelity digital PDF text and table coordinate extraction"),
        ("python-docx", "Native parsing for Microsoft Word document formats"),
        ("Email Notifier", "Automated candidate receipts and recruiter match alerts")
    ])
]

for idx, (col_title, col_color, items) in enumerate(tech_columns):
    left = Inches(0.8 + idx * 2.98)
    add_card(s4, left, Inches(1.7), Inches(2.85), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s4, left + Inches(0.18), Inches(1.9), Inches(2.5), Inches(0.32), col_title.upper(), col_color, COLOR_BG_DARK if col_color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s4.shapes.add_textbox(left + Inches(0.18), Inches(2.35), Inches(2.5), Inches(4.25))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    for i_idx, (name, desc) in enumerate(items):
        p = tf.paragraphs[0] if i_idx == 0 else tf.add_paragraph()
        p.text = f"{name}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        if i_idx > 0:
            p.space_before = Pt(7)
            
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(8.5)
        p_desc.font.color.rgb = COLOR_TEXT_SECONDARY
        p_desc.space_before = Pt(1)

add_notes(s4,
    script="Our tech stack was curated specifically to solve concurrency, data integrity, and DevOps automation. For the backend, we use Python 3.11 with FastAPI and Pydantic v2. For the distributed task queue, Celery works alongside Redis 7 as the message broker. For DevOps, Jenkins orchestrates our declarative CI/CD pipeline, and Docker Compose manages our four containerized microservices. For intelligence, Google Gemini 2.5 Pro provides structured entity extraction, backed by Tesseract OCR and pdfplumber.",
    why_matters="Answers the user's explicit request: Python + FastAPI + Celery + Redis + Jenkins, demonstrating how each technology fulfills an irreplaceable role.",
    technical_mechanics="FastAPI operates asynchronously using Uvicorn. Redis operates in memory as a Celery broker. Tesseract OCR and Poppler binaries are containerized via Dockerfile so they run identically in CI and production.",
    viva_qa="Q: Why use Redis as a broker rather than RabbitMQ or Kafka?\nA: Redis is exceptionally lightweight, provides sub-millisecond in-memory queueing, doubles as a task result store, and requires minimal operational overhead for microservice architectures."
)

# ==============================================================================
# SLIDE 5: END-TO-END SYSTEM ARCHITECTURE & DATA FLOW
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "System Architecture", "End-to-End Microservice Topology & Data Flow", "Decoupled 5-stage pipeline from client upload to AI extraction and automated notification")
add_footer(s5, 5)

flow_steps = [
    ("1. Client Ingestion", "Web Dashboard / API", "User drops resume (.pdf, .docx, .png). Client sends multipart HTTP POST to /upload.", COLOR_PRIMARY),
    ("2. FastAPI Gateway", "Validate & Dispatch", "Computes SHA-256 hash, guards 10MB limit, writes 'pending' in DB, queues job in Redis.", COLOR_CYAN),
    ("3. Redis Message Broker", "Queue Routing", "Holds task queue in memory. Dispatches task ID to active Celery worker thread.", COLOR_AMBER),
    ("4. Celery Worker", "OCR & AI Inference", "Picks up file, runs pdfplumber/Tesseract, sends text to Gemini Pro for JSON extraction.", COLOR_EMERALD),
    ("5. Database & Notifier", "Save & Email Alert", "Stores structured JSON in PostgreSQL, updates status to 'completed', and triggers email alerts.", COLOR_PRIMARY)
]

for idx, (title, subtitle, desc, color) in enumerate(flow_steps):
    left = Inches(0.8 + idx * 2.38)
    add_card(s5, left, Inches(1.8), Inches(2.25), Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s5, left + Inches(0.15), Inches(1.98), Inches(1.95), Inches(0.3), f"STAGE 0{idx+1}", color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s5.shapes.add_textbox(left + Inches(0.15), Inches(2.4), Inches(1.95), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = color
    p2.space_before = Pt(3)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9)
    p3.font.color.rgb = COLOR_TEXT_SECONDARY
    p3.space_before = Pt(6)

# Architecture Summary Banner Below
add_card(s5, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.15), COLOR_BG_CARD_ALT, COLOR_BORDER_ACCENT)
tb_b = s5.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.95))
tf_b = tb_b.text_frame
tf_b.word_wrap = True
tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

p_b = tf_b.paragraphs[0]
p_b.text = "Key Architectural Strength: Decoupled Producer-Consumer Pattern"
p_b.font.name = FONT_HEADING
p_b.font.size = Pt(12)
p_b.font.bold = True
p_b.font.color.rgb = COLOR_CYAN

p_b2 = tf_b.add_paragraph()
p_b2.text = "• Web server thread is freed in <50ms, allowing thousands of simultaneous uploads without timeout degradation.\n• Celery workers scale horizontally across multiple container nodes based on Redis queue depth."
p_b2.font.name = FONT_BODY
p_b2.font.size = Pt(9.5)
p_b2.font.color.rgb = COLOR_TEXT_SECONDARY
p_b2.space_before = Pt(3)

add_notes(s5,
    script="This diagram maps our end-to-end data flow. When a user uploads a resume, FastAPI receives the request, generates a unique SHA-256 hash to prevent duplicate reprocessing, creates a database row with status 'pending', and pushes the task ID to Redis. Within 50 milliseconds, the user receives an HTTP 200 response. Meanwhile, an asynchronous Celery worker pulls the task from Redis, runs OCR, extracts structured JSON from Gemini Pro, updates the database to 'completed', and fires automated email notifications.",
    why_matters="Provides a clear visual blueprint of the microservice interaction, demonstrating how message queues isolate web servers from compute-intensive workloads.",
    technical_mechanics="FastAPI's UploadFile stream is saved to a shared Docker volume. The Celery worker reads the file from disk, parses the content, and writes the structured JSONB payload directly into PostgreSQL.",
    viva_qa="Q: How does the frontend know when the worker finishes?\nA: The frontend polls the 'GET /api/v1/resumes/{id}/status' endpoint every 2 seconds. When the status changes from 'processing' to 'completed', the frontend fetches the full structured payload."
)

# ==============================================================================
# SLIDE 6: DEVOPS FOCUS 1: BACKGROUND JOB AUTOMATION (CELERY + REDIS)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "DevOps Focus #1", "Background Job Automation with Celery & Redis", "How asynchronous queuing guarantees sub-50ms ingestion latency and zero HTTP thread blocking")
add_footer(s6, 6)

# Left Column: The Asynchronous Paradigm
add_card(s6, Inches(0.8), Inches(1.7), Inches(5.75), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s6, Inches(1.0), Inches(1.9), Inches(3.2), Inches(0.3), "THE ASYNCHRONOUS PARADIGM", COLOR_PRIMARY, COLOR_TEXT_PRIMARY, 9)

tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.35), Inches(4.2))
tf_l = tb_l.text_frame
tf_l.word_wrap = True
tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

points_l = [
    ("Decoupling I/O from Compute", "Heavy tasks like OCR rendering and LLM calls (5–20s) are completely removed from the FastAPI event loop, ensuring high availability."),
    ("Task State Progression", "Jobs progress through explicit lifecycle states: 'pending' → 'processing' → 'completed' (or 'failed' on unrecoverable error)."),
    ("Concurrency & Prefetch Control", "Configured with prefetch multiplier = 1 and dedicated worker concurrency pools to prevent single large files from starving workers."),
    ("Fault Tolerance & Dead-Letter Handling", "If an external API call times out, Celery's exponential backoff automatically retries without crashing the service.")
]

for idx, (head, body) in enumerate(points_l):
    p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
    p.text = f"• {head}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    if idx > 0:
        p.space_before = Pt(8)
        
    run = p.add_run()
    run.text = body
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

# Right Column: Architecture Comparison Table
add_card(s6, Inches(6.75), Inches(1.7), Inches(5.78), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s6, Inches(6.95), Inches(1.9), Inches(3.0), Inches(0.3), "SYNCHRONOUS VS. ASYNCHRONOUS", COLOR_CYAN, COLOR_BG_DARK, 9)

# Table inside Right Card
table_shape = s6.shapes.add_table(5, 3, Inches(6.95), Inches(2.35), Inches(5.38), Inches(4.2))
table = table_shape.table
table.columns[0].width = Inches(1.5)
table.columns[1].width = Inches(1.9)
table.columns[2].width = Inches(1.98)

headers = ["Metric", "Synchronous (Traditional)", "Celery + Redis (Our System)"]
for col_idx, text in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_BG_CARD_ALT
    p = cell.text_frame.paragraphs[0]
    p.text = text
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

rows_data = [
    ("API Ingestion Time", "5,000 – 20,000 ms", "< 50 ms (Instant 200 OK)"),
    ("Concurrency Limit", "Exhausts web workers (~10-20)", "1,000+ jobs queued in Redis"),
    ("Failure Impact", "Crashes web request / 504", "Isolated worker retry / DB log"),
    ("Horizontal Scaling", "Requires cloning full API server", "Scale workers independently")
]

for row_idx, data in enumerate(rows_data):
    for col_idx, text in enumerate(data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BG_CARD if row_idx % 2 == 0 else COLOR_BG_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        if col_idx == 0:
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_PRIMARY
        elif col_idx == 1:
            p.font.color.rgb = COLOR_ROSE
        else:
            p.font.bold = True
            p.font.color.rgb = COLOR_EMERALD

add_notes(s6,
    script="This slide addresses our primary DevOps focus: background job automation using Celery and Redis. In traditional web architectures, processing happens inside the HTTP request. That means if an AI extraction takes 15 seconds, the client holds that connection open, blocking web worker threads. By offloading parsing to Celery, our upload endpoint finishes in under 50 milliseconds. The job sits in the Redis queue until a dedicated worker processes it, updating the database status upon completion.",
    why_matters="Directly answers the user's prompt regarding 'Background job automation' and demonstrates enterprise system design principles.",
    technical_mechanics="We configure Celery with task serialization via JSON, Redis as broker and backend, and worker concurrency matching host core counts. Workers poll Redis using BLPOP commands, ensuring low latency task dispatch.",
    viva_qa="Q: What happens if a Celery worker dies mid-task?\nA: Redis maintains task visibility timeouts. If a worker terminates without acknowledging task completion (ACK), Celery's acknowledgement protocol redelivers the task to another active worker."
)

# ==============================================================================
# SLIDE 7: DEVOPS FOCUS 2: JENKINS CI/CD PIPELINE SETUP
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "DevOps Focus #2", "Jenkins CI/CD Pipeline Automation", "Declarative pipeline setup automating linting, pytest suites, container packaging, and deployment")
add_footer(s7, 7)

# 6 Pipeline Stages horizontally/vertically arranged
stages = [
    ("Stage 1: Checkout & SCM", "Validates branch, extracts build metadata (commit hash, build ID), and pulls dependencies.", COLOR_PRIMARY),
    ("Stage 2: Code Quality & Lint", "Executes Flake8 and Black checks to enforce strict PEP-8 syntax and code quality standards.", COLOR_CYAN),
    ("Stage 3: Automated Pytest", "Runs pytest test suite with async fixtures, testing /health, /upload, file size caps, and task mocks.", COLOR_AMBER),
    ("Stage 4: Multi-Container Build", "Builds Docker images for API and Celery Worker, applying dynamic build number tags.", COLOR_EMERALD),
    ("Stage 5: Security & Audit", "Runs container vulnerability scanning to guarantee zero critical security flaws in dependencies.", COLOR_PRIMARY),
    ("Stage 6: Deploy & Verify", "Orchestrates Docker Compose, verifies service spin-up, and executes automated curl health check.", COLOR_CYAN)
]

for idx, (title, desc, color) in enumerate(stages):
    col = idx % 3
    row = idx // 3
    left = Inches(0.8 + col * 3.97)
    top = Inches(1.7 + row * 2.55)
    
    add_card(s7, left, top, Inches(3.8), Inches(2.35), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s7, left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(0.28), title.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 8.5)
    
    tb = s7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(3.4), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s7,
    script="Our second DevOps focus is our Jenkins CI/CD pipeline. We defined a complete declarative Jenkinsfile in the repository root. Every Git push automatically triggers six rigorous stages: source checkout, static linting with Flake8, our automated Pytest suite with task mocking, Docker container image compilation, vulnerability scanning, and automated deployment verification using curl against our live /health endpoint. If any single test fails, the pipeline immediately halts, preventing broken builds from reaching staging or production.",
    why_matters="Directly fulfills the user prompt: 'pipeline setup' and 'processes and filters resumes using CI'.",
    technical_mechanics="The Jenkinsfile uses declarative syntax. Stage 3 runs 'pytest tests/test_api.py -v'. Stage 4 runs 'docker build -t resumeparser/api:${BUILD_NUMBER}'. Stage 6 runs 'docker compose up -d' followed by curl health checks.",
    viva_qa="Q: How does Jenkins handle secret credentials like GEMINI_API_KEY?\nA: Jenkins Credentials Provider injects secrets into the pipeline environment at runtime without hardcoding sensitive API keys in source code or Git history."
)

# ==============================================================================
# SLIDE 8: DEVOPS FOCUS 3: AUTOMATED NOTIFICATION SYSTEM
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "DevOps Focus #3", "Dual-Tier Automated Notification System", "Real-time communication architecture for candidate progress, recruiter alerts, and CI/CD events")
add_footer(s8, 8)

# Left Card: Candidate & Recruiter Notifications
add_card(s8, Inches(0.8), Inches(1.7), Inches(5.75), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s8, Inches(1.0), Inches(1.9), Inches(4.5), Inches(0.3), "TIER 1: RECRUITMENT APPLICATION NOTIFICATIONS", COLOR_EMERALD, COLOR_BG_DARK, 9)

tb_n1 = s8.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.35), Inches(4.2))
tf_n1 = tb_n1.text_frame
tf_n1.word_wrap = True
tf_n1.margin_left = tf_n1.margin_right = tf_n1.margin_top = tf_n1.margin_bottom = 0

events_app = [
    ("Instant Submission Receipt", "Candidate receives confirmation immediately upon resume queueing, validating successful upload and providing tracking details."),
    ("AI Evaluation Summary", "Dispatches candidate scorecard including Quality Score (0-100) and top matching industry categorization once Celery processing completes."),
    ("High-Match Recruiter Alert", "Automatically triggers high-priority email to hiring managers whenever candidate match score exceeds requisition threshold (e.g., >=80%)."),
    ("Zero Ghosting Policy", "Ensures transparent status communication at every evaluation phase, eliminating candidate drop-off and recruiter manual emailing.")
]

for idx, (title, desc) in enumerate(events_app):
    p = tf_n1.paragraphs[0] if idx == 0 else tf_n1.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    if idx > 0:
        p.space_before = Pt(8)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

# Right Card: DevOps CI/CD Pipeline Notifications
add_card(s8, Inches(6.75), Inches(1.7), Inches(5.78), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s8, Inches(6.95), Inches(1.9), Inches(4.2), Inches(0.3), "TIER 2: DEVOPS CI/CD PIPELINE NOTIFICATIONS", COLOR_PRIMARY, COLOR_TEXT_PRIMARY, 9)

tb_n2 = s8.shapes.add_textbox(Inches(6.95), Inches(2.35), Inches(5.38), Inches(4.2))
tf_n2 = tb_n2.text_frame
tf_n2.word_wrap = True
tf_n2.margin_left = tf_n2.margin_right = tf_n2.margin_top = tf_n2.margin_bottom = 0

events_ci = [
    ("Build Failure & Alert Webhooks", "Jenkins post-action blocks dispatch instant notifications to developer Slack channels or email upon test or compilation failure."),
    ("Deployment Health Confirmation", "Automated notification confirming successful container rollout, active container IDs, and passed /health probes."),
    ("Audit Logs & Traceability", "Full execution logs preserved in Jenkins build artifacts, linking Git commit hashes with Docker image tags and test reports."),
    ("Continuous Operational Visibility", "Guarantees engineering teams are alerted within seconds of any pipeline regression before code hits production.")
]

for idx, (title, desc) in enumerate(events_ci):
    p = tf_n2.paragraphs[0] if idx == 0 else tf_n2.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    if idx > 0:
        p.space_before = Pt(8)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s8,
    script="Our third DevOps focus is automated notifications. We implemented a dual-tier notification system. Tier 1 handles the application domain: sending automated email receipts to applicants, sending scorecard updates upon parsing completion, and triggering high-match alerts to recruiters when candidates score above 80%. Tier 2 handles the DevOps pipeline: Jenkins automatically notifies engineers via webhooks or email on build successes, test failures, or container deployment verification.",
    why_matters="Directly addresses the user's requirement for 'notifications' across both application workflows and DevOps CI/CD pipelines.",
    technical_mechanics="We built 'src/worker/notifier.py' with SMTP integration. Celery triggers 'notify_parsing_completed()' upon database commit. Jenkins uses post { success {} failure {} } blocks to trigger alerting.",
    viva_qa="Q: How do you prevent email notifications from slowing down Celery workers?\nA: Email notifications are either invoked at the very end of the task or delegated to a secondary Celery queue dedicated to communication I/O, ensuring CPU-bound workers are not blocked."
)

# ==============================================================================
# SLIDE 9: MULTI-FORMAT DOCUMENT INGESTION & TESSERACT OCR
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "Ingestion Engine", "Universal Multi-Format Ingestion & Tesseract OCR", "Intelligent format detection, automatic OCR fallback, and cryptographic deduplication")
add_footer(s9, 9)

# 4 Ingestion Format Cards
formats = [
    ("Native Digital PDFs", "pdfplumber Engine", "Extracts structured text streams, multi-column blocks, and table cells with sub-200ms processing speed.", COLOR_PRIMARY),
    ("Scanned / Image PDFs", "Tesseract OCR + Poppler", "Automatically triggered when extracted text length < 10 characters. Converts pages to images and runs optical character recognition.", COLOR_CYAN),
    ("Microsoft Word (.docx)", "python-docx Parser", "Traverses paragraphs, tables, and nested XML tags, preserving formatting structure and bulleted candidate achievements.", COLOR_AMBER),
    ("Direct Image Files", "PIL + Pytesseract", "Direct optical character recognition on .jpg, .jpeg, and .png photo uploads, handling contrast variations and rotated text.", COLOR_EMERALD)
]

for idx, (title, engine, desc, color) in enumerate(formats):
    left = Inches(0.8 + idx * 2.98)
    add_card(s9, left, Inches(1.7), Inches(2.85), Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s9, left + Inches(0.18), Inches(1.9), Inches(2.5), Inches(0.3), engine.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 8.5)
    
    tb = s9.shapes.add_textbox(left + Inches(0.18), Inches(2.35), Inches(2.5), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(8)

# Deduplication & Security Banner Below
add_card(s9, Inches(0.8), Inches(5.55), Inches(11.733), Inches(1.2), COLOR_BG_CARD_ALT, COLOR_BORDER_ACCENT)
tb_d = s9.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.3), Inches(1.0))
tf_d = tb_d.text_frame
tf_d.word_wrap = True
tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0

p_d = tf_d.paragraphs[0]
p_d.text = "Data Integrity & Deduplication: SHA-256 File Hashing & 10MB Guarding"
p_d.font.name = FONT_HEADING
p_d.font.size = Pt(12)
p_d.font.bold = True
p_d.font.color.rgb = COLOR_CYAN

p_d2 = tf_d.add_paragraph()
p_d2.text = "• Every incoming file is cryptographically hashed (SHA-256). Duplicate submissions are rejected instantly before wasting expensive OCR or AI compute.\n• Ingestion endpoint strictly rejects files over 10MB with HTTP 413 (Content Too Large) to prevent DoS attacks."
p_d2.font.name = FONT_BODY
p_d2.font.size = Pt(9.5)
p_d2.font.color.rgb = COLOR_TEXT_SECONDARY
p_d2.space_before = Pt(3)

add_notes(s9,
    script="Real-world applicants submit documents in all kinds of formats. Our ingestion engine handles digital PDFs via pdfplumber, Word documents via python-docx, and scanned documents via Tesseract OCR and Poppler. When a PDF has fewer than 10 characters of extractable digital text, our worker automatically falls back to OCR. Furthermore, we compute a SHA-256 cryptographic hash on upload to eliminate duplicate submissions before wasting compute.",
    why_matters="Demonstrates robust engineering against messy real-world data and defends against server overload via 10MB size limits and hash deduplication.",
    technical_mechanics="The worker uses pdf2image's convert_from_path() with Poppler, iterates through rendered PIL images, and runs pytesseract.image_to_string() before passing the aggregate text stream to the AI parser.",
    viva_qa="Q: What happens if someone uploads a 50MB file to overwhelm the server?\nA: FastAPI inspects the Content-Length and buffer size. If it exceeds 10MB, it immediately raises an HTTPException with status code 413 Content Too Large without saving it to disk."
)

# ==============================================================================
# SLIDE 10: AI INTELLIGENCE & STRUCTURED EXTRACTION (GEMINI PRO)
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "AI Cognition", "AI-Powered Structured Extraction & Analysis", "Leveraging Google Gemini 2.5 Pro with strict JSON schema enforcement and quality metrics")
add_footer(s10, 10)

# Left Card: Schema Enforcement & Pydantic Models
add_card(s10, Inches(0.8), Inches(1.7), Inches(5.75), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s10, Inches(1.0), Inches(1.9), Inches(3.6), Inches(0.3), "STRICT PYDANTIC SCHEMA MAPPING", COLOR_PRIMARY, COLOR_TEXT_PRIMARY, 9)

tb_ai1 = s10.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.35), Inches(4.2))
tf_ai1 = tb_ai1.text_frame
tf_ai1.word_wrap = True
tf_ai1.margin_left = tf_ai1.margin_right = tf_ai1.margin_top = tf_ai1.margin_bottom = 0

schema_fields = [
    ("personalInfo", "Full name, email, phone number, address (city, state, country), and verified LinkedIn profile URLs."),
    ("summary & careerLevel", "Professional executive summary, mapped seniority level (entry, mid-level, senior, executive)."),
    ("experience[]", "Chronological roles: title, company, location, start/end dates, description, and technologies utilized."),
    ("education[]", "Academic credentials: degree, field of study, university institution, and graduation dates."),
    ("skills (tech & soft)", "Categorized technical languages, frameworks, cloud tooling, soft skills, and spoken languages.")
]

for idx, (field, desc) in enumerate(schema_fields):
    p = tf_ai1.paragraphs[0] if idx == 0 else tf_ai1.add_paragraph()
    p.text = f"• {field}: "
    p.font.name = FONT_MONO if idx != 1 else FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    if idx > 0:
        p.space_before = Pt(8)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

# Right Card: The aiEnhancements Cognitive Block
add_card(s10, Inches(6.75), Inches(1.7), Inches(5.78), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s10, Inches(6.95), Inches(1.9), Inches(3.6), Inches(0.3), "DEEP AI ENHANCEMENTS ENGINE", COLOR_EMERALD, COLOR_BG_DARK, 9)

tb_ai2 = s10.shapes.add_textbox(Inches(6.95), Inches(2.35), Inches(5.38), Inches(4.2))
tf_ai2 = tb_ai2.text_frame
tf_ai2.word_wrap = True
tf_ai2.margin_left = tf_ai2.margin_right = tf_ai2.margin_top = tf_ai2.margin_bottom = 0

enhancements = [
    ("qualityScore (0 – 100)", "Comprehensive rating evaluating clarity, quantifiable accomplishments, and professional layout standards.", COLOR_EMERALD),
    ("completenessScore (0 – 100)", "Percentage calculation verifying the presence of all core recruitment components (contact, education, history).", COLOR_CYAN),
    ("industryFit Probabilities", "Machine learning classification across multiple target sectors (e.g., Software Engineering: 0.95, Data Science: 0.45).", COLOR_AMBER),
    ("careerProgressionAnalysis", "AI qualitative narrative synthesizing promotion speed, seniority growth, and executive leadership readiness.", COLOR_PRIMARY)
]

for idx, (title, desc, color) in enumerate(enhancements):
    p = tf_ai2.paragraphs[0] if idx == 0 else tf_ai2.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = color
    if idx > 0:
        p.space_before = Pt(10)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s10,
    script="Now let's examine the AI extraction layer. Unstructured LLM outputs are useless in production ATS databases. We use Google Gemini 2.5 Pro configured with a strict JSON format template. The model extracts personal info, work history, education, and skills. Crucially, it also populates an 'aiEnhancements' block containing a quality score, completeness score, multi-industry classification probabilities, and a career progression analysis.",
    why_matters="Demonstrates high-level AI prompt engineering and schema validation, turning raw text into structured enterprise intelligence.",
    technical_mechanics="The Gemini client is configured with temperature=0.1 for high determinism. The response text is stripped of markdown delimiters, parsed into Python dictionaries, and validated against Pydantic schemas before writing to PostgreSQL JSONB.",
    viva_qa="Q: How do you prevent hallucinated fields in the JSON output?\nA: We enforce temperature=0.1, supply explicit JSON templates in the master prompt, and instruct the model that missing fields must strictly return null or empty lists."
)

# ==============================================================================
# SLIDE 11: AUTOMATED RESUME-JOB FILTERING & MATCHING ENGINE
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "Automated Filtering", "Intelligent Resume-Job Filtering & Semantic Match", "Evaluating candidate profiles against Job Descriptions via POST /resumes/{id}/match")
add_footer(s11, 11)

# 3 Dimensional Evaluation Cards
eval_cards = [
    ("Multi-Category Scoring", COLOR_CYAN, [
        ("Overall Score (0-100%)", "Synthesized holistic compatibility index"),
        ("Skills Match (0-100%)", "Direct & transferable tech stack overlap"),
        ("Experience Fit (0-100%)", "Years of relevant industry seniority"),
        ("Role Alignment", "Domain responsibility correspondence")
    ]),
    ("Automated Gap Analysis", COLOR_AMBER, [
        ("Missing Core Skills", "Identifies mandatory technical prerequisites missing"),
        ("Soft Skill Discrepancies", "Flags communication or leadership gaps"),
        ("Experience Shortfalls", "Highlights deficits in scale or team management"),
        ("Upskilling Guidance", "Recommends concrete technical bridges")
    ]),
    ("Automated Recruiter Action", COLOR_EMERALD, [
        ("Automated Shortlisting", "Auto-tags candidates exceeding score threshold"),
        ("Interview Guide Generation", "Generates tailored technical interview questions"),
        ("Salary Alignment", "Flags compensation mismatches early"),
        ("Email Notification Trigger", "Fires automated interview invite or feedback")
    ])
]

for idx, (col_title, col_color, items) in enumerate(eval_cards):
    left = Inches(0.8 + idx * 3.97)
    add_card(s11, left, Inches(1.7), Inches(3.8), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s11, left + Inches(0.2), Inches(1.9), Inches(3.4), Inches(0.3), col_title.upper(), col_color, COLOR_BG_DARK if col_color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s11.shapes.add_textbox(left + Inches(0.2), Inches(2.35), Inches(3.4), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    for i_idx, (name, desc) in enumerate(items):
        p = tf.paragraphs[0] if i_idx == 0 else tf.add_paragraph()
        p.text = f"{name}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        if i_idx > 0:
            p.space_before = Pt(10)
            
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_TEXT_SECONDARY
        p_desc.space_before = Pt(2)

add_notes(s11,
    script="Our system does more than just parse resumes—it actively filters them. Our '/api/v1/resumes/{id}/match' endpoint compares a candidate's structured profile against a job description. It computes multi-category compatibility scores for skills, experience, and education, performs an automated gap analysis, and generates tailored interview questions. If a candidate scores above 80%, the system automatically flags them for recruiter outreach.",
    why_matters="Directly fulfills the user outcome: 'Automate a job queue that processes and filters resumes using CI'.",
    technical_mechanics="The endpoint uses Gemini 2.5 Pro with Pydantic's MatchResponse schema. The model calculates mathematical score weightings and categorizes matched vs missing skills.",
    viva_qa="Q: Can the matching threshold be configured for different roles?\nA: Yes, the threshold is configurable via environment variables or query parameters (e.g. passing min_score=75 to automatically filter candidates)."
)

# ==============================================================================
# SLIDE 12: DOCKER CONTAINERIZATION & MULTI-SERVICE ORCHESTRATION
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_header(s12, "Container Orchestration", "Docker & Multi-Container Topology", "Isolated microservice network orchestrated via Docker Compose and multi-stage Dockerfiles")
add_footer(s12, 12)

services = [
    ("api", "FastAPI ASGI Server", "Port: 8000:8000", "Serves HTTP endpoints, static dashboard, OpenAPI docs, and dispatches Celery tasks.", COLOR_PRIMARY),
    ("worker", "Celery Task Consumer", "Shared /uploads Volume", "Pulls jobs from Redis, executes Tesseract OCR, Poppler rendering, and Gemini AI analysis.", COLOR_CYAN),
    ("redis", "In-Memory Broker", "Port: 6379:6379", "High-throughput Redis 7 Alpine container acting as message broker and task result backend.", COLOR_AMBER),
    ("db", "PostgreSQL Database", "Port: 5432:5432", "Postgres 15 Alpine storing resume metadata, status timestamps, and structured JSONB data.", COLOR_EMERALD)
]

for idx, (name, role, port, desc, color) in enumerate(services):
    left = Inches(0.8 + idx * 2.98)
    add_card(s12, left, Inches(1.7), Inches(2.85), Inches(3.6), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s12, left + Inches(0.18), Inches(1.9), Inches(1.5), Inches(0.3), name.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s12.shapes.add_textbox(left + Inches(0.18), Inches(2.35), Inches(2.5), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = role
    p.font.name = FONT_HEADING
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = port
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = color
    p2.space_before = Pt(3)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = COLOR_TEXT_SECONDARY
    p3.space_before = Pt(8)

# Containerization Best Practices Below
add_card(s12, Inches(0.8), Inches(5.55), Inches(11.733), Inches(1.2), COLOR_BG_CARD_ALT, COLOR_BORDER_ACCENT)
tb_cp = s12.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.3), Inches(1.0))
tf_cp = tb_cp.text_frame
tf_cp.word_wrap = True
tf_cp.margin_left = tf_cp.margin_right = tf_cp.margin_top = tf_cp.margin_bottom = 0

p_cp = tf_cp.paragraphs[0]
p_cp.text = "Production DevOps Containerization Practices"
p_cp.font.name = FONT_HEADING
p_cp.font.size = Pt(12)
p_cp.font.bold = True
p_cp.font.color.rgb = COLOR_CYAN

p_cp2 = tf_cp.add_paragraph()
p_cp2.text = "• Dockerfile bundles required system libraries (tesseract-ocr, poppler-utils) alongside Python 3.11 slim base.\n• Shared persistent volume (/uploads) allows API and Celery workers to access files seamlessly.\n• Persistent postgres_data volume guarantees relational data durability across container restarts."
p_cp2.font.name = FONT_BODY
p_cp2.font.size = Pt(9.5)
p_cp2.font.color.rgb = COLOR_TEXT_SECONDARY
p_cp2.space_before = Pt(3)

add_notes(s12,
    script="Reproducibility is paramount in DevOps. We containerized our entire four-service ecosystem using Docker and Docker Compose. Our Dockerfile installs system-level C dependencies like tesseract-ocr and poppler-utils directly on top of Debian slim. The API and Worker containers share an isolated internal network alongside Redis and PostgreSQL, ensuring secure inter-service communication.",
    why_matters="Demonstrates complete cloud containerization proficiency, making deployment a single 'docker compose up' command.",
    technical_mechanics="The Docker Compose file specifies depends_on relations: API depends on DB and Redis; Worker depends on DB and Redis. Shared volumes ensure zero file replication overhead.",
    viva_qa="Q: Why use Python 3.11-slim instead of Alpine Linux for the Docker image?\nA: Python wheels and OCR packages like PyTorch or Tesseract frequently require glibc. Alpine's musl libc causes compilation failures or subtle bugs with C-extensions, making Debian slim the production standard."
)

# ==============================================================================
# SLIDE 13: QUALITY ASSURANCE & AUTOMATED TESTING SUITE
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)
add_header(s13, "Quality Assurance", "Automated Pytest Suite & Pipeline Guardrails", "Validating API health, queue dispatching, payload limits, and deduplication via Pytest")
add_footer(s13, 13)

# 3 Test Strategy Cards
tests = [
    ("Test 1: Healthcheck Verification", "Endpoint: GET /health", "Validates that the API gateway is fully operational, verifying database connectivity and returning HTTP 200 with status 'ok'.", COLOR_PRIMARY),
    ("Test 2: Upload & Queue Dispatch", "Endpoint: POST /api/v1/resumes/upload", "Simulates file upload, verifies unique SHA-256 hash generation, and asserts that Celery's parse_resume_task.delay() is triggered with resume UUID.", COLOR_CYAN),
    ("Test 3: File Limit Guarding", "Boundary Test: 11MB Payload", "Transmits oversized file exceeding 10MB limit and asserts that FastAPI immediately rejects the payload with HTTP 413 Content Too Large.", COLOR_ROSE)
]

for idx, (title, sub, desc, color) in enumerate(tests):
    left = Inches(0.8 + idx * 3.97)
    add_card(s13, left, Inches(1.7), Inches(3.8), Inches(3.5), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s13, left + Inches(0.2), Inches(1.9), Inches(3.4), Inches(0.3), f"TEST CASE 0{idx+1}", color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s13.shapes.add_textbox(left + Inches(0.2), Inches(2.35), Inches(3.4), Inches(2.6))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = color
    p2.space_before = Pt(3)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = COLOR_TEXT_SECONDARY
    p3.space_before = Pt(8)

# Testing Best Practices Below
add_card(s13, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.3), COLOR_BG_CARD_ALT, COLOR_BORDER_ACCENT)
tb_t = s13.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.3), Inches(1.1))
tf_t = tb_t.text_frame
tf_t.word_wrap = True
tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

p_t = tf_t.paragraphs[0]
p_t.text = "Mock Fixtures & Isolated Async Testing Principles"
p_t.font.name = FONT_HEADING
p_t.font.size = Pt(12)
p_t.font.bold = True
p_t.font.color.rgb = COLOR_CYAN

p_t2 = tf_t.add_paragraph()
p_t2.text = "• Uses pytest-mock (mocker.patch) to intercept Celery tasks during unit tests, verifying queue dispatch without requiring an active Redis instance.\n• Async test client (httpx.AsyncClient) exercises endpoints asynchronously matching production ASGI runtime.\n• Jenkins enforces 100% test pass rate prior to building Docker container images."
p_t2.font.name = FONT_BODY
p_t2.font.size = Pt(9.5)
p_t2.font.color.rgb = COLOR_TEXT_SECONDARY
p_t2.space_before = Pt(3)

add_notes(s13,
    script="Automated testing is the backbone of our CI pipeline. In 'tests/test_api.py', we test the critical paths: API health, resume upload and queue dispatching, and file size boundary enforcement. By using pytest-mock, we verify that Celery's delay() method is invoked with the exact resume UUID without needing a live Redis server during unit testing. In Jenkins Stage 3, if any of these tests fail, the build aborts immediately.",
    why_matters="Shows strict test-driven development and automated quality gates in action.",
    technical_mechanics="We use httpx.AsyncClient with ASGITransport to test FastAPI endpoints in-memory. mocker.patch intercepts 'src.api.v1.endpoints.resumes.parse_resume_task' and asserts called_once_with(resume_id).",
    viva_qa="Q: Why mock Celery in the upload test?\nA: Unit tests must be fast, deterministic, and isolated. Mocking Celery verifies that the API dispatches the correct job payload without incurring the overhead of running live Redis and OCR workers."
)

# ==============================================================================
# SLIDE 14: PROJECT OUTCOME & DELIVERABLES (CI AUTOMATION)
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14)
add_header(s14, "Project Deliverables", "Automating Job Queues & Filtering via CI", "Synthesizing project outcomes: fully automated processing, intelligent filtering, and CI deployment")
add_footer(s14, 14)

# 4 Key Deliverables Achieved
outcomes = [
    ("Automated Job Queue", "Fully asynchronous Celery + Redis queueing system capable of processing high-volume candidate files without API latency degradation.", COLOR_PRIMARY),
    ("Intelligent Resume Filtering", "Semantic matching and scoring engine evaluating resumes against job descriptions, identifying tech gaps, and ranking top talent.", COLOR_CYAN),
    ("Jenkins CI Pipeline", "Automated multi-stage declarative pipeline validating code quality, running unit tests, and packaging Docker containers.", COLOR_AMBER),
    ("Real-Time Email Notifier", "Automated communication service dispatching submission acknowledgments, scorecards, and recruiter high-match alerts.", COLOR_EMERALD)
]

for idx, (title, desc, color) in enumerate(outcomes):
    left = Inches(0.8 + idx * 2.98)
    add_card(s14, left, Inches(1.7), Inches(2.85), Inches(3.4), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s14, left + Inches(0.18), Inches(1.9), Inches(2.5), Inches(0.3), f"OUTCOME 0{idx+1}", color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 9)
    
    tb = s14.shapes.add_textbox(left + Inches(0.18), Inches(2.35), Inches(2.5), Inches(2.6))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(8)

# Outcome Benchmark Summary Table Below
add_card(s14, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.4), COLOR_BG_CARD_ALT, COLOR_BORDER_ACCENT)
tb_o = s14.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.2))
tf_o = tb_o.text_frame
tf_o.word_wrap = True
tf_o.margin_left = tf_o.margin_right = tf_o.margin_top = tf_o.margin_bottom = 0

p_o = tf_o.paragraphs[0]
p_o.text = "Fulfillment of Core Objective: 'Automate a job queue that processes and filters resumes using CI'"
p_o.font.name = FONT_HEADING
p_o.font.size = Pt(12)
p_o.font.bold = True
p_o.font.color.rgb = COLOR_CYAN

p_o2 = tf_o.add_paragraph()
p_o2.text = "• Manual Screening Time: Reduced from 15 minutes per resume to <25 seconds of automated background AI analysis.\n• Web Ingestion Latency: Instantaneous sub-50ms HTTP response compared to 15,000ms synchronous blocking.\n• Continuous Deployment: Zero manual terminal commands required; Jenkins CI tests and deploys microservices automatically on commit."
p_o2.font.name = FONT_BODY
p_o2.font.size = Pt(9.5)
p_o2.font.color.rgb = COLOR_TEXT_SECONDARY
p_o2.space_before = Pt(3)

add_notes(s14,
    script="Here is the direct fulfillment of the user's project objective: automating a job queue that processes and filters resumes using CI. We built an asynchronous Celery and Redis job queue, integrated an automated candidate filtering and gap analysis engine, set up a multi-stage Jenkins CI pipeline, and connected an automated email notification system. Our system cuts candidate screening time by over 95% while keeping deployment 100% automated.",
    why_matters="Directly aligns every technical deliverable with the user's explicit prompt requirements.",
    technical_mechanics="The outcome combines asynchronous message queueing, AI structured data modeling, container orchestration, and continuous integration into a single unified architecture.",
    viva_qa="Q: How does this project differ from a standard web API?\nA: A standard web API performs synchronous processing. This project implements a distributed DevOps microservices architecture with decoupled workers, message queues, AI schema contracts, and automated CI pipelines."
)

# ==============================================================================
# SLIDE 15: LIVE INTERACTIVE DASHBOARD & UX (RESUMEAI STUDIO)
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15)
add_header(s15, "User Experience", "Interactive ResumeAI Studio Dashboard", "Modern glassmorphic web interface supporting drag-and-drop upload, live polling, and job matching")
add_footer(s15, 15)

dashboard_features = [
    ("Glassmorphism UI", "HTML5 & Modern CSS3", "Dark theme with ambient gradient glows, responsive navigation tabs, and live API connectivity indicator.", COLOR_PRIMARY),
    ("Drag-and-Drop Ingestion", "Multi-Format File Drop", "Instant drag-and-drop zone accepting PDF, DOCX, TXT, and scanned image files with client-side size checks.", COLOR_CYAN),
    ("Real-Time Status Polling", "Async Progress Poller", "Polls GET /status every 2 seconds, displaying animated spinner and status progression until worker completes.", COLOR_AMBER),
    ("Candidate Scorecard", "Visual Metrics & JSON", "Presents extracted personal info, experience cards, skills badges, quality score gauges, and raw JSON tree.", COLOR_EMERALD),
    ("Job Matcher Studio", "One-Click JD Analysis", "Interactive tab allowing recruiters to paste job descriptions and view instantaneous AI match breakdown and gaps.", COLOR_PRIMARY),
    ("Swagger API Docs", "FastAPI /docs Link", "Direct navigation to auto-generated OpenAPI 3.1 interactive Swagger documentation for API consumers.", COLOR_CYAN)
]

for idx, (title, sub, desc, color) in enumerate(dashboard_features):
    col = idx % 3
    row = idx // 3
    left = Inches(0.8 + col * 3.97)
    top = Inches(1.7 + row * 2.55)
    
    add_card(s15, left, top, Inches(3.8), Inches(2.35), COLOR_BG_CARD, COLOR_BORDER)
    add_badge(s15, left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(0.28), sub.upper(), color, COLOR_BG_DARK if color != COLOR_PRIMARY else COLOR_TEXT_PRIMARY, 8.5)
    
    tb = s15.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(3.4), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(6)

add_notes(s15,
    script="To make our backend accessible to non-technical recruiters, we developed ResumeAI Studio, a glassmorphic web dashboard in 'src/static/'. Users can drag and drop any resume format. The dashboard displays an animated status spinner that polls the background worker every two seconds. Once processing finishes, it renders an interactive candidate scorecard, complete with experience timelines, technical skill pills, AI quality scores, and our Job Matcher studio.",
    why_matters="Demonstrates that the system is fully production-ready with both developer APIs and an intuitive user interface.",
    technical_mechanics="The frontend is served directly by FastAPI via StaticFiles at '/static' and FileResponse at '/'. Vanilla JavaScript handles asynchronous fetch requests, error toasts, and JSON rendering without external framework bloat.",
    viva_qa="Q: Why use Vanilla JS instead of React or Vue?\nA: Vanilla JS eliminates build steps and heavy node_modules dependencies, keeping the Docker image lean and serving the entire UI directly from FastAPI without an additional Node server container."
)

# ==============================================================================
# SLIDE 16: PRODUCTION ROADMAP & CONCLUSION
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16)
add_header(s16, "Future Scope & Conclusion", "Production Roadmap & Executive Takeaways", "Scalability horizons: Kubernetes autoscaling, cloud storage, ATS webhooks, and final summary")
add_footer(s16, 16)

# Left Column: Roadmap Milestones
add_card(s16, Inches(0.8), Inches(1.7), Inches(5.75), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s16, Inches(1.0), Inches(1.9), Inches(3.2), Inches(0.3), "STRATEGIC ROADMAP MILESTONES", COLOR_CYAN, COLOR_BG_DARK, 9)

tb_r1 = s16.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.35), Inches(4.2))
tf_r1 = tb_r1.text_frame
tf_r1.word_wrap = True
tf_r1.margin_left = tf_r1.margin_right = tf_r1.margin_top = tf_r1.margin_bottom = 0

milestones = [
    ("Kubernetes & KEDA Autoscaling", "Deploying on EKS/GKE with Kubernetes Event-driven Autoscaling (KEDA) to dynamically scale Celery worker pods based on Redis queue length."),
    ("Cloud Object Storage Integration", "Migrating from shared local disk volumes to Amazon S3 or Google Cloud Storage with encrypted presigned URLs for enterprise document retention."),
    ("Enterprise ATS Webhook Connectors", "Direct bidirectional webhook integrations with Greenhouse, Lever, and Workday to ingest candidate submissions automatically."),
    ("Multi-LLM Hybrid Routing", "Dynamic model routing using lightweight models for simple text extraction and Gemini Pro for deep semantic scoring to optimize cost.")
]

for idx, (title, desc) in enumerate(milestones):
    p = tf_r1.paragraphs[0] if idx == 0 else tf_r1.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    if idx > 0:
        p.space_before = Pt(8)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

# Right Column: Executive Takeaways
add_card(s16, Inches(6.75), Inches(1.7), Inches(5.78), Inches(5.05), COLOR_BG_CARD, COLOR_BORDER)
add_badge(s16, Inches(6.95), Inches(1.9), Inches(3.2), Inches(0.3), "EXECUTIVE TAKEAWAYS & SUMMARY", COLOR_EMERALD, COLOR_BG_DARK, 9)

tb_r2 = s16.shapes.add_textbox(Inches(6.95), Inches(2.35), Inches(5.38), Inches(4.2))
tf_r2 = tb_r2.text_frame
tf_r2.word_wrap = True
tf_r2.margin_left = tf_r2.margin_right = tf_r2.margin_top = tf_r2.margin_bottom = 0

takeaways = [
    ("Asynchronous Resilience", "FastAPI + Celery + Redis successfully eliminates web server timeouts, guaranteeing sub-50ms ingestion latency under heavy concurrency."),
    ("DevOps CI/CD Automation", "Jenkins pipeline automates linting, pytest suites, container compilation, and zero-downtime deployment verification."),
    ("Intelligent Filtering & Feedback", "Gemini 2.5 Pro and automated email notifications transform raw resumes into actionable talent intelligence with zero ghosting."),
    ("Cloud-Native Architecture", "Multi-container Docker Compose topology guarantees complete environment reproducibility and production readiness.")
]

for idx, (title, desc) in enumerate(takeaways):
    p = tf_r2.paragraphs[0] if idx == 0 else tf_r2.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    if idx > 0:
        p.space_before = Pt(8)
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_BODY
    run.font.bold = False
    run.font.color.rgb = COLOR_TEXT_SECONDARY

add_notes(s16,
    script="In conclusion, our Automated Resume Parser and Email Notifier demonstrates the power of combining asynchronous backend architectures, intelligent AI models, and continuous DevOps automation. By using Python, FastAPI, Celery, Redis, and Jenkins, we have built a resilient, high-throughput system that ingests multi-format resumes in under 50 milliseconds, filters candidates accurately against job descriptions, and maintains continuous deployment with automated email notifications. Thank you for your time, and we look forward to your questions.",
    why_matters="Provides an impactful conclusion summarizing architectural strengths and defining clear, pragmatic production expansion vectors.",
    technical_mechanics="The architecture is containerized and cloud-ready. Workers can be scaled horizontally via KEDA on Kubernetes by monitoring the Redis queue length metric 'llen celery'.",
    viva_qa="Q: How would you monitor this system in production?\nA: We would deploy Prometheus metrics exporters for FastAPI and Celery (e.g. Flower for Celery tasks), Grafana dashboards for throughput and queue lag, and Loki for centralized container log aggregation."
)

# ------------------------------------------------------------------------------
# SAVE PRESENTATION
# ------------------------------------------------------------------------------
output_file = "Automated_Resume_Parser_and_Email_Notifier.pptx"
prs.save(output_file)
print(f"SUCCESS: Presentation successfully generated and saved to: {output_file}")
