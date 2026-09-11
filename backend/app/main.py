from fastapi import FastAPI

app = FastAPI(
    title="CodeGuard AI",
    description="AI-powered code review, testing, and fixing.",
    version="0.1.0",
)


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