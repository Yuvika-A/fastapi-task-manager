from fastapi import FastAPI
from .database import Base, engine
from app.routers import auth_router, task_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(task_router.router)