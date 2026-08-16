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
    assert "email" not in data
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.anyio
async def test_get_user_by_non_existing_id(client: AsyncClient):
    response = await client.get(
            "/api/users/99999"
        )

    assert response.status_code == 404

@pytest.mark.anyio
async def test_partial_user_profile_update(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    response = await client.patch(
        "/api/users/me",
        json={
            "username": "update_username"
        },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "update_username"
    assert data["email"] == "test@example.com"
    assert "image_file" in data

@pytest.mark.anyio
async def test_partial_user_profile_update_by_non_authorized(client: AsyncClient):
    response = await client.patch(
            "/api/users/me",
            json={
                "username": "update_username"
            }
        )

    assert response.status_code == 401

@pytest.mark.anyio
async def test_partial_user_profile_update_error_validation(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    response = await client.patch(
        "/api/users/me",
        json={
            "username": 123456
        },
        headers=headers
    )

    assert response.status_code == 422

@pytest.mark.anyio
async def test_delete_user_success(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    response = await client.delete(
        "/api/users/me",
        headers=headers
    )

    assert response.status_code == 204

@pytest.mark.anyio
async def test_delete_user_by_non_authorized(client: AsyncClient):
    response = await client.delete(
            "/api/users/me",
        )

    assert response.status_code == 401

@pytest.mark.anyio
async def test_upload_image_success(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()

    response = await client.patch(
        "/api/users/me/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")},
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["image_file"] is not None
    assert data["image_file"].endswith(".jpg")

@pytest.mark.anyio
async def test_upload_image_by_non_authorized(client: AsyncClient):
    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()
    
    response = await client.patch(
        "/api/users/me/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")}
    )

    assert response.status_code == 401

@pytest.mark.anyio
async def test_delete_image_success(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    test_image_path = Path(__file__).parent / "test_image.jpg"
    image_bytes = test_image_path.read_bytes()
    
    upload_response = await client.patch(
        "/api/users/me/picture",
        files={"file": ("profile.jpg", image_bytes, "image/jpeg")},
        headers=headers
    )

    assert upload_response.status_code == 200

    delete_response = await client.delete(
            "/api/users/me/picture",
            headers=headers
        )

    assert delete_response.status_code == 204

@pytest.mark.anyio
async def test_delete_image_by_non_authorized(client: AsyncClient):
    delete_response = await client.delete(
            "/api/users/me/picture"
        )

    assert delete_response.status_code == 401

@pytest.mark.anyio
async def test_delete_non_existing_image(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    delete_response = await client.delete(
            "/api/users/me/picture",
            headers=headers
        )

    assert delete_response.status_code == 400
    assert delete_response.json()["detail"] == "User or picture not found"
