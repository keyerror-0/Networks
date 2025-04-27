```markdown
# URL Storage Application

A web application for storing and managing URLs using Flask and PostgreSQL, deployed via Docker containers.

## Features

- 🐳 **Dockerized Architecture**:
  - `web` - Flask application (port 5000)
  - `db` - PostgreSQL 13 database
- 🌐 **Custom Docker Network** for inter-container communication
- 🔐 **Environment Variable Security** with `.env` file
- 🔄 **Automatic Database Initialization**
- 📦 **Migrations Support** with Flask-Migrate

## Prerequisites

- Docker 20.10+
- Git 2.25+

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo/lab5
```

### 2. Install Docker
[Official Docker Installation Guide](https://docs.docker.com/get-docker/)

### 3. Configure Environment
Create `.env` file:
```bash
cp .env.example .env
nano .env  # or your preferred editor
```

Populate with your values:
```env
# PostgreSQL Configuration
DB_USER=your_db_user
DB_PASSWORD=your_strong_password
DB_NAME=url_storage
DB_HOST=db
DB_PORT=5432

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key
```

## Running the Application
```bash
# Make scripts executable
chmod +x *.sh

# Start containers
./start.sh
```
Access application at: [http://localhost:5000](http://localhost:5000)

## Stopping the Application
```bash
./stop.sh
```

## Troubleshooting

### Permission Issues
```bash
sudo chmod +x *.sh  # Linux/MacOS
```

### Line Ending Conflicts (Windows/WSL)
```bash
sudo apt-get install dos2unix && dos2unix start.sh
```

### Port Conflicts
1. Modify in `.env`:
```env
FLASK_RUN_PORT=5001
```
2. Update Docker commands:
```bash
-p 5001:5001
```

### Database Migrations
```bash
docker exec -it web flask db upgrade
```

### Container Connectivity Issues
Verify network configuration:
```bash
docker network inspect app-net
```
