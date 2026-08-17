from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routes.job import router as job_router

app = FastAPI(title="Candidate Processor BTG")

origins = ["http://localhost:5173", settings.front_url]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, allow_headers=["*"], 
    allow_methods=["*"]
)

app.include_router(job_router)
