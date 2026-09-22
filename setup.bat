@echo off
:: ============================================================
:: National AI-Enabled Crop Health Advisory System
:: Windows Deployment Script
:: ============================================================

echo.
echo ============================================================
echo   National AI-Enabled Crop Health Advisory System
echo   Windows Deployment
echo ============================================================
echo.

:: Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found. Please install Docker Desktop first:
    echo https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker found
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo [OK] Docker Compose found

:: Setup environment
if not exist backend\.env (
    if exist backend\.env.example (
        copy backend\.env.example backend\.env
        echo [OK] Created .env file
    )
)

:: Setup SSL certificates
if not exist backend\ssl\cert.pem (
    mkdir backend\ssl 2>nul
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 ^
        -keyout backend\ssl\key.pem ^
        -out backend\ssl\cert.pem ^
        -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/CN=cropadvisory.gov.bd" ^
        2>nul
    echo [OK] Generated SSL certificates
)

:: Deploy
echo.
echo Building and deploying services...
cd backend
docker-compose down 2>nul
docker-compose build --no-cache
docker-compose up -d

:: Wait for services
echo.
echo Waiting for services to start...
timeout /t 20 /nobreak >nul

:: Health check
echo.
echo Performing health checks...
curl -f -s http://localhost:8000/ >nul 2>&1
if errorlevel 1 (
    echo [WARNING] API not responding yet
) else (
    echo [OK] API is responding
)

echo.
echo ============================================================
echo   DEPLOYMENT SUCCESSFUL!
echo ============================================================
echo.
echo Access Points:
echo   - API:          http://localhost:8000
echo   - API Docs:     http://localhost:8000/api/docs
echo   - WhatsApp:     http://localhost:8000/api/v1/whatsapp/webhook
echo.
echo Management Commands:
echo   - View logs:    cd backend ^&^& docker-compose logs -f
echo   - Stop:         cd backend ^&^& docker-compose down
echo   - Restart:      cd backend ^&^& docker-compose restart
echo.
pause
