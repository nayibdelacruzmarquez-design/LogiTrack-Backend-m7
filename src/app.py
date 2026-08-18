from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LogiTrack API",
    version="1.0.0",
    description="Plataforma SaaS de Gestión Logística Inteligente",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.get("/", tags=["Raíz"])
async def root():
    return {
        "message": "Bienvenido a LogiTrack API",
        "docs": "/docs",
        "health": "/health"
    }