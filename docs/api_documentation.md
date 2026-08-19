# Documentación de la API RESTful - LogiTrack

## Información General
* **URL Base (Producción/Docker):** `http://localhost/`
* **URL Base (Desarrollo):** `http://localhost:8000/`
* **Documentación Interactiva Swagger:** `http://localhost/docs`
* **Especificación OpenAPI (JSON):** `http://localhost/openapi.json`
* **Autenticación:** Bearer Token (JWT) mediante el header `Authorization: Bearer <token>`

---

## Resumen de Endpoints

### 1. Autenticación y Usuarios (`/auth`)
* `POST /auth/register`: Registrar un nuevo usuario.
* `POST /auth/login`: Autenticarse y obtener token JWT de acceso.

### 2. Gestión de Envíos e Inventario (`/api/v1/...`)
* `GET /api/v1/shipments`: Listar envíos (soporta paginación).
* `POST /api/v1/shipments`: Crear un nuevo registro de envío.
* `GET /api/v1/shipments/{id}`: Obtener detalles de un envío por ID.
* `PUT /api/v1/shipments/{id}`: Actualizar estado de envío.
* `DELETE /api/v1/shipments/{id}`: Eliminar o desactivar un envío.

### 3. Tareas Asíncronas (`/api/v1/tasks`)
* `POST /api/v1/tasks/generate-report`: Encolar la generación de reportes en Celery.
* `GET /api/v1/tasks/status/{task_id}`: Consultar el estado de ejecución del worker.

---

## Códigos de Respuesta HTTP
* `200 OK`: Solicitud exitosa.
* `201 Created`: Recurso creado exitosamente.
* `400 Bad Request`: Datos de entrada inválidos (Validación Pydantic).
* `401 Unauthorized`: Token no proporcionado o expirado.
* `403 Forbidden`: Permisos insuficientes (RBAC).
* `404 Not Found`: Recurso no encontrado.
* `500 Internal Server Error`: Error no controlado en el servidor.