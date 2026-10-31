"""
Location: /src/worker/notifier.py
Automated Email Notification Service for Resume Parsing & Candidate Filtering.
Dispatches asynchronous email updates to candidates and recruiters via SMTP/SendGrid.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@resumeparser.ai")
RECRUITER_EMAIL = os.getenv("RECRUITER_EMAIL", "recruiter@example.com")


def send_email_notification(to_email: str, subject: str, html_content: str) -> bool:
    """
    Sends an HTML email notification. Logs gracefully in mock/development mode
    if SMTP credentials are not configured.
    """
    if not SMTP_USER or not SMTP_PASS:
        print(f"[NOTIFIER MOCK] Email would be sent to: {to_email}")
        print(f"[NOTIFIER MOCK] Subject: {subject}")
        print(f"[NOTIFIER MOCK] Preview: {html_content[:150]}...")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        part = MIMEText(html_content, "html")
        msg.attach(part)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"[NOTIFIER] Email successfully dispatched to {to_email}")
        return True
    except Exception as e:
        print(f"[NOTIFIER_ERROR] Failed to send email to {to_email}: {e}")
        return False


def notify_candidate_received(candidate_email: str, candidate_name: str, file_name: str):
    """Sends confirmation email to candidate that resume has been queued."""
    subject = f"Resume Received & Queued for Processing: {file_name}"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #4F46E5;">Application Acknowledged</h2>
        <p>Dear {candidate_name or 'Applicant'},</p>
        <p>Your resume (<strong>{file_name}</strong>) has been successfully uploaded to our automated evaluation pipeline.</p>
        <p>Our distributed Celery queue is currently analyzing your technical background and experience.</p>
        <p>Best regards,<br>Talent Operations Team</p>
      </body>
    </html>
    """
    return send_email_notification(candidate_email, subject, html)


def notify_parsing_completed(candidate_email: str, candidate_name: str, quality_score: int, industry_fit: Dict[str, float]):
    """Sends notification once AI parsing and scoring is complete."""
    top_industry = max(industry_fit.items(), key=lambda x: x[1])[0] if industry_fit else "Technology"
    subject = f"Profile Evaluated: Quality Score {quality_score}/100"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #059669;">Profile Analysis Complete</h2>
        <p>Dear {candidate_name or 'Applicant'},</p>
        <p>Our AI evaluation engine has finished analyzing your credentials:</p>
        <ul>
          <li><strong>Quality Score:</strong> {quality_score} / 100</li>
          <li><strong>Primary Industry Match:</strong> {top_industry.replace('_', ' ').title()}</li>
        </ul>
        <p>Recruiters have been notified of your profile matching score.</p>
      </body>
    </html>
    """
    return send_email_notification(candidate_email, subject, html)


def notify_recruiter_high_match(candidate_name: str, candidate_email: str, overall_score: int, job_title: str):
    """Alerts recruiters when a candidate meets high-match threshold for a requisition."""
    subject = f"[HIGH-MATCH ALERT] {candidate_name} scored {overall_score}% for {job_title}"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #1e293b;">
        <h2 style="color: #6366F1;">Candidate Matched Requisition Threshold</h2>
        <p>A candidate has exceeded the matching threshold for <strong>{job_title}</strong>:</p>
        <ul>
          <li><strong>Name:</strong> {candidate_name}</li>
          <li><strong>Email:</strong> {candidate_email}</li>
          <li><strong>Overall Match Score:</strong> {overall_score}%</li>
        </ul>
        <p>Please review the full structured extraction and gap analysis in the ResumeAI Studio Dashboard.</p>
      </body>
    </html>
    """
    return send_email_notification(RECRUITER_EMAIL, subject, html)

