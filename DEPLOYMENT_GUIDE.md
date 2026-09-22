# 🚀 Automated Deployment Guide

## Quick Start (Choose One Method)

### Method 1: One-Click Deploy (Recommended)
```bash
./one_click_deploy.sh
```
This script automatically:
- Checks/installs Docker
- Sets up environment
- Generates SSL certificates
- Builds and deploys all services
- Performs health checks

### Method 2: Interactive Wizard
```bash
./install_wizard.py
```
Guided setup with custom configuration options.

### Method 3: Python Deployment Manager
```bash
./auto_deploy.py deploy
```
Advanced deployment with full control:
```bash
# Deploy
./auto_deploy.py deploy

# Check status
./auto_deploy.py status

# View logs
./auto_deploy.py logs

# Backup database
./auto_deploy.py backup

# Stop services
./auto_deploy.py stop

# Restart
./auto_deploy.py restart
```

### Method 4: Manual Docker
```bash
cd backend
docker-compose up -d
```

---

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk | 20 GB | 50+ GB |
| OS | Ubuntu 20.04+ | Ubuntu 22.04 LTS |

---

## Pre-Deployment Checklist

- [ ] Docker installed
- [ ] Ports 80, 443, 8000, 5432, 6379 available
- [ ] Domain configured (for production)
- [ ] SSL certificates ready (or use self-signed)
- [ ] WhatsApp API credentials (optional)

---

## Post-Deployment

### Verify Installation
```bash
# Health check
curl http://localhost:8000/

# API documentation
curl http://localhost:8000/api/docs

# Test diagnosis
curl -X POST http://localhost:8000/api/v1/diagnose \
  -F "image=@test.jpg" \
  -F "crop=rice" \
  -F "district=Dhaka"
```

### Configure WhatsApp Webhook
1. Go to Meta Developer Console
2. Set webhook URL: `https://your-domain/api/v1/whatsapp/webhook`
3. Verify token: `crop_health_bot`

### Setup SSL (Production)
Replace self-signed certificates:
```bash
# Using Let's Encrypt
certbot certonly --standalone -d your-domain.com

# Copy certificates
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem backend/ssl/cert.pem
cp /etc/letsencrypt/live/your-domain.com/privkey.pem backend/ssl/key.pem
```

---

## Troubleshooting

### Services not starting
```bash
# Check logs
docker-compose logs -f

# Restart specific service
docker-compose restart api
```

### Database connection failed
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# Reset database (WARNING: data loss)
docker-compose down -v
docker-compose up -d
```

### Port conflicts
```bash
# Check port usage
sudo lsof -i :8000

# Kill process using port
sudo kill -9 <PID>
```

---

## Automatic Startup

### Using systemd
```bash
# Copy service file
sudo cp crop-advisory.service /etc/systemd/system/

# Enable and start
sudo systemctl enable crop-advisory
sudo systemctl start crop-advisory

# Check status
sudo systemctl status crop-advisory
```

### Using cron
```bash
# Add to crontab
crontab -e

# Add line:
@reboot cd /path/to/crop-advisory-system && docker-compose up -d
```

---

## CI/CD Integration

### GitHub Actions
Already configured in `.github/workflows/deploy.yml`

### GitLab CI
Create `.gitlab-ci.yml`:
```yaml
stages:
  - test
  - deploy

test:
  stage: test
  script:
    - python test_system.py

deploy:
  stage: deploy
  script:
    - ./auto_deploy.py deploy
  only:
    - main
```

---

## Monitoring

### Health Endpoints
- API: `GET /`
- Database: `docker-compose exec db pg_isready`
- Redis: `docker-compose exec redis redis-cli ping`

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### Backup
```bash
# Automated
./auto_deploy.py backup

# Manual
docker-compose exec db pg_dump -U postgres crop_advisory > backup.sql
```

---

## Support

- **Technical**: DAE IT Division
- **Agricultural**: 16263 (DAE Hotline)
- **Emergency**: Upazila Agriculture Officer
