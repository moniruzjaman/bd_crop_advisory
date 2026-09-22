
-- National Crop Health Advisory System Database Schema
-- PostgreSQL for Bangladesh Government Deployment

-- Main diagnosis logs table
CREATE TABLE diagnosis_logs (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20),
    district VARCHAR(100) NOT NULL,
    upazila VARCHAR(100) NOT NULL,
    union_name VARCHAR(100),
    crop VARCHAR(50) NOT NULL,
    symptom VARCHAR(50) NOT NULL,
    diagnosis VARCHAR(200) NOT NULL,
    cause_group VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    ai_certainty VARCHAR(20) NOT NULL,
    advisory_data JSONB,
    image_hash VARCHAR(64),
    farmer_feedback VARCHAR(20),
    weather_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for performance
    INDEX idx_district_crop (district, crop),
    INDEX idx_timestamp (timestamp),
    INDEX idx_cause_group (cause_group),
    INDEX idx_symptom (symptom)
);

-- Outbreak alerts for early warning system
CREATE TABLE outbreak_alerts (
    id SERIAL PRIMARY KEY,
    district VARCHAR(100) NOT NULL,
    upazila VARCHAR(100) NOT NULL,
    crop VARCHAR(50) NOT NULL,
    symptom VARCHAR(50) NOT NULL,
    cause_group VARCHAR(50) NOT NULL,
    case_count INTEGER DEFAULT 1,
    first_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_level VARCHAR(20) DEFAULT 'low', -- low, medium, high, critical
    status VARCHAR(20) DEFAULT 'active', -- active, monitoring, resolved
    notified_officers JSONB,
    weather_correlation JSONB,

    INDEX idx_alert_district (district, alert_level),
    INDEX idx_alert_crop (crop, alert_level)
);

-- Users table for dashboard access
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'officer', -- admin, officer, viewer, expert
    district VARCHAR(100),
    upazila VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Knowledge base updates tracking
CREATE TABLE kb_updates (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL, -- BRRI, BARI, DAE, etc.
    crop VARCHAR(50) NOT NULL,
    update_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    approved_by INTEGER REFERENCES users(id),
    approved_at TIMESTAMP,
    effective_date DATE
);

-- Farmer feedback for model improvement
CREATE TABLE farmer_feedback (
    id SERIAL PRIMARY KEY,
    diagnosis_id INTEGER REFERENCES diagnosis_logs(id),
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    helpful BOOLEAN,
    comments TEXT,
    followed_advice BOOLEAN,
    outcome VARCHAR(50), -- improved, same, worsened, unknown
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
