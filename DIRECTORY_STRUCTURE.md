# Project Directory Structure

This document outlines the organized directory structure of the MWECAU ICT Club project.

## Root Level

```
mwecau_ict/
├── docs/              # All project documentation
├── public/            # Public assets and examples
├── scripts/           # Utility scripts and configuration files
├── src/               # Django application source code
├── README.md          # Main project README
└── .gitignore         # Git ignore rules
```

## Directory Details

### `docs/` - Documentation
Complete project documentation organized by purpose:

```
docs/
├── setup/             # Setup and deployment configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── DOCKER_GUIDE.md
│   ├── DOCKER_SETUP_SUMMARY.md
│   └── requirements.txt
├── deployment/        # Deployment guides and checklists
│   └── DEPLOYMENT_READY.md
├── guides/            # Feature-specific guides
│   ├── EMAIL_SYSTEM_GUIDE.md
│   └── EMAIL_SYSTEM_COMPLETE.md
├── api/               # API documentation (reserved for future use)
├── CHANGELOG.md       # Version history and release notes
├── CODE_OF_CONDUCT.md # Community standards
├── CONTRIBUTING.md    # Contribution guidelines
├── FEATURES_IMPLEMENTATION_AUDIT.md  # Feature status
├── PROJECT_STATUS.txt # Overall project status
└── USERS.md           # User and role documentation
```

### `public/` - Public Assets
Public files and templates:

```
public/
├── .env.example       # Environment variables template
└── [images/assets]    # Public images and design assets
```

### `scripts/` - Utility Scripts & Configuration
Automation scripts and environment configuration:

```
scripts/
├── EMAIL_QUICK_REFERENCE.sh  # Email system quick reference
├── tests_email.py            # Email testing script
├── .env                       # Development environment (gitignored)
├── .env.dev                   # Development config (gitignored)
├── .env.docker                # Docker environment config (gitignored)
└── .env.prod                  # Production config (gitignored)
```

### `src/` - Django Application
Main Django project source code:

```
src/
├── config/            # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/          # User authentication and management
├── core/              # Core application features
├── membership/        # Membership and payments
├── templates/         # HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── core/
│   └── emails/       # Email templates
├── static/            # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── staticfiles/       # Collected static files (production)
├── manage.py          # Django management command
└── db.sqlite3         # Development database
```

## How to Use New Structure

### Installation & Running
```bash
# Install dependencies from the new location
pip install -r docs/setup/requirements.txt

# Environment configuration
cp public/.env.example scripts/.env
nano scripts/.env

# Docker deployment
docker-compose -f docs/setup/docker-compose.yml build
docker-compose -f docs/setup/docker-compose.yml up -d
```

### Documentation Navigation
- **Getting Started**: See [README.md](../README.md)
- **Contributing**: See [docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md)
- **Docker Setup**: See [docs/setup/DOCKER_GUIDE.md](../docs/setup/DOCKER_GUIDE.md)
- **Deployment**: See [docs/deployment/DEPLOYMENT_READY.md](../docs/deployment/DEPLOYMENT_READY.md)
- **Email System**: See [docs/guides/EMAIL_SYSTEM_GUIDE.md](../docs/guides/EMAIL_SYSTEM_GUIDE.md)

## Benefits of This Structure

1. **Clear Organization**: Documentation, scripts, and assets are logically separated
2. **Easy Navigation**: New contributors can quickly find relevant information
3. **Clean Root**: Reduces clutter at project root level
4. **Professional Layout**: Follows Django best practices for project structure
5. **Scalability**: Easy to add new documentation or features as project grows

---

*Last updated: December 14, 2025*
