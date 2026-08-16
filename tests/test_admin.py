import pytest
from httpx import AsyncClient
from tests.conftest import auth_header, create_test_user, login_user, create_test_admin, login_admin
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

@pytest.mark.anyio
async def test_update_user_profile_by_admin_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "testuser", "email": "user@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    update_response = await client.patch(
        f"/api/admin/{user_id}",
        json={
            "username": "update_username"
        },
        headers=headers
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert "id" in data
    assert data["username"] == "update_username"
    assert "image_file" in data
    assert "email" in data
    assert "role" in data

@pytest.mark.anyio
async def test_delete_user_profile_by_admin_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "testuser", "email": "user@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    delete_response = await client.delete(
        f"/api/admin/{user_id}",
        headers=headers
    )

    assert delete_response.status_code == 204