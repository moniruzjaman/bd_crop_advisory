#!/bin/bash
# ============================================================
# 🇧🇩 National AI-Enabled Crop Health Advisory System
# Universal Setup & Deployment Script
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="crop-advisory-system"
GREEN='[0;32m'
YELLOW='[1;33m'
RED='[0;31m'
BLUE='[0;34m'
NC='[0m'

print_header() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo "  🇧🇩 National AI-Enabled Crop Health Advisory System"
    echo "  Automated Deployment"
    echo "============================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Docker automatically
install_docker() {
    print_info "Docker not found. Installing Docker..."

    if command_exists apt-get; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm -f get-docker.sh
    elif command_exists yum; then
        # RHEL/CentOS
        sudo yum install -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io
        sudo systemctl start docker
        sudo systemctl enable docker
    elif command_exists brew; then
        # macOS
        brew install --cask docker
    else
        print_error "Cannot install Docker automatically. Please install manually."
        exit 1
    fi

    print_success "Docker installed successfully!"
    print_warning "You may need to log out and back in for Docker permissions to take effect."
}

# Install Docker Compose
install_docker_compose() {
    print_info "Docker Compose not found. Installing..."

    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    print_success "Docker Compose installed!"
}

# Main deployment function
deploy() {
    print_header

    cd "$SCRIPT_DIR"

    # Step 1: Check prerequisites
    print_info "Step 1: Checking prerequisites..."

    if ! command_exists docker; then
        install_docker
    else
        print_success "Docker found: $(docker --version)"
    fi

    if ! command_exists docker-compose; then
        install_docker_compose
    else
        print_success "Docker Compose found: $(docker-compose --version)"
    fi

    # Step 2: Setup environment
    print_info "Step 2: Setting up environment..."

    if [ ! -f backend/.env ]; then
        if [ -f backend/.env.example ]; then
            cp backend/.env.example backend/.env
            print_success "Created .env from example"
        fi
    fi

    # Generate secure secret key if not set
    if [ -f backend/.env ]; then
        if grep -q "your-super-secret-key" backend/.env; then
            SECRET_KEY=$(openssl rand -base64 32)
            sed -i "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" backend/.env
            print_success "Generated secure SECRET_KEY"
        fi
    fi

    # Step 3: Setup SSL
    print_info "Step 3: Setting up SSL certificates..."

    mkdir -p backend/ssl

    if [ ! -f backend/ssl/cert.pem ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048             -keyout backend/ssl/key.pem             -out backend/ssl/cert.pem             -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/CN=cropadvisory.gov.bd"             2>/dev/null || true
        print_success "Generated self-signed SSL certificates"
        print_warning "Replace with production certificates for live deployment"
    else
        print_success "SSL certificates already exist"
    fi

    # Step 4: Build and deploy
    print_info "Step 4: Building and deploying services..."

    cd backend

    # Stop existing services if running
    docker-compose down 2>/dev/null || true

    # Build images
    print_info "Building Docker images (this may take a few minutes)..."
    docker-compose build --no-cache

    # Start services
    print_info "Starting services..."
    docker-compose up -d

    # Step 5: Wait for services
    print_info "Step 5: Waiting for services to start..."
    sleep 20

    # Step 6: Health checks
    print_info "Step 6: Performing health checks..."

    # Check API
    if curl -f -s http://localhost:8000/ > /dev/null 2>&1; then
        print_success "API is responding"
    else
        print_warning "API not responding yet (may need more time)"
    fi

    # Check database
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        print_success "Database is ready"
    else
        print_warning "Database not ready yet"
    fi

    # Check Redis
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is ready"
    else
        print_warning "Redis not ready yet"
    fi

    # Step 7: Display results
    echo ""
    echo -e "${GREEN}============================================================"
    echo "  🎉 DEPLOYMENT SUCCESSFUL!"
    echo "============================================================${NC}"
    echo ""
    echo -e "${BLUE}📍 Access Points:${NC}"
    echo "   • API:          http://localhost:8000"
    echo "   • API Docs:     http://localhost:8000/api/docs"
    echo "   • WhatsApp:     http://localhost:8000/api/v1/whatsapp/webhook"
    echo ""
    echo -e "${BLUE}📁 Project Directory:${NC}"
    echo "   $SCRIPT_DIR"
    echo ""
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "   • View logs:    cd backend && docker-compose logs -f"
    echo "   • Stop:         cd backend && docker-compose down"
    echo "   • Restart:      cd backend && docker-compose restart"
    echo ""
    echo -e "${BLUE}📞 Support:${NC}"
    echo "   • DAE Hotline:  16263"
    echo "   • Email:        admin@cropadvisory.gov.bd"
    echo ""
    echo -e "${GREEN}============================================================${NC}"
}

# Stop services
stop() {
    print_info "Stopping services..."
    cd "$SCRIPT_DIR/backend"
    docker-compose down
    print_success "Services stopped"
}

# Restart services
restart() {
    stop
    sleep 5
    deploy
}

# View logs
logs() {
    cd "$SCRIPT_DIR/backend"
    if [ -n "$1" ]; then
        docker-compose logs -f "$1"
    else
        docker-compose logs -f
    fi
}

# Backup database
backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="$SCRIPT_DIR/backups"
    mkdir -p "$BACKUP_DIR"

    cd "$SCRIPT_DIR/backend"
    docker-compose exec -T db pg_dump -U postgres crop_advisory > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

    print_success "Backup created: backups/backup_$TIMESTAMP.sql"
}

# Status check
status() {
    print_header

    cd "$SCRIPT_DIR/backend"

    echo -e "${BLUE}Service Status:${NC}"
    docker-compose ps

    echo ""
    echo -e "${BLUE}Health Checks:${NC}"

    if curl -f -s http://localhost:8000/ > /dev/null 2>&1; then
        print_success "API: Running"
    else
        print_error "API: Not responding"
    fi

    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        print_success "Database: Running"
    else
        print_error "Database: Not responding"
    fi
}

# Main command handler
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "$2"
        ;;
    backup)
        backup
        ;;
    status)
        status
        ;;
    help|--help|-h)
        print_header
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy    - Deploy all services (default)"
        echo "  stop      - Stop all services"
        echo "  restart   - Restart all services"
        echo "  logs      - View logs [service_name]"
        echo "  backup    - Backup database"
        echo "  status    - Check service status"
        echo "  help      - Show this help message"
        echo ""
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
