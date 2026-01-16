# Movie Hub — Client‑Server Movie Streaming & Recommendations

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/pytest-passing-0A9EDC?logo=pytest&logoColor=white)
![OAuth](https://img.shields.io/badge/OAuth2-GitHub-181717?logo=github&logoColor=white)

A modern Flask + PostgreSQL client‑server web app that lets users browse a movie catalog, open a movie page with an embedded player, and get a quick “What to watch?” recommendation.  
Includes an admin panel (password-protected) to manage movies and upload video files, plus optional GitHub OAuth 2.0 login.

---

## Features

- Modern UI (cards grid, background wallpaper, responsive layout)
- Movie catalog: title, short description with ellipsis, rating, “Watch now”
- Movie page: HTML5 video player (plays uploaded .mp4/.webm/.ogg)
- Recommendations: “What to watch?” button (top-rated first)
- Admin panel (/admin/login, password: 3333)
  - Create movies
  - Upload a video file (stored under /static/videos/)
  - Or set a direct video_url
- REST API for movies & recommendations
- Database via SQLAlchemy (PostgreSQL in Docker Compose)
- Logging with Flask app.logger (visible via Docker logs)
- Unit + Integration tests via pytest
- CI/CD ready via GitHub Actions + Railway (per course checkpoint)

---

## Architecture (high level)

- Frontend: HTML templates + CSS + vanilla JS (static/js/main.js, static/js/admin.js)
- Backend: Flask routes render pages + JSON API
- DB: PostgreSQL stores movies (title/genre/year/rating/description/video_url)
- Uploads: admin can upload video files -> saved to backend/static/videos/

Typical flow:
1. Home page loads -> JS calls GET /api/movies -> renders movie cards.
2. “What to watch?” -> JS calls GET /api/recommendations -> shows a modal with a pick.
3. “Watch now” -> opens /movie/<id> -> HTML renders <video src=...>.

---

## Grading criteria mapping (important)

This project is built to satisfy the course checkpoints.

### Checkpoint 14.11.2025 (max 35 pts)
- README.md actual & complete (this file)
- Docker (Dockerfile + docker-compose.yml)
- CI/CD (GitHub Actions for build/run/route checks + Railway deployment)
- Simple server + client (Flask route(s) + browser client + requests checks in CI)

### Checkpoint 16.12.2025 (max 65 pts)
- Routes & features
  - Web pages + API routes (see below)
  - Features described here match implementation
- Database
  - PostgreSQL + SQLAlchemy (flask_sqlalchemy)
- Tests
  - 2+ unit tests (validation, error handling)
  - 2+ integration tests (API create/retrieve/update/delete)
- Logger
  - Flask app.logger with structured output
- Authorization using OAuth 2.0 (extra points)
  - GitHub OAuth 2.0 login (optional, can be disabled if env vars not set)
- Docker Compose
  - DB and web server as separate containers
  - connection params via environment variables
- Deployed using Docker
  - Designed to deploy to Railway (or any Docker host)

Notes:
- If a grader runs the app in Docker and the described features work, you are in the “Routes” bracket for the checkpoint.
- OAuth 2.0 is an extra task.

---

## Quick start (Docker Compose)

### 1) Create .env file
In project root (same folder as docker-compose.yml), create .env:

```env
# Flask
SECRET_KEY=change_me_in_real_life
LOG_LEVEL=INFO

# Database (Docker Compose)
POSTGRES_DB=movies
POSTGRES_USER=movies_user
POSTGRES_PASSWORD=movies_pass
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://movies_user:movies_pass@db:5432/movies

# Optional: GitHub OAuth 2.0 (see OAuth section)
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

### 2) Build & run
```bash
docker compose up -d --build
```

Open:
- App: http://localhost:8080
- Admin login: http://localhost:8080/admin/login

### 3) Stop
```bash
docker compose down
```

---

## Running tests

Run all tests inside the web container:

```bash
docker compose exec web pytest -q
```

Run only unit tests:
```bash
docker compose exec web pytest -q tests/unit
```

Run only integration tests:
```bash
docker compose exec web pytest -q tests/integration
```

Why PYTHONPATH=/app exists:
Pytest imports backend.*. In Docker we set PYTHONPATH=/app so Python can always find the backend/ package.

---

## Logging

The app uses app.logger and writes to stdout. Docker captures stdout, so logs are accessible via:

```bash
docker compose logs -f web
```

Example:
```
INFO backend.server.server: 127.0.0.1 GET /api/movies
```

---

## Admin panel (movie management + upload)

- URL: /admin/login
- Password: 3333
- Admin can:
  - create a movie (title/genre/year/rating/description)
  - optionally upload video (.mp4, .webm, .ogg)
  - or set video_url manually

Uploaded videos are saved to:
- backend/static/videos/<uuid>.<ext>
and become available via:
- /static/videos/<uuid>.<ext>

---

## Video URLs: what works

The HTML5 video tag expects a direct file URL it can stream, not a YouTube page link.

Works:
- /static/videos/my_movie.mp4
- https://example.com/video.mp4 (direct file)
- https://cdn.example.com/movie.webm

Does not work:
- https://youtube.com/watch?v=... (not a direct stream URL)

Best option: upload through the admin panel, and the app will auto-set video_url.

---

## GitHub OAuth 2.0 (optional)

OAuth is optional. If GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET are empty, the app will still run, but “Login” will redirect back to home.

### Create a GitHub OAuth App
1. GitHub -> Settings -> Developer settings -> OAuth Apps -> New OAuth App
2. Fill:
   - Homepage URL: http://localhost:8080
   - Authorization callback URL: http://localhost:8080/authorize
3. Copy Client ID and Client Secret into .env:
   - GITHUB_CLIENT_ID=...
   - GITHUB_CLIENT_SECRET=...
4. Restart:
```bash
docker compose up -d --build
```

---

## API endpoints

Public:
- GET /api/movies -> list movies
- GET /api/movies/<id> -> get one movie
- GET /api/recommendations?limit=5 -> top picks (sorted by rating)

Admin-protected (in normal mode):
- POST /api/movies -> create movie (JSON or multipart with video_file)
- PUT /api/movies/<id> -> update movie (JSON)
- DELETE /api/movies/<id> -> delete movie

In test mode (app.config["TESTING"]=True) the admin restriction is disabled to allow automated tests to validate API behaviors.

---

## Tech stack

- Backend: Python 3.11, Flask
- DB: PostgreSQL 15, SQLAlchemy (flask_sqlalchemy)
- Auth: GitHub OAuth 2.0 (Authlib)
- Frontend: Jinja templates + CSS + Vanilla JS (AJAX via fetch)
- Testing: Pytest (unit + integration)
- Containerization: Docker + Docker Compose
- CI/CD: GitHub Actions + Railway deployment

---

## Troubleshooting

Service web is not running:
```bash
docker compose logs -f web
```

Postgres error: role "-d" does not exist:
Use $$POSTGRES_USER in docker-compose.yml healthcheck:
```yaml
test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
```

Browser cache doesn’t update styles/scripts:
Hard refresh: Cmd + Shift + R

Docker Compose warns: attribute version is obsolete:
Remove the version: line from docker-compose.yml. It is harmless.

---

## Deployment (Railway)

This project is designed to be deployable on Railway using Docker.

General steps:
1. Push repo to GitHub
2. Create Railway project from GitHub repo
3. Add environment variables in Railway
4. Ensure services:
   - web (Flask)
   - db (Postgres) or Railway Postgres plugin
5. Railway will build and run Docker image

---

## License

Educational project for the course.
