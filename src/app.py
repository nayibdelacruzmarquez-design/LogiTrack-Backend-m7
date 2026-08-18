import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, drivers, shipments, vehicles

# Configuración básica de Logging (para auditoría y evidencia)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("evidencia/app.log", encoding="utf-8") if False else logging.NullHandler()
    ]
)
logger = logging.getLogger("logitrack")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento al iniciar la aplicación
    logger.info("Iniciando LogiTrack API v1.0.0...")
    yield
    # Evento al apagar la aplicación
    logger.info("Apagando servicio LogiTrack API...")

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="LogiTrack API",
    version="1.0.0",
    description="Plataforma SaaS de Gestión Logística Inteligente con Seguridad JWT y RBAC",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración del Middleware de CORS (Seguridad Módulo 7.5)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se restrinja a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(shipments.router, prefix="/api/v1/shipments", tags=["Envíos"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["Vehículos"])
app.include_router(drivers.router, prefix="/api/v1/drivers", tags=["Conductores"])

# Endpoint de Verificación de Salud
@app.get("/health", tags=["Salud"])
async def health_check():
    """
    Endpoint de comprobación de salud del servidor.
    Retorna el estado operativo y versión del servicio.
    """
    return {
        "status": "ok",
        "service": "LogiTrack Backend",
        "version": "1.0.0"
    }

# Endpoint Raíz de Bienvenida
@app.get("/", tags=["Raíz"])
async def root():
    """
    Ruta principal con accesos rápidos a la documentación.
    """
    return {
        "message": "Bienvenido a LogiTrack API",
        "docs": "/docs",
        "health": "/health"
    }