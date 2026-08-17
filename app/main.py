from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.job import router as job_router

app = FastAPI(title="Candidate Processor BTG")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, allow_headers=["*"], 
    allow_methods=["*"]
)

app.include_router(job_router)
