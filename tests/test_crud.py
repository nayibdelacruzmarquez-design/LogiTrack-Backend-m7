import pytest


@pytest.mark.asyncio
async def test_crud_flow(client):
    # 1. Registrar usuario y obtener JWT Token
    user_payload = {
        "name": "Admin LogiTrack",
        "email": "admin@logitrack.com",
        "password": "AdminPassword123",
        "phone": "+529219998877"
    }
    reg_res = await client.post("/api/v1/auth/register", json=user_payload)
    assert reg_res.status_code == 201

    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@logitrack.com", "password": "AdminPassword123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un Vehículo
    veh_payload = {"plate": "LOG-2026", "model": "Kenworth T680", "capacity_kg": 15000.0}
    veh_res = await client.post("/api/v1/vehicles/", json=veh_payload, headers=headers)
    assert veh_res.status_code in [200, 201]

    # 3. Listar Vehículos
    veh_list = await client.get("/api/v1/vehicles/", headers=headers)
    assert veh_list.status_code == 200

    # 4. Crear un Conductor
    driver_payload = {
        "full_name": "Chofer Ejemplo",
        "email": "chofer@logitrack.com",
        "license_number": "LIC-2026-X"
    }
    drv_res = await client.post("/api/v1/drivers/", json=driver_payload, headers=headers)
    assert drv_res.status_code in [200, 201]

    # 5. Listar Conductores
    drv_list = await client.get("/api/v1/drivers/", headers=headers)
    assert drv_list.status_code == 200

    # 6. Crear un Envío (Shipment)
    shipment_payload = {
        "tracking_number": "TRK-9999",
        "origin_address": "Planta Coatzacoalcos",
        "destination_address": "Puerto Veracruz",
        "weight_kg": 500.0
    }
    ship_res = await client.post("/api/v1/shipments/", json=shipment_payload, headers=headers)
    assert ship_res.status_code in [200, 201]

    # 7. Listar Envíos Autenticado
    ship_list = await client.get("/api/v1/shipments/", headers=headers)
    assert ship_list.status_code == 200


@pytest.mark.asyncio
async def test_shipment_not_found(client):
    user_payload = {
        "name": "User 404",
        "email": "u404@logitrack.com",
        "password": "Password123"
    }
    await client.post("/api/v1/auth/register", json=user_payload)
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "u404@logitrack.com", "password": "Password123"}
    )
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    response = await client.get("/api/v1/shipments/999999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    user_payload = {
        "name": "Usuario Auth Test",
        "email": "auth_test@logitrack.com",
        "password": "PasswordCorrecta123"
    }
    await client.post("/api/v1/auth/register", json=user_payload)

    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "auth_test@logitrack.com", "password": "PasswordIncorrecta"}
    )
    assert login_res.status_code == 401