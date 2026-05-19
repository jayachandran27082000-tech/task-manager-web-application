# TaskFlow — FastAPI Task Manager

A full-stack task management application with JWT authentication, built with FastAPI and vanilla JavaScript.

**Live Demo:** `https://your-deployment-url.onrender.com`  
**API Docs:** `https://your-deployment-url.onrender.com/docs`

---

## Features

- **JWT Authentication** — register, login, secure token-based access
- **Full Task CRUD** — create, view, update, delete tasks
- **Completion Toggle** — mark tasks done/undone
- **Filtering** — filter by completed / pending status
- **Pagination** — server-side, configurable page size
- **User Isolation** — users only ever see their own tasks
- **Interactive API Docs** — auto-generated Swagger UI at `/docs`
- **Dockerized** — single `docker-compose up` to run locally
- **Test Suite** — pytest coverage for auth and task endpoints

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic settings (env vars)
│   │   │   └── security.py     # JWT + bcrypt helpers
│   │   ├── models/
│   │   │   ├── user.py         # SQLAlchemy User model
│   │   │   └── task.py         # SQLAlchemy Task model
│   │   ├── schemas/
│   │   │   ├── user.py         # Pydantic user schemas
│   │   │   └── task.py         # Pydantic task schemas
│   │   ├── routers/
│   │   │   ├── auth.py         # POST /register, POST /login
│   │   │   └── tasks.py        # Full tasks CRUD
│   │   ├── tests/
│   │   │   ├── conftest.py     # Fixtures and test DB setup
│   │   │   ├── test_auth.py    # Auth endpoint tests
│   │   │   └── test_tasks.py   # Task CRUD tests
│   │   ├── database.py         # SQLAlchemy engine + session
│   │   ├── dependencies.py     # get_current_user dependency
│   │   └── main.py             # FastAPI app + middleware
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html              # Single-page vanilla JS frontend
├── Dockerfile
├── render.yaml                 # Render deployment config
└── README.md
```

---

## API Endpoints

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/register` | Create a new user account |
| POST | `/login` | Authenticate and receive JWT token |

### Tasks (all require Bearer token)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

**Query params for `GET /tasks`:**
- `completed=true` / `completed=false` — filter by status
- `page=1` — page number (default: 1)
- `page_size=10` — items per page (default: 10, max: 100)

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp backend/.env.example backend/.env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing secret — use a long random string | *(required)* |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `30` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./taskmanager.db` |

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ **Never commit `.env` to version control.**

---

## Local Setup

### Option A — Plain Python

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/taskmanager.git
cd taskmanager

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env with your SECRET_KEY

# 5. Run the server
cd backend
uvicorn app.main:app --reload
```

Open **http://localhost:8000** for the app, **http://localhost:8000/docs** for API docs.

### Option B — Docker

```bash
# Build and run
docker build -t taskflow .
docker run -p 8000:8000 -e SECRET_KEY=your-secret-key taskflow
```

---

## Running Tests

```bash
cd backend
pytest app/tests/ -v
```

---

## Deployment on Render

1. Push this repo to GitHub (public).
2. Go to [render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo.
4. Set these env vars in the Render dashboard:
   - `SECRET_KEY` → generate a secure random value
   - `DATABASE_URL` → `sqlite:///./taskmanager.db` (or a Postgres URL for production)
5. Build command: `pip install -r backend/requirements.txt`
6. Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Or use the included `render.yaml` for automatic configuration.

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic v2, python-jose, passlib/bcrypt
- **Database:** SQLite (dev) / PostgreSQL (production ready)
- **Auth:** JWT (Bearer tokens)
- **Frontend:** Vanilla HTML + CSS + JavaScript (no build step)
- **Tests:** pytest, httpx (TestClient)
- **Deployment:** Docker, Render
