"""
GREENRIDE - Main FastAPI Application
Connects all community mobility routers, CORS, and mounts the modern frontend SPA.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import init_db
from .seed_data import seed
from .routers import auth, rides, bookings, vehicles, drivers, marketplace, impact, admin, safety

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        from .database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM users")
            if cursor.fetchone()["cnt"] == 0:
                print("Seeding database on startup...")
                seed()
    except Exception as e:
        print("Startup database check exception:", e)
        seed()
    yield

# Initialize FastAPI application
app = FastAPI(
    title="GREENRIDE - Sustainable Community Mobility Platform",
    description="Full-stack community mobility platform connecting passengers, EV drivers, and spare vehicle owners.",
    version="2.0.0-technofest",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(rides.router)
app.include_router(bookings.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(marketplace.router)
app.include_router(impact.router)
app.include_router(admin.router)
app.include_router(safety.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "GREENRIDE",
        "version": "2.0.0",
        "environment": "Technofest Demonstration"
    }

# Mount Frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend_root():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found"}

    # Catch-all fallback for SPA client-side routes
    @app.get("/{full_path:path}")
    def serve_spa_paths(full_path: str):
        # Don't intercept API paths
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_file)
