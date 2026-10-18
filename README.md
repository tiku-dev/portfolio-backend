# 🚀 Senior Portfolio Backend (Django REST Framework)

A production-grade, architectural Django REST Framework (DRF) backend for a software engineer's portfolio. Designed to prove backend engineering competencies to hiring managers and tech leads: asynchronous jobs, dynamic PDF compilation, privacy-preserving telemetry, live status health probes, and an interactive developer CLI console.

---

## 🛠️ Tech Stack

* **Framework**: Django 5.x & Django REST Framework (DRF)
* **Database**: PostgreSQL (Production/Docker) / SQLite (Local Dev)
* **Caching & Queuing**: Redis & Celery
* **Document Engine**: ReportLab (In-memory compiled ATS-friendly PDF resume)
* **Security & Reliability**: `django-cors-headers`, Rate Throttling, Honeypot Anti-Spam
* **Testing**: Django APITestCase (16 automated tests)

---

## 📂 Modular Architecture (`/apps`)

```
backend/
├── apps/
│   ├── projects/       # Case studies, architecture components, metrics, live ping probes
│   ├── resume/         # Structured JSON resume & dynamic on-the-fly PDF compiler
│   ├── contact/        # Inquiries, honeypot spam protection, async notification dispatch
│   ├── terminal/       # Interactive hacker CLI endpoint for frontend terminal UI
│   ├── telemetry/      # Privacy-preserving visit analytics & public statistics
│   └── sync_engine/    # GitHub metrics sync & live demo uptime health probes
├── config/             # Split settings, URL router, healthcheck
├── manage.py
├── Dockerfile
└── docker-compose.yml
```

---

## ⚡ Quick Start

### 1. Activate Environment & Run Migrations
```bash
# Windows
.\venv\Scripts\activate

# Apply migrations
python manage.py migrate
```

### 2. Seed Standout Portfolio Data
Populates the database with real-world case studies, architecture notes, metrics, skills, and resume records:
```bash
python manage.py seed_portfolio
```

### 3. Sync GitHub & Probe Live Demos
Fetches real-time GitHub stars, forks, and followers, and pings live project demos:
```bash
python manage.py sync_portfolio
```

### 4. Run Automated Test Suite
```bash
python manage.py test
```

### 5. Start Development Server
```bash
python manage.py runserver
```

---

## 🌐 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/` | `GET` | API Directory & Discoverability Index |
| `/api/health/` | `GET` | Health Check (DB connectivity & uptime status) |
| `/api/v1/projects/` | `GET` | List case-study projects (Filter by `?tags__slug=` or `?featured=true`) |
| `/api/v1/projects/<slug>/` | `GET` | Retrieve complete project case study & architecture breakdown |
| `/api/v1/projects/<slug>/ping/` | `GET` | Real-time health probe (pings live demo & reports latency in ms) |
| `/api/v1/projects/tags/` | `GET` | List technical skill tags categorized |
| `/api/v1/resume/` | `GET` | Full structured resume data (JSON) |
| `/api/v1/resume/pdf/` | `GET` | **Dynamic PDF resume generator** (Supports `?focus=backend` or `?focus=devops`) |
| `/api/v1/terminal/execute/` | `POST` | **Developer CLI Console** (Executes simulated terminal commands) |
| `/api/v1/contact/` | `POST` | Contact submission with honeypot spam detection & async notifications |
| `/api/v1/telemetry/stats/` | `GET` | Public telemetry dashboard (total requests, avg latency, uptime) |
| `/api/v1/telemetry/track/` | `POST` | Records frontend interactions (e.g. project demo clicks) |
| `/api/v1/sync/github/` | `GET` | Returns live/cached GitHub profile and repo statistics |

---

## 💻 Interactive Developer Terminal API

Frontend terminal components can send command strings to `POST /api/v1/terminal/execute/`:

```json
// Request
{
  "command": "skills --tree"
}

// Response
{
  "output": "└── Core Competencies\n    ├── BACKEND\n    │   ├── Django\n    │   └── Python\n    └── DATABASE\n        ├── PostgreSQL\n        └── Redis",
  "status": "ok"
}
```

Supported commands:
* `help` &mdash; Show developer manual
* `whoami` &mdash; Display engineer profile & availability
* `skills [--tree | --category=<cat>]` &mdash; Render skills as ASCII tree or table
* `projects [--tag=<slug>]` &mdash; List projects, live status, and repository stars
* `cat project <slug>` &mdash; Print deep-dive architecture breakdown
* `cat experience` &mdash; Print employment timeline
* `ping <slug>` &mdash; Real-time probe of project demo URL with latency report
* `contact <name> <email> <msg>` &mdash; Dispatch contact inquiry directly from the terminal
* `uptime` &mdash; Show system uptime and active services

---

## 🐳 Running with Docker Compose

```bash
docker compose up --build
```
This spins up:
- **Django API**: `http://localhost:8000`
- **PostgreSQL 16**: Port `5432`
- **Redis 7**: Port `6379`

