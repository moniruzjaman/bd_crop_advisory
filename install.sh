#!/bin/bash
# 🇧🇩 National Crop Health Advisory System - Deployment Guide
# Run this script for interactive deployment

echo "=========================================="
echo "🇧🇩 BANGLADESH CROP ADVISORY SYSTEM"
echo "Interactive Deployment Guide"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker installed"
        docker --version
    else
        echo -e "${RED}✗${NC} Docker not found. Please install Docker first."
        echo "  Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker Compose installed"
        docker-compose --version
    else
        echo -e "${RED}✗${NC} Docker Compose not found."
        exit 1
    fi
}

# Setup environment
setup_env() {
    echo ""
    echo "Step 1: Environment Configuration"
    echo "-----------------------------------"

    if [ ! -f backend/.env ]; then
        echo "Creating .env file from template..."
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}!${NC} Please edit backend/.env with your actual credentials"
        echo "  Required: SECRET_KEY, DATABASE_URL, WHATSAPP_TOKEN"
    else
        echo -e "${GREEN}✓${NC} .env file already exists"
    fi
}

# SSL Setup
setup_ssl() {
    echo ""
    echo "Step 2: SSL Certificate Setup"
    echo "-------------------------------"

    mkdir -p backend/ssl

    if [ ! -f backend/ssl/cert.pem ]; then
        echo "Generating self-signed SSL certificate..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048             -keyout backend/ssl/key.pem             -out backend/ssl/cert.pem             -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/OU=IT/CN=api.cropadvisory.gov.bd"
        echo -e "${GREEN}✓${NC} SSL certificates generated"
        echo -e "${YELLOW}!${NC} For production, replace with Let's Encrypt or official certificates"
    else
        echo -e "${GREEN}✓${NC} SSL certificates already exist"
    fi
}

# Build and deploy
deploy() {
    echo ""
    echo "Step 3: Building & Deploying Services"
    echo "----------------------------------------"

    cd backend

    echo "Pulling latest images..."
    docker-compose pull

    echo "Building services..."
    docker-compose build --no-cache

    echo "Starting services..."
    docker-compose up -d

    echo "Waiting for database..."
    sleep 15

    echo "Running database migrations..."
    docker-compose exec -T api python -c "from database import init_db; init_db()" || echo "Migration skipped"

    cd ..
    echo -e "${GREEN}✓${NC} Deployment complete!"
}

# Health check
health_check() {
    echo ""
    echo "Step 4: Health Check"
    echo "---------------------"

    # Check API
    if curl -s http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}✓${NC} API is running on http://localhost:8000"
    else
        echo -e "${RED}✗${NC} API not responding"
    fi

    # Check services
    cd backend
    docker-compose ps
    cd ..
}

# Show access info
show_info() {
    echo ""
    echo "=========================================="
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "Access Points:"
    echo "  • API Docs:    http://localhost:8000/api/docs"
    echo "  • API Root:    http://localhost:8000/"
    echo "  • WhatsApp:    http://localhost:8000/api/v1/whatsapp/webhook"
    echo ""
    echo "Services:"
    echo "  • API Server:  http://localhost:8000"
    echo "  • Database:    localhost:5432"
    echo "  • Redis:       localhost:6379"
    echo ""
    echo "Commands:"
    echo "  • View logs:   cd backend && docker-compose logs -f"
    echo "  • Stop:        cd backend && docker-compose down"
    echo "  • Restart:     cd backend && docker-compose restart"
    echo ""
    echo "=========================================="
}

# Main menu
main() {
    check_docker
    setup_env
    setup_ssl
    deploy
    health_check
    show_info
}

# Run
main
