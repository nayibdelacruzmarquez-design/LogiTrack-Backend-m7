import os
from celery import Celery
from celery.schedules import crontab

# URL de conexión a Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Instancia principal de Celery en services
celery_app = Celery(
    "logitrack_services",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "src.services.route_optimizer",
        "src.services.notifications"
    ]
)

# Ajustes y Programación Periódica (Celery Beat)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Mexico_City",
    enable_utc=True,

    # 🕒 Tarea periódica para cumplimiento del entregable 7.6
    beat_schedule={
        "cleanup-logs-or-update-statuses": {
            "task": "src.services.notifications.scheduled_status_check",
            "schedule": 300.0,  # Se ejecuta automáticamente cada 5 minutos
        },
    },
)