from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="AI Appointment Scheduler",
    version="1.0"
)

app.include_router(router)
