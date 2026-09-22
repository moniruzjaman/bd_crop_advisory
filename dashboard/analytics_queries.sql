
-- MIS Dashboard Analytics Queries for Bangladesh Crop Advisory System

-- 1. Top symptoms by district (last 30 days)
SELECT 
    district,
    symptom,
    COUNT(*) as case_count,
    ROUND(AVG(confidence) * 100, 2) as avg_confidence
FROM diagnosis_logs
WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY district, symptom
ORDER BY district, case_count DESC;

-- 2. Pest outbreak frequency by crop
SELECT 
    crop,
    cause_group,
    COUNT(*) as total_cases,
    COUNT(DISTINCT district) as districts_affected,
    COUNT(DISTINCT upazila) as upazilas_affected
FROM diagnosis_logs
WHERE cause_group IN ('Insect', 'Fungal', 'Bacterial', 'Viral', 'Nematode')
    AND timestamp >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY crop, cause_group
ORDER BY total_cases DESC;

-- 3. Nutrient deficiency trends
SELECT 
    district,
    crop,
    COUNT(*) as deficiency_cases,
    ROUND(AVG(confidence) * 100, 2) as avg_confidence
FROM diagnosis_logs
WHERE cause_group = 'Nutrient_deficiency'
    AND timestamp >= CURRENT_DATE - INTERVAL '60 days'
GROUP BY district, crop
HAVING COUNT(*) > 5
ORDER BY deficiency_cases DESC;

-- 4. Monthly diagnosis volume
SELECT 
    DATE_TRUNC('month', timestamp) as month,
    COUNT(*) as total_diagnoses,
    COUNT(DISTINCT phone_number) as unique_farmers,
    ROUND(AVG(confidence) * 100, 2) as avg_confidence
FROM diagnosis_logs
WHERE timestamp >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', timestamp)
ORDER BY month;

-- 5. Climate-linked surge detection
WITH daily_counts AS (
    SELECT 
        DATE(timestamp) as date,
        district,
        crop,
        symptom,
        COUNT(*) as daily_cases
    FROM diagnosis_logs
    WHERE timestamp >= CURRENT_DATE - INTERVAL '14 days'
    GROUP BY DATE(timestamp), district, crop, symptom
),
avg_counts AS (
    SELECT 
        district,
        crop,
        symptom,
        AVG(daily_cases) as avg_cases,
        STDDEV(daily_cases) as stddev_cases
    FROM daily_counts
    GROUP BY district, crop, symptom
)
SELECT 
    d.date,
    d.district,
    d.crop,
    d.symptom,
    d.daily_cases,
    a.avg_cases,
    CASE 
        WHEN d.daily_cases > a.avg_cases + (2 * a.stddev_cases) THEN 'SURGE'
        WHEN d.daily_cases > a.avg_cases + (1.5 * a.stddev_cases) THEN 'ELEVATED'
        ELSE 'NORMAL'
    END as alert_status
FROM daily_counts d
JOIN avg_counts a ON d.district = a.district AND d.crop = a.crop AND d.symptom = a.symptom
WHERE d.daily_cases > a.avg_cases + (1.5 * a.stddev_cases)
ORDER BY d.date DESC, d.daily_cases DESC;

-- 6. Low confidence diagnoses requiring expert review
SELECT 
    id,
    district,
    upazila,
    crop,
    symptom,
    confidence,
    timestamp,
    phone_number
FROM diagnosis_logs
WHERE confidence < 0.6
    AND timestamp >= CURRENT_DATE - INTERVAL '7 days'
    AND farmer_feedback IS NULL
ORDER BY timestamp DESC;

-- 7. Crop-wise advisory effectiveness
SELECT 
    crop,
    COUNT(*) as total_diagnoses,
    COUNT(f.id) as feedback_count,
    ROUND(AVG(f.accuracy_rating), 2) as avg_rating,
    SUM(CASE WHEN f.helpful THEN 1 ELSE 0 END) as helpful_count,
    ROUND(100.0 * SUM(CASE WHEN f.helpful THEN 1 ELSE 0 END) / NULLIF(COUNT(f.id), 0), 2) as helpful_percentage
FROM diagnosis_logs d
LEFT JOIN farmer_feedback f ON d.id = f.diagnosis_id
WHERE d.timestamp >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY crop
ORDER BY avg_rating DESC NULLS LAST;

-- 8. District-wise coverage metrics
SELECT 
    district,
    COUNT(DISTINCT upazila) as upazilas_covered,
    COUNT(DISTINCT phone_number) as unique_farmers,
    COUNT(*) as total_diagnoses,
    COUNT(DISTINCT crop) as crops_supported
FROM diagnosis_logs
WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY district
ORDER BY total_diagnoses DESC;
