"""
EN: File: app/api/routes/health.py
EN: Purpose: Defines API endpoint handlers for a specific route group.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/api/routes/health.py
RU: Назначение: Определяет обработчики API-эндпоинтов для конкретной группы маршрутов.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter(tags=["health"])


# EN: Function health_check executes a specific reusable operation.
# RU: Функция health_check выполняет конкретную переиспользуемую операцию.
@router.get("/health")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
    }
