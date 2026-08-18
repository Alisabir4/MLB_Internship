from fastapi import FastAPI
from app.routes.students import router as student_router

app = FastAPI(
    title="Student Management REST API",
    description="A simple REST API built with FastAPI for managing students.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Student Management REST API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }


app.include_router(student_router)