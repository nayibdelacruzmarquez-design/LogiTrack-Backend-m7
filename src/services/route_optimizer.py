import logging
import time
from src.services.celery_app import celery_app

logger = logging.getLogger("logitrack")


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
    autoretry_for=(Exception,)  # 🔄 Reintento automático en fallo temporal
)
def calculate_optimal_route(self, shipment_id: int, origin: str, destination: str):
    """
    Simulación de procesamiento pesado: Cálculo de optimización de ruta GPS.
    """
    logger.info(f"[Celery Worker] Calculando ruta óptima para el envío #{shipment_id} ({origin} -> {destination})...")

    # Simula proceso pesado de 3 segundos
    time.sleep(3)

    result = {
        "shipment_id": shipment_id,
        "status": "Ruta Calculada",
        "distance_km": 128.4,
        "estimated_hours": 2.5
    }
    logger.info(f"[Celery Worker] Ruta calculada exitosamente para envío #{shipment_id}: {result}")
    return result