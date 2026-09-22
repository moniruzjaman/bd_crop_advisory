
"""
🇧🇩 National AI-Enabled Crop Health Advisory System
FastAPI Backend - Government Grade Implementation
Ministry-aligned Architecture | Plantwise Protocol
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime
import json

from ai_model import SymptomClassifier
from rule_engine import RuleEngine
from advisory_engine import AdvisoryEngine
from bangla_explainer import BanglaExplainer
from database import get_db, engine, Base
from models import DiagnosisLog
from whatsapp_webhook import whatsapp_router
from security import verify_token, rate_limiter

# Initialize FastAPI app
app = FastAPI(
    title="🇧🇩 National Crop Health Advisory System",
    description="AI-assisted crop diagnosis for Bangladesh farmers",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize components
symptom_classifier = SymptomClassifier()
rule_engine = RuleEngine()
advisory_engine = AdvisoryEngine()
bangla_explainer = BanglaExplainer()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {
        "message": "🇧🇩 National AI-Enabled Crop Health Advisory System",
        "status": "operational",
        "protocol": "Plantwise Symptom-First",
        "compliance": ["DAE", "BRRI", "BARI", "SRDI", "BARC"]
    }

@app.post("/api/v1/diagnose")
async def diagnose_crop(
    image: UploadFile = File(...),
    crop: str = Form(...),
    district: str = Form(...),
    upazila: str = Form(...),
    phone_number: Optional[str] = Form(None),
    observation_flags: Optional[str] = Form("[]"),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Main diagnosis endpoint
    Accepts crop image and returns AI-assisted advisory
    """
    # Verify authentication
    verify_token(credentials.credentials)

    # Rate limiting
    await rate_limiter(phone_number or "anonymous")

    try:
        # Parse observation flags
        flags = json.loads(observation_flags) if observation_flags else []

        # Step 1: AI Symptom Classification
        symptom_result = await symptom_classifier.classify(image)

        # Step 2: Rule Engine Processing
        rule_result = rule_engine.process(
            symptom=symptom_result["symptom"],
            observation_flags=flags,
            crop=crop
        )

        # Step 3: Generate Advisory
        advisory = advisory_engine.generate(
            symptom=symptom_result["symptom"],
            cause_group=rule_result["cause_group"],
            crop=crop,
            confidence=symptom_result["confidence"]
        )

        # Step 4: Generate Bangla Explanation
        explanation = bangla_explainer.generate(
            diagnosis=advisory["diagnosis"],
            cause=rule_result["cause_group"],
            advice=advisory["advice"]
        )

        # Step 5: Log to Database
        log_entry = DiagnosisLog(
            phone_number=phone_number,
            district=district,
            upazila=upazila,
            crop=crop,
            symptom=symptom_result["symptom"],
            diagnosis=advisory["diagnosis"],
            cause_group=rule_result["cause_group"],
            confidence=symptom_result["confidence"],
            ai_certainty="low" if symptom_result["confidence"] < 0.6 else "medium" if symptom_result["confidence"] < 0.8 else "high",
            advisory_data=json.dumps(advisory),
            timestamp=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()

        return {
            "status": "success",
            "diagnosis_id": log_entry.id,
            "symptom_detected": symptom_result["symptom"],
            "confidence": symptom_result["confidence"],
            "certainty_level": "low" if symptom_result["confidence"] < 0.6 else "medium" if symptom_result["confidence"] < 0.8 else "high",
            "probable_cause": rule_result["cause_group"],
            "advisory": advisory,
            "explanation_bangla": explanation,
            "disclaimer": "এটি কেবল AI-সহায়তা পরামর্শ। চূড়ান্ত নির্ণয়ের জন্য কৃষি কর্মকর্তার সাথে যোগাযোগ করুন।",
            "logged_at": log_entry.timestamp.isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Diagnosis failed: {str(e)}"
        )

@app.get("/api/v1/symptoms")
async def get_symptoms():
    """Return available symptom categories"""
    return {
        "symptoms": [
            {"id": "healthy", "name_en": "Healthy", "name_bn": "সুস্থ"},
            {"id": "leaf_spot", "name_en": "Leaf Spot", "name_bn": "পাতা পচা/দাগ"},
            {"id": "yellowing", "name_en": "Yellowing", "name_bn": "হলুদ হয়ে যাওয়া"},
            {"id": "wilt", "name_en": "Wilting", "name_bn": "গাছ শুকিয়ে যাওয়া"},
            {"id": "mosaic", "name_en": "Mosaic Pattern", "name_bn": "মোজাইক প্যাটার্ন"},
            {"id": "leaf_distortion", "name_en": "Leaf Distortion", "name_bn": "পাতা বিকৃতি"},
            {"id": "galls", "name_en": "Galls/Swellings", "name_bn": "গাল/ফোলা"},
            {"id": "necrosis_blight", "name_en": "Necrosis/Blight", "name_bn": "পাতা পোড়া/ঝলসে যাওয়া"},
            {"id": "root_problem", "name_en": "Root Problem", "name_bn": "গোড়া সমস্যা"},
            {"id": "stem_damage", "name_en": "Stem Damage", "name_bn": "কাণ্ড ক্ষতি"},
            {"id": "panicle_ear_problem", "name_en": "Panicle/Ear Problem", "name_bn": "শীষ/ফুল সমস্যা"}
        ]
    }

@app.get("/api/v1/crops")
async def get_crops():
    """Return supported crops for Bangladesh"""
    return {
        "crops": [
            {"id": "rice", "name_en": "Rice", "name_bn": "ধান", "authority": "BRRI"},
            {"id": "wheat", "name_en": "Wheat", "name_bn": "গম", "authority": "BARI"},
            {"id": "maize", "name_en": "Maize", "name_bn": "ভুট্টা", "authority": "BARI"},
            {"id": "eggplant", "name_en": "Eggplant", "name_bn": "বেগুন", "authority": "BARI"},
            {"id": "tomato", "name_en": "Tomato", "name_bn": "টমেটো", "authority": "BARI"},
            {"id": "potato", "name_en": "Potato", "name_bn": "আলু", "authority": "BARI"},
            {"id": "cabbage", "name_en": "Cabbage", "name_bn": "বাঁধাকপি", "authority": "BARI"},
            {"id": "cauliflower", "name_en": "Cauliflower", "name_bn": "ফুলকপি", "authority": "BARI"},
            {"id": "okra", "name_en": "Okra", "name_bn": "ঢেঁড়স", "authority": "BARI"},
            {"id": "cucumber", "name_en": "Cucumber", "name_bn": "শসা", "authority": "BARI"},
            {"id": "country_bean", "name_en": "Country Bean", "name_bn": "শিম", "authority": "BARI"},
            {"id": "mango", "name_en": "Mango", "name_bn": "আম", "authority": "BARI"},
            {"id": "jute", "name_en": "Jute", "name_bn": "পাট", "authority": "BJRI"}
        ]
    }

# Include WhatsApp webhook
app.include_router(whatsapp_router, prefix="/api/v1/whatsapp", tags=["whatsapp"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
