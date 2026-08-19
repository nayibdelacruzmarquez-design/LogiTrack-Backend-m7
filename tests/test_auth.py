import pytest


@pytest.mark.asyncio
async def test_register_and_login_user(client):
    # 1. Registrar usuario de prueba
    register_payload = {
        "name": "Usuario de Prueba",
        "email": "testuser@logitrack.com",
        "password": "PasswordSegura123",
        "phone": "+529211234567"
    }
    response_reg = await client.post("/api/v1/auth/register", json=register_payload)
    assert response_reg.status_code == 201
    assert response_reg.json()["email"] == "testuser@logitrack.com"

    # 2. Login correcto
    login_payload = {
        "username": "testuser@logitrack.com",
        "password": "PasswordSegura123"
    }
    response_login = await client.post("/api/v1/auth/login", data=login_payload)
    assert response_login.status_code == 200
    token_data = response_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    login_payload = {
        "username": "noexiste@logitrack.com",
        "password": "PasswordErronea"
    }
    response = await client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 401
    assert "Credenciales incorrectas" in response.json()["detail"]