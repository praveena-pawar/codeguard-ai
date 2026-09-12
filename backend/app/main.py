from fastapi import FastAPI

from app.api.routes.analysis import router as analysis_router

app = FastAPI(
    title="CodeGuard AI",
    description="AI-powered code review, testing, and fixing.",
    version="0.1.0",
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