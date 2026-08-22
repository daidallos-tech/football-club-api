import pytest
from httpx import AsyncClient
from tests.conftest import auth_header, create_test_admin, login_admin, create_test_user, login_user
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

@pytest.mark.anyio
async def test_update_team_by_id_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)
    team_response = await client.post(
                "/api/admin/teams",
                json={"name": "PSG FC", "shortName": "PSG", "tla": "PSG", "founded": 1876, "country": "France", "leagueCode": "FL"},
                headers=headers
            )

    assert team_response.status_code == 201
    team_id = team_response.json()["id"]

    update_response = await client.patch(
        f"/api/admin/teams/{team_id}",
        json={
            "name": "update_name",
            "shortName": "updated"
        },
        headers=headers
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "update_name"
    assert data["shortName"] == "updated"
    assert "tla" in data
    assert "founded" in data
    assert "country" in data
    assert "leagueCode" in data

@pytest.mark.anyio
async def test_update_team_by_non_authorized(client: AsyncClient):
    update_response = await client.patch(
            "/api/admin/teams/99999",
            json={
                "name": "update_name",
                "shortName": "updated"
            },
        )

    assert update_response.status_code == 401

@pytest.mark.anyio
async def test_update_team_error_validation(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)
    team_response = await client.post(
                "/api/admin/teams",
                json={"name": "PSG FC", "shortName": "PSG", "tla": "PSG", "founded": 1876, "country": "France", "leagueCode": "FL"},
                headers=headers
            )

    assert team_response.status_code == 201
    team_id = team_response.json()["id"]

    update_response = await client.patch(
        f"/api/admin/teams/{team_id}",
        json={
            "name": "",
            "founded": 1490,
            "shortName": 666,
        },
        headers=headers
    )

    assert update_response.status_code == 422
    errors = update_response.json()["detail"]
    error_fields = [err["loc"][-1] for err in errors]
    
    assert "name" in error_fields
    assert "founded" in error_fields
    assert "shortName" in error_fields

@pytest.mark.anyio
async def test_delete_team_by_admin(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)
    team_response = await client.post(
                "/api/admin/teams",
                json={"name": "PSG FC", "shortName": "PSG", "tla": "PSG", "founded": 1876, "country": "France", "leagueCode": "FL"},
                headers=headers
            )

    assert team_response.status_code == 201
    team_id = team_response.json()["id"]

    delete_response = await client.delete(
        f"/api/admin/teams/{team_id}",
        headers=headers
    )

    assert delete_response.status_code == 204

@pytest.mark.anyio
async def test_delete_team_by_non_authorized(client: AsyncClient):
    delete_response = await client.delete(
        "/api/admin/teams/99999"
    )
    
    assert delete_response.status_code == 401

@pytest.mark.anyio
async def test_delete_non_existing_team(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    delete_response = await client.delete(
        "/api/admin/teams/99999",
        headers=headers
    )
        
    assert delete_response.status_code == 404

@pytest.mark.anyio
async def test_delete_team_by_user(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    delete_response = await client.delete(
        "/api/admin/teams/99999",
        headers=headers
    )
        
    assert delete_response.status_code == 403