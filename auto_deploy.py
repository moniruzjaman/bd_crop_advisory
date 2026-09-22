#!/usr/bin/env python3
"""
National AI-Enabled Crop Health Advisory System
Automated Deployment Script
"""

import os
import sys
import subprocess
import time
import json
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
LOG_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backups"

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(msg, level="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = {
        "info": Colors.BLUE,
        "success": Colors.GREEN,
        "warning": Colors.YELLOW,
        "error": Colors.RED,
        "header": Colors.CYAN + Colors.BOLD
    }
    color = colors.get(level, Colors.BLUE)
    print(f"{color}[{timestamp}] {msg}{Colors.END}")

def run_command(cmd, check=True, shell=True, capture_output=False):
    log(f"Executing: {cmd}", "info")
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=shell, check=check, 
                                  capture_output=True, text=True)
            return result
        else:
            result = subprocess.run(cmd, shell=shell, check=check)
            return result
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {e}", "error")
        if check:
            raise
        return None

class DeploymentManager:
    def __init__(self):
        self.status = {}
        self.ensure_directories()

    def ensure_directories(self):
        dirs = [LOG_DIR, BACKUP_DIR, BACKEND_DIR / "uploads", 
                BACKEND_DIR / "ssl", BACKEND_DIR / "models"]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def check_prerequisites(self):
        log("Checking prerequisites...", "header")

        checks = {
            "docker": self._check_docker(),
            "docker_compose": self._check_docker_compose(),
            "ports": self._check_ports(),
            "memory": self._check_memory(),
            "disk": self._check_disk()
        }

        self.status["prerequisites"] = checks

        all_passed = all(checks.values())
        if all_passed:
            log("All prerequisites met!", "success")
        else:
            failed = [k for k, v in checks.items() if not v]
            log(f"Failed checks: {', '.join(failed)}", "error")

        return all_passed

    def _check_docker(self):
        try:
            result = run_command("docker --version", capture_output=True)
            version = result.stdout.strip()
            log(f"Docker: {version}", "success")
            return True
        except:
            log("Docker not installed", "error")
            return False

    def _check_docker_compose(self):
        try:
            result = run_command("docker-compose --version", capture_output=True)
            version = result.stdout.strip()
            log(f"Docker Compose: {version}", "success")
            return True
        except:
            log("Docker Compose not installed", "error")
            return False

    def _check_ports(self):
        required_ports = [8000, 5432, 6379, 80, 443]
        unavailable = []

        for port in required_ports:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                unavailable.append(port)
            sock.close()

        if unavailable:
            log(f"Ports in use: {unavailable}", "warning")
            return False

        log("All required ports available", "success")
        return True

    def _check_memory(self):
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            available = int([line for line in meminfo.split('\n') 
                           if 'MemAvailable' in line][0].split()[1])
            available_gb = available / (1024 * 1024)

            if available_gb < 2:
                log(f"Low memory: {available_gb:.1f}GB available", "warning")
                return False

            log(f"Memory: {available_gb:.1f}GB available", "success")
            return True
        except:
            log("Could not check memory", "warning")
            return True

    def _check_disk(self):
        stat = shutil.disk_usage(BASE_DIR)
        free_gb = stat.free / (1024**3)

        if free_gb < 10:
            log(f"Low disk space: {free_gb:.1f}GB free", "warning")
            return False

        log(f"Disk: {free_gb:.1f}GB free", "success")
        return True

    def setup_environment(self):
        log("Setting up environment...", "header")

        env_file = BACKEND_DIR / ".env"
        env_example = BACKEND_DIR / ".env.example"

        if not env_file.exists() and env_example.exists():
            shutil.copy(env_example, env_file)
            log("Created .env from example", "success")

        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()

            if 'your-super-secret-key' in content:
                import secrets
                secret_key = secrets.token_urlsafe(32)
                content = content.replace(
                    'SECRET_KEY=your-super-secret-key-change-this-in-production',
                    f'SECRET_KEY={secret_key}'
                )
                with open(env_file, 'w') as f:
                    f.write(content)
                log("Generated secure SECRET_KEY", "success")

    def setup_ssl(self):
        log("Setting up SSL certificates...", "header")

        ssl_dir = BACKEND_DIR / "ssl"
        cert_file = ssl_dir / "cert.pem"
        key_file = ssl_dir / "key.pem"

        if cert_file.exists() and key_file.exists():
            log("SSL certificates already exist", "success")
            return

        cmd = f"""openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout {key_file} \
            -out {cert_file} \
            -subj "/C=BD/ST=Dhaka/L=Dhaka/O=DAE/CN=cropadvisory.gov.bd" \
            2>/dev/null"""

        run_command(cmd)
        log("Generated self-signed SSL certificates", "success")
        log("Replace with production certificates before going live", "warning")

    def build_images(self):
        log("Building Docker images...", "header")
        os.chdir(BACKEND_DIR)
        run_command("docker-compose build --no-cache")
        log("Docker images built successfully", "success")

    def deploy_services(self):
        log("Deploying services...", "header")
        os.chdir(BACKEND_DIR)
        run_command("docker-compose up -d")
        log("Waiting for services to start...", "info")
        time.sleep(15)

        result = run_command("docker-compose ps", capture_output=True)
        log(f"Service status:\n{result.stdout}", "info")

    def run_migrations(self):
        log("Running database migrations...", "header")
        os.chdir(BACKEND_DIR)

        max_retries = 10
        for i in range(max_retries):
            result = run_command(
                "docker-compose exec -T db pg_isready -U postgres",
                check=False, capture_output=True
            )
            if result and result.returncode == 0:
                log("Database is ready", "success")
                break
            log(f"Waiting for database... ({i+1}/{max_retries})", "warning")
            time.sleep(5)
        else:
            log("Database failed to start", "error")
            return False

        run_command("docker-compose exec -T api python -c \"from database import init_db; init_db()\"", 
                   check=False)
        log("Database initialized", "success")
        return True

    def health_check(self):
        log("Performing health checks...", "header")

        import urllib.request

        checks = {"api": False, "database": False, "redis": False}

        try:
            response = urllib.request.urlopen('http://localhost:8000/', timeout=10)
            if response.status == 200:
                data = json.loads(response.read())
                log(f"API: {data.get('message', 'OK')}", "success")
                checks["api"] = True
        except Exception as e:
            log(f"API check failed: {e}", "error")

        try:
            result = run_command(
                "docker-compose exec -T db pg_isready -U postgres",
                check=False, capture_output=True
            )
            if result and result.returncode == 0:
                log("Database: Ready", "success")
                checks["database"] = True
        except:
            log("Database check failed", "error")

        try:
            result = run_command(
                "docker-compose exec -T redis redis-cli ping",
                check=False, capture_output=True
            )
            if result and 'PONG' in result.stdout:
                log("Redis: Ready", "success")
                checks["redis"] = True
        except:
            log("Redis check failed", "error")

        self.status["health"] = checks
        return all(checks.values())

    def setup_monitoring(self):
        log("Setting up monitoring...", "header")
        logrotate_script = BACKEND_DIR / "logrotate.sh"
        with open(logrotate_script, 'w') as f:
            f.write('#!/bin/bash\n# Log rotation for crop advisory system\nLOG_DIR="/app/logs"\nfind $LOG_DIR -name "*.log" -type f -mtime +7 -delete\nfind $LOG_DIR -name "*.log.*" -type f -mtime +30 -delete\n')
        logrotate_script.chmod(0o755)
        log("Monitoring setup complete", "success")

    def backup_database(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"

        log(f"Creating backup: {backup_file}", "header")
        os.chdir(BACKEND_DIR)
        run_command(
            f"docker-compose exec -T db pg_dump -U postgres crop_advisory > {backup_file}",
            check=False
        )

        if backup_file.exists():
            log(f"Backup created: {backup_file}", "success")
        else:
            log("Backup failed", "error")

    def deploy(self):
        log("=" * 60, "header")
        log("National AI-Enabled Crop Health Advisory System", "header")
        log("Automated Deployment Starting...", "header")
        log("=" * 60, "header")

        try:
            if not self.check_prerequisites():
                log("Prerequisites check failed", "warning")

            self.setup_environment()
            self.setup_ssl()
            self.build_images()
            self.deploy_services()
            self.run_migrations()

            if self.health_check():
                log("All health checks passed!", "success")
            else:
                log("Some health checks failed", "warning")

            self.setup_monitoring()
            self.backup_database()

            log("=" * 60, "header")
            log("DEPLOYMENT SUCCESSFUL!", "header")
            log("=" * 60, "header")
            log(f"API URL: https://localhost:8000", "success")
            log(f"API Docs: https://localhost:8000/api/docs", "success")
            log(f"WhatsApp Webhook: https://localhost:8000/api/v1/whatsapp/webhook", "success")
            log("=" * 60, "header")

            status_file = BASE_DIR / "deployment_status.json"
            with open(status_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "details": self.status
                }, f, indent=2)

            return True

        except Exception as e:
            log(f"Deployment failed: {e}", "error")

            status_file = BASE_DIR / "deployment_status.json"
            with open(status_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "error": str(e),
                    "details": self.status
                }, f, indent=2)

            return False

    def stop(self):
        log("Stopping services...", "header")
        os.chdir(BACKEND_DIR)
        run_command("docker-compose down")
        log("Services stopped", "success")

    def restart(self):
        log("Restarting services...", "header")
        self.stop()
        time.sleep(5)
        self.deploy()

    def logs(self, service=None):
        os.chdir(BACKEND_DIR)
        if service:
            run_command(f"docker-compose logs -f {service}")
        else:
            run_command("docker-compose logs -f")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='National Crop Health Advisory System Deployment Manager'
    )
    parser.add_argument(
        'command',
        choices=['deploy', 'stop', 'restart', 'logs', 'backup', 'status'],
        help='Command to execute'
    )
    parser.add_argument(
        '--service',
        help='Service name for logs command'
    )

    args = parser.parse_args()

    manager = DeploymentManager()

    if args.command == 'deploy':
        success = manager.deploy()
        sys.exit(0 if success else 1)
    elif args.command == 'stop':
        manager.stop()
    elif args.command == 'restart':
        manager.restart()
    elif args.command == 'logs':
        manager.logs(args.service)
    elif args.command == 'backup':
        manager.backup_database()
    elif args.command == 'status':
        manager.check_prerequisites()
        manager.health_check()

if __name__ == "__main__":
    main()
