"""
EN: File: app/main.py
EN: Purpose: Creates and configures the FastAPI application entry point.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/main.py
RU: Назначение: Создает и настраивает точку входа FastAPI-приложения.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.router import api_router
from app.core.config import get_settings


settings = get_settings()


# EN: Function lifespan executes a specific reusable operation.
# RU: Функция lifespan выполняет конкретную переиспользуемую операцию.
@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.ensure_directories()
    yield

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="RAG backend for document upload, retrieval, and question answering.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router, prefix="/api")


# EN: Function root executes a specific reusable operation.
# RU: Функция root выполняет конкретную переиспользуемую операцию.
@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "running",
    }
