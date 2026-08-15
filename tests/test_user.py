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