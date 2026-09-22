# 🇧🇩 National AI-Enabled Crop Health Advisory System

## Complete Deployment Package

**Version:** 1.0.0  
**Date:** 2024  
**License:** Government of Bangladesh - Ministry of Agriculture

---

## 🚀 Quick Start (Choose Your Platform)

### Linux / macOS
```bash
# Make executable and run
chmod +x setup.sh
./setup.sh deploy
```

### Windows
```cmd
# Double-click or run in Command Prompt
setup.bat
```

### Python (Cross-Platform)
```bash
# Requires Python 3.8+
python auto_deploy.py deploy
```

---

## 📦 What's Included

### Core Application (Backend)
- **FastAPI** web framework
- **TensorFlow/PyTorch** AI model
- **PostgreSQL** database
- **Redis** caching
- **NGINX** reverse proxy
- **Docker** containerization

### Mobile Application
- **Flutter** cross-platform app
- Camera integration
- Offline support
- Bangla UI

### Dashboard & Analytics
- PostgreSQL schema
- MIS analytics queries
- Early warning system

### Deployment Tools
- `setup.sh` - Universal Linux/macOS installer
- `setup.bat` - Windows installer
- `auto_deploy.py` - Advanced Python deployment manager
- `one_click_deploy.sh` - Quick bash deployment
- `install_wizard.py` - Interactive setup wizard
- `docker-compose.yml` - Docker orchestration
- `crop-advisory.service` - systemd auto-start
- `.github/workflows/deploy.yml` - CI/CD pipeline

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│  Farmer (Mobile/WhatsApp/Web)           │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  NGINX (SSL/Reverse Proxy)              │
│  Port: 80/443                           │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  FastAPI Backend                        │
│  Port: 8000                             │
│  ├─ AI Symptom Classifier (CNN)         │
│  ├─ Plantwise Rule Engine               │
│  ├─ Bangladesh Advisory KB            │
│  └─ Bangla Explanation Generator        │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  PostgreSQL Database                    │
│  Port: 5432                             │
│  ├─ Diagnosis logs                      │
│  ├─ Outbreak alerts                     │
│  └─ User management                     │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Redis Cache                            │
│  Port: 6379                             │
└─────────────────────────────────────────┘
```

---

## 🔧 System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk | 20 GB SSD | 50+ GB SSD |
| OS | Ubuntu 20.04 | Ubuntu 22.04 LTS |
| Docker | 20.10+ | Latest |
| Docker Compose | 1.29+ | 2.x |

---

## 📋 Pre-Deployment Checklist

- [ ] Docker installed and running
- [ ] Ports 80, 443, 8000, 5432, 6379 available
- [ ] Domain name configured (for production)
- [ ] SSL certificates (or use auto-generated)
- [ ] WhatsApp Business API credentials (optional)

---

## 🚀 Deployment Steps

### 1. Extract Package
```bash
tar -xzf bd_crop_advisory_package.tar.gz
cd bd_crop_advisory_package
```

### 2. Run Setup
```bash
# Linux/macOS
./setup.sh deploy

# Windows
setup.bat
```

### 3. Verify Deployment
```bash
# Health check
curl http://localhost:8000/

# API documentation
curl http://localhost:8000/api/docs

# Test diagnosis
curl -X POST http://localhost:8000/api/v1/diagnose   -F "image=@test.jpg"   -F "crop=rice"   -F "district=Dhaka"
```

---

## 🔐 Security Configuration

### Environment Variables
Edit `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/crop_advisory

# Security
SECRET_KEY=your-secure-secret-key

# WhatsApp (optional)
WHATSAPP_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
```

### SSL Certificates
- **Development:** Auto-generated self-signed
- **Production:** Replace with Let's Encrypt or commercial certificates

```bash
# Using Let's Encrypt
certbot certonly --standalone -d your-domain.com
```

---

## 📱 WhatsApp Integration

1. Create WhatsApp Business Account
2. Get API credentials from Meta Developer Console
3. Configure webhook URL: `https://your-domain/api/v1/whatsapp/webhook`
4. Set verify token: `crop_health_bot`

---

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# System status
./setup.sh status

# Service logs
./setup.sh logs

# Specific service
./setup.sh logs api
```

### Database Backup
```bash
# Automated backup
./setup.sh backup

# Manual backup
cd backend
docker-compose exec db pg_dump -U postgres crop_advisory > backup.sql
```

### Updates
```bash
# Pull latest images
cd backend
docker-compose pull
docker-compose up -d
```

---

## 🛡️ AI Governance & Compliance

### Mandatory Rules
- ❌ No final disease confirmation
- ❌ No pesticide dosage recommendations
- ❌ No unapproved product recommendations
- ✅ Always include disclaimer
- ✅ Human officer oversight required
- ✅ All outputs logged and auditable

### Compliance Standards
- **DAE:** Department of Agricultural Extension
- **BRRI:** Bangladesh Rice Research Institute
- **BARI:** Bangladesh Agricultural Research Institute
- **SRDI:** Soil Resource Development Institute
- **BARC:** Bangladesh Agricultural Research Council

---

## 📞 Support & Contact

| Type | Contact |
|------|---------|
| Technical | DAE IT Division |
| Agricultural | 16263 (DAE Hotline) |
| Emergency | Upazila Agriculture Officer |
| Email | admin@cropadvisory.gov.bd |

---

## 🔄 Scale Strategy

| Phase | Coverage | Timeline | Status |
|-------|----------|----------|--------|
| Phase 1 | 1 District (Pilot) | Month 1-3 | ✅ Ready |
| Phase 2 | 10 Districts | Month 4-6 | 📋 Planned |
| Phase 3 | National Rollout | Month 7-12 | 📋 Planned |
| Phase 4 | Climate Integration | Year 2 | 📋 Future |

---

## 📝 Changelog

### v1.0.0 (2024)
- Initial release
- AI symptom classification (11 categories)
- Plantwise rule engine integration
- Bangladesh advisory knowledge base
- Bangla language support
- WhatsApp integration
- MIS dashboard
- Docker containerization
- Automated deployment

---

## 🤝 Contributing

This is a government project. For contributions:

1. Contact DAE IT Division
2. Submit PR with BARI/BRRI validation
3. Security review required
4. Compliance check mandatory

---

**Built with ❤️ for Bangladesh Farmers** 🇧🇩🌾
