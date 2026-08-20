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
        f"/api/admin/users/{user_id}",
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
async def test_update_user_profile_by_non_admin(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user2", "email": "user2@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    update_response = await client.patch(
        f"/api/admin/users/{user_id}",
        json={
            "username": "update_username"
        },
        headers=headers
    )

    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "You do not have enough permissions. Admin only."


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
        f"/api/admin/users/{user_id}",
        headers=headers
    )

    assert delete_response.status_code == 204

@pytest.mark.anyio
async def test_delete_user_profile_by_non_admin(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user2", "email": "user2@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    delete_response = await client.delete(
        f"/api/admin/users/{user_id}",
        headers=headers
    )

    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "You do not have enough permissions. Admin only."

@pytest.mark.anyio
async def test_update_user_profile_picture_by_admin_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user2", "email": "user2@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()

    update_response = await client.patch(
        f"/api/admin/users/{user_id}/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")},
        headers=headers
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["image_file"] is not None
    assert data["image_file"].endswith(".jpg")

@pytest.mark.anyio
async def test_update_user_profile_picture_by_non_admin(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user2", "email": "user2@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()

    update_response = await client.patch(
        f"/api/admin/users/{user_id}/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")},
        headers=headers
    )

    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "You do not have enough permissions. Admin only."

@pytest.mark.anyio
async def test_delete_user_profile_picture_by_admin_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user2", "email": "user2@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()

    update_response = await client.patch(
        f"/api/admin/users/{user_id}/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")},
        headers=headers
    )
    assert update_response.status_code == 200

    delete_response = await client.delete(
        f"/api/admin/users/{user_id}/picture",
        headers=headers
    )

    assert delete_response.status_code == 204

@pytest.mark.anyio
async def test_delete_user_profile_picture_by_non_admin(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    user_response = await client.post(
        "/api/users",
        json={"username": "user3", "email": "user3@test.com", "password": "password123"}
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    delete_response = await client.delete(
        f"/api/admin/users/{user_id}/picture",
        headers=headers
    )

    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "You do not have enough permissions. Admin only."




