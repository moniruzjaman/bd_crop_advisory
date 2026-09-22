# 🇧🇩 National AI-Enabled Crop Health Advisory System

## Government Grade Implementation for Bangladesh

**Ministry-aligned Architecture | Plantwise Protocol | DAE/BARI/BRRI/SRDI/BARC Compliant**

---

## 📋 System Overview

This is a national-scale AI-assisted crop diagnosis and advisory platform designed for Bangladesh farmers. The system follows the **Plantwise Symptom-First Diagnosis Protocol** and integrates authoritative knowledge from Bangladesh Agricultural Research Institutes.

### Key Features

- ✅ **AI Symptom Classification** (CNN-based, 11 symptom categories)
- ✅ **Plantwise Rule Engine** (JSON-based elimination logic)
- ✅ **Bangladesh Authoritative Advisory** (BRRI/BARI/DAE/SRDI/BARC)
- ✅ **Bangla Language Support** (Farmer-friendly explanations)
- ✅ **WhatsApp Integration** (Button messages for low-literacy users)
- ✅ **MIS Dashboard** (Early warning and analytics)
- ✅ **Human-in-the-Loop Governance** (AI is Decision Support only)

---

## 🏗️ Architecture

```
Farmer (Mobile/WhatsApp)
    ↓
FastAPI Backend (Docker)
    ↓
Symptom AI Model (CNN 224x224)
    ↓
Rule Engine (Plantwise Protocol)
    ↓
Bangladesh Advisory KB (BRRI/BARI/DAE)
    ↓
Bangla Explanation Generator
    ↓
PostgreSQL + Redis + MIS Dashboard
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- 4GB RAM minimum
- 20GB disk space

### Deployment

```bash
# Clone repository
git clone https://github.com/bd-gov/crop-advisory-system.git
cd crop-advisory-system

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Deploy
./deploy.sh
```

### Access Points

- **API Documentation**: `https://api.cropadvisory.gov.bd/api/docs`
- **WhatsApp Webhook**: `https://api.cropadvisory.gov.bd/api/v1/whatsapp/webhook`
- **Health Check**: `https://api.cropadvisory.gov.bd/`

---

## 📁 Project Structure

```
bd_crop_advisory_system/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── ai_model.py            # CNN Symptom Classifier
│   ├── rule_engine.py         # Plantwise Elimination Logic
│   ├── advisory_engine.py     # Bangladesh KB Integration
│   ├── bangla_explainer.py    # Bangla Explanation Generator
│   ├── whatsapp_webhook.py    # WhatsApp Cloud API Handler
│   ├── database.py            # PostgreSQL Models
│   ├── security.py            # JWT & Rate Limiting
│   ├── Dockerfile             # Container definition
│   ├── docker-compose.yml     # Multi-service orchestration
│   └── requirements.txt       # Python dependencies
├── mobile_app/
│   ├── main.dart              # Flutter application
│   └── pubspec.yaml           # Flutter dependencies
├── dashboard/
│   ├── schema.sql             # PostgreSQL schema
│   └── analytics_queries.sql  # MIS dashboard queries
├── deploy.sh                  # Deployment script
├── test_system.py             # Testing suite
└── README.md                  # This file
```

---

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/crop_advisory

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key

# WhatsApp Cloud API
WHATSAPP_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
VERIFY_TOKEN=your-verify-token
```

---

## 🧪 Testing

```bash
# Run all tests
python test_system.py

# Or test specific components
curl http://localhost:8000/api/v1/symptoms
curl http://localhost:8000/api/v1/crops
```

---

## 📊 API Endpoints

### Diagnosis

```bash
POST /api/v1/diagnose
Content-Type: multipart/form-data

Parameters:
  - image: File (JPEG/PNG, max 10MB)
  - crop: string (rice, eggplant, tomato, etc.)
  - district: string
  - upazila: string
  - phone_number: string (optional)
  - observation_flags: JSON array (optional)

Response:
{
  "status": "success",
  "diagnosis_id": 123,
  "symptom_detected": "leaf_spot",
  "confidence": 0.85,
  "probable_cause": "Fungal",
  "advisory": { ... },
  "explanation_bangla": { ... },
  "disclaimer": "এটি AI-পরামর্শ..."
}
```

### WhatsApp Webhook

```bash
GET /api/v1/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=...
POST /api/v1/whatsapp/webhook (message receiving)
```

---

## 🛡️ Security & Governance

### AI Governance Rules (Mandatory)

- ❌ **AI must NOT**: Provide final disease confirmation
- ❌ **AI must NOT**: Provide pesticide dosage
- ❌ **AI must NOT**: Recommend unapproved products
- ❌ **AI must NOT**: Override human officer decision

- ✅ **AI must**: Log all outputs
- ✅ **AI must**: Be auditable
- ✅ **AI must**: Use knowledge base only
- ✅ **AI must**: Include disclaimer

### Compliance

- **DAE**: Department of Agricultural Extension
- **BRRI**: Bangladesh Rice Research Institute
- **BARI**: Bangladesh Agricultural Research Institute
- **SRDI**: Soil Resource Development Institute
- **BARC**: Bangladesh Agricultural Research Council

---

## 📱 Mobile App

The Flutter mobile app provides:

- 📸 Camera integration for image capture
- 🌾 Crop selection with Bangla UI
- 🤖 AI diagnosis with visual feedback
- 📚 Offline advisory access
- 📞 Direct helpline integration (16263)

### Build Mobile App

```bash
cd mobile_app
flutter pub get
flutter build apk --release
```

---

## 📈 MIS Dashboard Metrics

- Top symptoms by district
- Pest outbreak frequency
- Nutrient deficiency trends
- Monthly diagnosis volume
- Climate-linked surge detection
- Advisory effectiveness ratings

---

## 🔄 Scale Strategy

| Phase | Coverage | Timeline |
|-------|----------|----------|
| Phase 1 | 1 District (Pilot) | Month 1-3 |
| Phase 2 | 10 Districts | Month 4-6 |
| Phase 3 | National Rollout | Month 7-12 |
| Phase 4 | Climate Integration | Year 2 |

---

## 🤝 Contributing

This is a government project. For contributions:

1. Contact DAE IT Division
2. Submit PR with BARI/BRRI validation
3. Security review required
4. Compliance check mandatory

---

## 📞 Support

- **Technical**: DAE IT Division
- **Agricultural**: 16263 (DAE Hotline)
- **Emergency**: Upazila Agriculture Officer

---

## 📄 License

Government of Bangladesh - Ministry of Agriculture

---

**Built with ❤️ for Bangladesh Farmers**
