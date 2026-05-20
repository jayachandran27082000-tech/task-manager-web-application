from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import init_db
from .routers import auth_router, tasks_router

app = FastAPI(
    title="Task Manager API",
    description="Task Manager with JWT Authentication",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def startup():
    try:
        init_db()
        print("Database initialized")
    except Exception as e:
        print("Database init failed:", e)


# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Task Manager API Running",
        "docs": "/docs"
    }


# Optional frontend support
frontend_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "frontend"
)

if os.path.exists(frontend_path):
    app.mount(
        "/static",
        StaticFiles(directory=frontend_path),
        name="static"
    )

    @app.get("/app", include_in_schema=False)
    def serve_frontend():
        return FileResponse(
            os.path.join(frontend_path, "index.html")
        )