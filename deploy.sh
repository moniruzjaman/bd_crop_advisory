#!/bin/bash

# National Crop Health Advisory System Deployment Script
# Bangladesh Government Grade Deployment

set -e

echo "🇧🇩 Starting National Crop Health Advisory System Deployment..."

# Configuration
PROJECT_NAME="crop-advisory-system"
BACKEND_DIR="backend"
DOMAIN="api.cropadvisory.gov.bd"
EMAIL="admin@cropadvisory.gov.bd"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    command -v docker >/dev/null 2>&1 || { log_error "Docker not installed. Aborting."; exit 1; }
    command -v docker-compose >/dev/null 2>&1 || { log_error "Docker Compose not installed. Aborting."; exit 1; }

    log_info "Prerequisites check passed ✓"
}

# Setup SSL certificates
setup_ssl() {
    log_info "Setting up SSL certificates..."

    mkdir -p backend/ssl

    # For production, use Let's Encrypt
    # certbot certonly --standalone -d $DOMAIN --email $EMAIL --agree-tos --non-interactive

    # For development, generate self-signed
    openssl req -x509 -nodes -days 365 -newkey rsa:2048         -keyout backend/ssl/key.pem         -out backend/ssl/cert.pem         -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/OU=IT/CN=$DOMAIN"

    log_info "SSL certificates generated ✓"
}

# Create environment file
setup_environment() {
    log_info "Setting up environment..."

    if [ ! -f backend/.env ]; then
        cp backend/.env.example backend/.env
        log_warn "Created .env from example. Please update with production values!"
    fi

    # Create necessary directories
    mkdir -p backend/uploads
    mkdir -p backend/models
    mkdir -p backend/logs

    log_info "Environment setup complete ✓"
}

# Build and deploy
build_and_deploy() {
    log_info "Building Docker images..."

    cd backend

    # Build images
    docker-compose build --no-cache

    log_info "Starting services..."

    # Start services
    docker-compose up -d

    # Wait for database
    log_info "Waiting for database to be ready..."
    sleep 10

    # Run migrations
    docker-compose exec -T api alembic upgrade head || log_warn "Migration skipped or failed"

    cd ..

    log_info "Deployment complete ✓"
}

# Health check
health_check() {
    log_info "Performing health checks..."

    # Check API
    if curl -f -s http://localhost:8000/ > /dev/null; then
        log_info "API is responding ✓"
    else
        log_error "API is not responding"
        exit 1
    fi

    # Check database
    if docker-compose -f backend/docker-compose.yml exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        log_info "Database is ready ✓"
    else
        log_error "Database is not ready"
        exit 1
    fi

    log_info "All health checks passed ✓"
}

# Monitoring setup
setup_monitoring() {
    log_info "Setting up monitoring..."

    # Create prometheus config
    cat > backend/prometheus.yml <<EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'crop-advisory-api'
    static_configs:
      - targets: ['api:8000']
EOF

    log_info "Monitoring configuration created ✓"
}

# Backup function
backup_database() {
    log_info "Creating database backup..."

    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="backups"

    mkdir -p $BACKUP_DIR

    docker-compose -f backend/docker-compose.yml exec -T db         pg_dump -U postgres crop_advisory > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

    log_info "Backup created: backups/backup_$TIMESTAMP.sql"
}

# Main deployment flow
deploy() {
    check_prerequisites
    setup_ssl
    setup_environment
    build_and_deploy
    health_check
    setup_monitoring

    log_info "==================================="
    log_info "🎉 Deployment Successful!"
    log_info "==================================="
    log_info "API URL: https://$DOMAIN"
    log_info "API Docs: https://$DOMAIN/api/docs"
    log_info "WhatsApp Webhook: https://$DOMAIN/api/v1/whatsapp/webhook"
    log_info "==================================="
}

# Command handling
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    backup)
        backup_database
        ;;
    update)
        log_info "Updating deployment..."
        cd backend
        docker-compose pull
        docker-compose up -d
        cd ..
        health_check
        ;;
    stop)
        log_info "Stopping services..."
        cd backend
        docker-compose down
        cd ..
        ;;
    logs)
        cd backend
        docker-compose logs -f
        ;;
    *)
        echo "Usage: $0 {deploy|backup|update|stop|logs}"
        exit 1
        ;;
esac
