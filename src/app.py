import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Importación del inicializador de BD desde config.database
from src.config.database import init_db
from src.routes import auth, drivers, shipments, vehicles

# Configuración básica de Logging
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
    # Evento al iniciar la aplicación: Crear tablas en la BD si no existen
    logger.info("Iniciando LogiTrack API v1.0.0...")
    await init_db()
    logger.info("Tablas de la base de datos verificadas / creadas correctamente.")
    yield
    # Evento al apagar la aplicación
    logger.info("Apagando servicio LogiTrack API...")


# Instancia principal de FastAPI
app = FastAPI(
    title="LogiTrack API",
    version="1.0.0",
    description="Plataforma SaaS de Gestión Logística Inteligente con Seguridad JWT y RBAC",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Habilitación global del esquema de autenticación Bearer JWT para Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Aplica el candado de seguridad globalmente en la interfaz
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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