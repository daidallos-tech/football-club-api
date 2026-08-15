import pytest
from httpx import AsyncClient
from tests.conftest import auth_header, create_test_user, login_user
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient):
    """ User creation success scenario """
    response = await client.post(
        "/api/users",
        json={
            "username": "roman",
            "email": "roman@test.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "roman"
    assert data["email"] == "roman@test.com"
    assert "id" in data
    assert "image_file" in data
    assert "password" not in data
    assert "password_hash" not in data

@pytest.mark.anyio
async def test_create_user_error_validation(client: AsyncClient):
    """ User creation scenario with error validation """
    response = await client.post(
            "/api/users",
            json={
                "email": "roman@test.com"
            },
        )

    assert response.status_code == 422
    assert "username" in response.text
    assert "password" in response.text

@pytest.mark.anyio
async def test_create_user_with_duplicate_email(client: AsyncClient):
    """ User creation scenario with email that is already exist """
    await create_test_user(client)

    response = await client.post(
        "/api/users",
        json={
            "username": "roman",
            "email": "test@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.anyio 
async def test_create_user_with_duplicate_username(client: AsyncClient):
    """ User creation scenario with username that is already exist """
    await create_test_user(client)

    response = await client.post(
        "/api/users",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

@pytest.mark.anyio
async def test_get_current_user_profile_success(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    response = await client.get(
        "/api/users/me",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "image_file" in data
    assert "password" not in data
    assert "password_hash" not in data

@pytest.mark.anyio
async def test_get_current_user_by_non_authorized(client: AsyncClient):
    response = await client.get(
        "/api/users/me",
    )
    
    assert response.status_code == 401

@pytest.mark.anyio
async def test_get_user_by_user_id_success(client: AsyncClient):
    user_response = await client.post(
            "/api/users",
            json={"username": "testuser", "email": "user@test.com", "password": "password123"}
        )
    user_id = user_response.json()["id"]

    response = await client.get(
        f"/api/users/{user_id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "image_file" in data
    assert "password" not in data
    assert "password_hash" not in data

