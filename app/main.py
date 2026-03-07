from fastapi import FastAPI
from .database import Base, engine
from app.routers import auth_router, task_router

app = FastAPI(
    title="FastAPI Task Manager",
    description="A Task Manager API built with FastAPI",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router.router)
app.include_router(task_router.router)

# Root endpoint (for homepage)
@app.get("/")
def root():
    return {
        "message": "FastAPI Task Manager API is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }