# 🚚 LogiTrack - Sistema de Gestión Logística Backend (Módulo 7)

**Alumno:** Ing. Nayib de la Cruz Márquez  
**Repositorio:** LogiTrack_Modulo7_DeLaCruzNayib  

Sistema de backend para gestión de envíos, inventario y procesamiento asíncrono de reportes logísticos construido con FastAPI, PostgreSQL, Redis, Celery y Nginx.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.12
* **Framework Backend:** FastAPI (ASGI)
* **Base de Datos:** PostgreSQL 15 (ORM SQLAlchemy + `asyncpg`)
* **Gestión de Tareas Asíncronas:** Celery + Redis
* **Proxy Inverso / Servidor:** Nginx + Uvicorn
* **Contenerización:** Docker & Docker Compose
* **Testing:** Pytest & Locust

---

## 🚀 Instrucciones de Instalación y Despliegue

### Requisitos Previos
* Docker Desktop instalado y corriendo.
* Git.

### Despliegue con Docker (Entorno de Producción)

1. Clonar el repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSO>
   cd LogiTrack_Modulo7_DeLaCruzNayib
   ```
   
2. Configurar variables de entorno:
   ```bash
    cp .env.example .env
   ```
   
3. Levantar todo el stack de servicios (PostgreSQL, Redis, API, Worker, Nginx):
   ```bash
    docker-compose up -d --build
   ```
   
4. Verificar el estado de los contenedores:
   ```bash
    docker-compose ps
   ```
   
5. Acceder a la documentación interactiva (Swagger UI):
* Vía Nginx (Puerto 80): http://localhost/docs

* Directo a la API: http://localhost:8000/docs

## 🧪 Ejecución de Pruebas Unitarias y Cobertura
Para ejecutar las pruebas en un entorno local con virtualenv:
   ```bash
    # Activar entorno virtual
    .venv\Scripts\activate

    # Ejecutar suite de pruebas con Pytest y Cobertura
    python -m pytest -v --cov=src
   ```
## 📂 Estructura del Proyecto
* src/: Código fuente (Rutas, Modelos, Servicios, Autenticación, Configuración).

* docs/: Documentación técnica de arquitectura, API y auto-crítica.

* nginx/: Configuración del proxy inverso Nginx.

* evidencia/: Evidencias no falsificables (logs, resultados de tests, historial git y capturas).
