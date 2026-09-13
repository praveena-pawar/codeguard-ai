from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router as analysis_router


app = FastAPI(
    title="CodeGuard AI",
    description="AI-powered code review, testing, and fixing.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://codeguard-ai-ten.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)


@app.get("/")
def root():
    return {
        "message": "CodeGuard AI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }