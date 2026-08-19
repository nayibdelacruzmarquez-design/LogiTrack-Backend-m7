import logging
import time
from src.services.celery_app import celery_app

logger = logging.getLogger("logitrack")


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
    autoretry_for=(Exception,)
)
def send_shipment_notification(self, shipment_id: int, client_email: str):
    """
    Tarea asíncrona para envío de emails/notificaciones masivas sin bloquear la API.
    """
    logger.info(f"[Celery Worker] Enviando notificación de envío #{shipment_id} a {client_email}...")

    # Simula tiempo de respuesta de un servidor SMTP/Email
    time.sleep(2)

    logger.info(f"[Celery Worker] Notificación enviada con éxito a {client_email}.")
    return {"status": "sent", "recipient": client_email, "shipment_id": shipment_id}


@celery_app.task
def scheduled_status_check():
    """
    Tarea periódica ejecutada por Celery Beat (ej. limpieza de logs o actualización de estados).
    """
    logger.info("[Celery Beat] Tarea periódica ejecutada: Verificación de estados y mantenimiento de logs.")
    return "Verificación completada."