from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import shipments, vehicles, drivers, auth

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="LogiTrack API",
    version="1.0.0",
    description="Plataforma SaaS de Gestión Logística Inteligente",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración del Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers (Módulo 7.3)
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