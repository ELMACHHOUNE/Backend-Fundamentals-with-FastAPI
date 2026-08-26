from fastapi import FastAPI
from app.routers import health, chat, quiz, summarise

app = FastAPI(
    title="Backend Fundamentals API",
    description="A simple FastAPI backend with health, chat, quiz, and summarise endpoints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(summarise.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Backend Fundamentals API",
        "docs": "/docs",
        "health": "/health"
    }