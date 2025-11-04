# Location: /src/api/v1/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
import uuid

# --- Pydantic models for the GET /resumes/{id} response ---
# These match the "Parsed Data Retrieval" section of the spec

class ResumeMetadata(BaseModel):
    fileName: str
    fileSize: int
    uploadedAt: datetime
    processedAt: Optional[datetime] = None
    processingTime: Optional[float] = None

class PersonalInfoName(BaseModel):
    first: Optional[str] = None
    last: Optional[str] = None
    full: Optional[str] = None

class PersonalInfoContactAddress(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipCode: Optional[str] = None
    country: Optional[str] = None

class PersonalInfoContact(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[PersonalInfoContactAddress] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None

class PersonalInfo(BaseModel):
    name: Optional[PersonalInfoName] = None
    contact: Optional[PersonalInfoContact] = None

class Summary(BaseModel):
    text: Optional[str] = None
    careerLevel: Optional[str] = None
    industryFocus: Optional[str] = None

class Experience(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    current: Optional[bool] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    achievements: Optional[List[str]] = []
    technologies: Optional[List[str]] = []

class Education(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    graduationDate: Optional[str] = None
    gpa: Optional[float] = None
    honors: Optional[List[str]] = []

class SkillCategory(BaseModel):
    category: str
    items: List[str]

class SkillLanguage(BaseModel):
    language: str
    proficiency: str

class Skills(BaseModel):
    technical: Optional[List[SkillCategory]] = []
    soft: Optional[List[str]] = []
    languages: Optional[List[SkillLanguage]] = []

class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    issueDate: Optional[str] = None
    expiryDate: Optional[str] = None
    credentialId: Optional[str] = None

class AIEnhancements(BaseModel):
    qualityScore: Optional[int] = None
    completenessScore: Optional[int] = None
    suggestions: Optional[List[str]] = []
    industryFit: Optional[Dict[str, float]] = {}

class ResumeDataResponse(BaseModel):
    """
    The main response model for the GET /resumes/{id} endpoint.
    """
    id: uuid.UUID
    metadata: ResumeMetadata
    personalInfo: Optional[PersonalInfo] = None
    summary: Optional[Summary] = None
    experience: Optional[List[Experience]] = []
    education: Optional[List[Education]] = []
    skills: Optional[Skills] = None
    certifications: Optional[List[Certification]] = []
    aiEnhancements: Optional[AIEnhancements] = None

    class Config:
        from_attributes = True # Replaces orm_mode = True