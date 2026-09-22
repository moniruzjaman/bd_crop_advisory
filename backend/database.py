
"""
Database Configuration
PostgreSQL for national-scale deployment
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@localhost/crop_advisory_db"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

class DiagnosisLog(Base):
    """
    Diagnosis log table for MIS and early warning
    """
    __tablename__ = "diagnosis_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=True, index=True)
    district = Column(String(100), nullable=False, index=True)
    upazila = Column(String(100), nullable=False)
    crop = Column(String(50), nullable=False, index=True)
    symptom = Column(String(50), nullable=False)
    diagnosis = Column(String(200), nullable=False)
    cause_group = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    ai_certainty = Column(String(20), nullable=False)
    advisory_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    image_hash = Column(String(64), nullable=True)  # For deduplication
    farmer_feedback = Column(String(20), nullable=True)  # helpful/not_helpful

    def __repr__(self):
        return f"<DiagnosisLog(id={self.id}, crop={self.crop}, district={self.district})>"

class CropOutbreakAlert(Base):
    """
    Early warning system for pest/disease outbreaks
    """
    __tablename__ = "outbreak_alerts"

    id = Column(Integer, primary_key=True)
    district = Column(String(100), nullable=False, index=True)
    upazila = Column(String(100), nullable=False)
    crop = Column(String(50), nullable=False)
    symptom = Column(String(50), nullable=False)
    cause_group = Column(String(50), nullable=False)
    case_count = Column(Integer, default=1)
    first_reported = Column(DateTime, default=datetime.utcnow)
    alert_level = Column(String(20), default="low")  # low, medium, high
    status = Column(String(20), default="active")  # active, resolved
    notified_officers = Column(JSON, nullable=True)

class User(Base):
    """
    Admin users for dashboard
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(20), default="officer")  # admin, officer, viewer
    district = Column(String(100), nullable=True)
    is_active = Column(Integer, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
