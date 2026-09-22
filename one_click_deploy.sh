#!/bin/bash
# One-Click Deployment for National Crop Health Advisory System
# Usage: ./one_click_deploy.sh

set -e

echo "🇧🇩 National AI-Enabled Crop Health Advisory System"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Note: Running without root. Some features may be limited.${NC}"
fi

# Step 1: Check Docker
echo "🔍 Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker found: $(docker --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Docker not found. Installing...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo -e "${GREEN}✅ Docker installed${NC}"
fi

# Step 2: Check Docker Compose
echo ""
echo "🔍 Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose found: $(docker-compose --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Docker Compose not found. Installing...${NC}"
    apt-get install -y docker-compose-plugin || pip install docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
fi

# Step 3: Setup environment
echo ""
echo "🔧 Setting up environment..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

# Step 4: Generate SSL certificates
echo ""
echo "🔒 Setting up SSL certificates..."
if [ ! -f backend/ssl/cert.pem ]; then
    mkdir -p backend/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048         -keyout backend/ssl/key.pem         -out backend/ssl/cert.pem         -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/CN=cropadvisory.gov.bd"         2>/dev/null
    echo -e "${GREEN}✅ SSL certificates generated${NC}"
else
    echo -e "${GREEN}✅ SSL certificates already exist${NC}"
fi

# Step 5: Build and deploy
echo ""
echo "🚀 Building and deploying services..."
cd backend
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

# Step 6: Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 20

# Step 7: Health check
echo ""
echo "🏥 Performing health checks..."

# Check API
if curl -f -s http://localhost:8000/ > /dev/null; then
    echo -e "${GREEN}✅ API is responding${NC}"
else
    echo -e "${YELLOW}⚠️  API not responding yet (may need more time)${NC}"
fi

# Check database
if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database is ready${NC}"
else
    echo -e "${YELLOW}⚠️  Database not ready yet${NC}"
fi

# Step 8: Display information
echo ""
echo "=================================================="
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo "=================================================="
echo ""
echo "📍 Access Points:"
echo "   • API:          http://localhost:8000"
echo "   • API Docs:     http://localhost:8000/api/docs"
echo "   • WhatsApp:     http://localhost:8000/api/v1/whatsapp/webhook"
echo ""
echo "📁 Project Directory: $(pwd)"
echo ""
echo "🔧 Management Commands:"
echo "   • View logs:    docker-compose logs -f"
echo "   • Stop:         docker-compose down"
echo "   • Restart:      docker-compose restart"
echo ""
echo "📞 Support:"
echo "   • DAE Hotline:  16263"
echo "   • Email:        admin@cropadvisory.gov.bd"
echo ""
echo "=================================================="
