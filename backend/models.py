
"""
Pydantic Models for API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class SymptomEnum(str, Enum):
    healthy = "healthy"
    leaf_spot = "leaf_spot"
    yellowing = "yellowing"
    wilt = "wilt"
    mosaic = "mosaic"
    leaf_distortion = "leaf_distortion"
    galls = "galls"
    necrosis_blight = "necrosis_blight"
    root_problem = "root_problem"
    stem_damage = "stem_damage"
    panicle_ear_problem = "panicle_ear_problem"

class CauseGroupEnum(str, Enum):
    fungal = "Fungal"
    bacterial = "Bacterial"
    viral = "Viral"
    insect = "Insect"
    nematode = "Nematode"
    nutrient_deficiency = "Nutrient_deficiency"
    abiotic_stress = "Abiotic_stress"

class DiagnosisRequest(BaseModel):
    crop: str = Field(..., description="Crop type (rice, eggplant, tomato, etc.)")
    district: str = Field(..., description="District name in Bangladesh")
    upazila: str = Field(..., description="Upazila name")
    phone_number: Optional[str] = Field(None, description="Farmer phone number")
    observation_flags: List[str] = Field(default=[], description="Observation flags from rule engine")

class DiagnosisResponse(BaseModel):
    status: str
    diagnosis_id: int
    symptom_detected: str
    confidence: float
    certainty_level: str
    probable_cause: str
    advisory: Dict
    explanation_bangla: Dict
    disclaimer: str
    logged_at: str

class WhatsAppMessage(BaseModel):
    phone_number: str
    message_type: str  # text, image, button_response
    content: str
    media_url: Optional[str] = None
    button_payload: Optional[str] = None

class WhatsAppResponse(BaseModel):
    to: str
    message: str
    buttons: Optional[List[Dict]] = None
    media: Optional[str] = None

class DashboardMetrics(BaseModel):
    total_diagnoses: int
    top_symptoms: List[Dict]
    top_crops: List[Dict]
    district_breakdown: List[Dict]
    confidence_distribution: Dict
    recent_alerts: List[Dict]

class OutbreakAlert(BaseModel):
    district: str
    upazila: str
    crop: str
    symptom: str
    case_count: int
    alert_level: str
    first_reported: datetime
