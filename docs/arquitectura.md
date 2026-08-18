# Documento de Diseño Arquitectónico — LogiTrack Backend

**Sistema:** Plataforma SaaS de Gestión Logística Inteligente  
**Módulo:** 7.1 Fundamentos de Arquitectura Backend y Protocolos Web  
**Autor:** Ing. Nayib de la Cruz Márquez  

---

## 1. Patrón Arquitectónico Seleccionado

Para el ecosistema de **LogiTrack**, se ha seleccionado una arquitectura de **Monolito Modular**.

### Justificación Técnica
- **Concurrencia y Rendimiento:** Implementado sobre **FastAPI** (ASGI), el sistema maneja múltiples peticiones simultáneas de rastreo y consulta mediante I/O asíncrono no bloqueante (`async/await`).
- **Simplicidad Operativa y Escalabilidad:** Un monolito modular evita la sobrecarga operativa y de red (*network overhead*) propia de los microservicios en etapas iniciales, manteniendo una separación estricta de responsabilidades por capas (`routes`, `services`, `models`, `schemas`, `auth`).
- **Evolución:** Las fronteras entre módulos están claramente delimitadas, permitiendo que componentes de alto tráfico (como el cálculo de rutas) se migren a microservicios independientes en el futuro si la carga lo requiere.

---

## 2. Diagrama de Arquitectura Cliente-Servidor

```text
+-----------------------------------------------------------------------+
|                            CLIENTES                                   |
|   [ Web App / Dashboard ]              [ Dispositivos IoT / GPS ]     |
+-----------------------------------------------------------------------+
           |                                         |
           | HTTP/REST (JSON)                        | WebSockets / HTTP
           v                                         v
+-----------------------------------------------------------------------+
|                    REVERSE PROXY / NGINX                              |
|   - Terminación TLS/SSL                                              |
|   - Manejo de CORS y Rate Limiting                                    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    LOGITRACK BACKEND (FastAPI)                        |
|                                                                       |
|   +-------------------+  +-------------------+  +-----------------+   |
|   |   Auth (JWT/RBAC) |  |   API Routes      |  |   ORM Models    |   |
|   +-------------------+  +-------------------+  +-----------------+   |
+-----------------------------------------------------------------------+
           |                                         |
           | Async Queries                           | Task Delegation
           v                                         v
+-----------------------+                 +-----------------------------+
|   PostgreSQL Database |                 |   Broker: Redis             |
|   (Persistencia ORM)  |                 +-----------------------------+
+-----------------------+                                |
                                                         v
                                          +-----------------------------+
                                          |   Worker: Celery            |
                                          |   - Cálculo de Rutas        |
                                          |   - Reportes y Notif.       |
                                          +-----------------------------+
```

## 3. Justificación de Protocolos de Comunicación
### 3.1 HTTP / REST (API Principal)
* Protocoolo: HTTPS / RESTful
* Uso: Gestión de usuarios, autenticación (JWT), administración de flotas (vehículos/conductores) y operaciones CRUD de envíos.
* Ventajas: Sin estado (stateless), fácil de cachear, estándar de la industria y documentación automática mediante especificación OpenAPI/Swagger.

### 3.2 WebSockets (Rastreo en Tiempo Real)
* Protocolo: WS / WSS (WebSocket).
* Uso: Transmisión bidireccional continua de coordenadas GPS de los vehículos hacia el panel de monitoreo.
* Ventajas: Bajo consumo de ancho de banda y latencia mínima al mantener una conexión TCP persistente, evitando el polling constante sobre la base de datos.

## 4. Ciclo de Vida de las Peticiones Críticas
### 4.1 Petición Sincrónica: Creación y Consulta de Envíos
1. Cliente: Envía petición POST /api/v1/shipments/ con payload JSON y encabezado Authorization: Bearer <token>.
2. Reverse Proxy (Nginx): Valida cabeceras y redirige la petición al servidor ASGI (Uvicorn/FastAPI).
3. Middleware de Seguridad: Intercepta la petición, valida la firma y expiración del JWT, y confirma que el rol del usuario tenga permisos (ADMIN o OPERATOR).
4. Capa de Validación (Pydantic): Valida la estructura y tipos de datos del cuerpo de la petición.
5. Capa de Persistencia (SQLAlchemy): Abre transacción asíncrona en PostgreSQL, inserta el registro y confirma (commit).
6. Respuesta: El servidor retorna HTTP 201 Created con la representación JSON del envío.

### 4.2 Petición Asincrónica: Cálculo de Ruta Óptima
1. Disparador: Al crearse un envío que requiere procesamiento pesado, el handler invoca calculate_optimal_route_task.delay(shipment_id).
2. Broker (Redis): Recibe la tarea formateada en JSON y la encola.
3. Worker (Celery): Toma la tarea de la cola en segundo plano, ejecuta el algoritmo de optimización de rutas sin bloquear el servidor web.
4. Notificación / Actualización: Al finalizar, el worker actualiza el estado del envío en PostgreSQL y emite un evento de finalización.

