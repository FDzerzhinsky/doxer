"""
EN: File: app/api/router.py
EN: Purpose: Configures API routing and endpoint composition.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/api/router.py
RU: Назначение: Настраивает маршрутизацию API и композицию эндпоинтов.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.documents import router as documents_router


api_router = APIRouter()
api_router.include_router(documents_router)
api_router.include_router(chat_router)
