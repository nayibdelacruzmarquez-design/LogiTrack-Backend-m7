import logging
import json
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación del inicializador de BD desde config.database
from src.config.database import init_db
from src.routes import auth, drivers, shipments, vehicles


# ==========================================
# CONFIGURACIÓN DE LOGGING ESTRUCTURADO (JSON)
# ==========================================
class StructuredJSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)


def setup_logger():
    logger = logging.getLogger("logitrack")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(handler)

    return logger


logger = setup_logger()


# ==========================================
# LIFESPAN Y APLICACIÓN
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando LogiTrack API v1.0.0...")
    await init_db()
    logger.info("Tablas de la base de datos verificadas / creadas correctamente.")
    yield
    logger.info("Apagando servicio LogiTrack API...")


app = FastAPI(
    title="LogiTrack API",
    version="1.0.0",
    description="Plataforma SaaS de Gestión Logística Inteligente con Seguridad JWT y RBAC",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(shipments.router, prefix="/api/v1/shipments", tags=["Envíos"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["Vehículos"])
app.include_router(drivers.router, prefix="/api/v1/drivers", tags=["Conductores"])


# Endpoints base
@app.get("/health", tags=["Salud"])
async def health_check():
    return {
        "status": "ok",
        "service": "LogiTrack Backend",
        "version": "1.0.0"
    }


@app.get("/", tags=["Raíz"])
async def root():
    return {
        "message": "Bienvenido a LogiTrack API",
        "docs": "/docs",
        "health": "/health"
    }