import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Bienvenido a LogiTrack API" in response.json()["message"]


@pytest.mark.asyncio
async def test_get_shipments_unauthorized(client):
    # Intentar consultar envíos sin enviar Token JWT en cabecera
    response = await client.get("/api/v1/shipments/")
    assert response.status_code == 401