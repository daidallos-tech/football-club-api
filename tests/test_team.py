import pytest
from httpx import AsyncClient
from tests.conftest import create_test_admin, auth_header, login_admin
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

@pytest.mark.anyio
async def test_get_team_by_id(client:AsyncClient, db_session: AsyncSession):
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

    response = await client.get(
        f"/api/teams/{team_id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "shortName" in data
    assert "tla" in data
    assert "founded" in data
    assert "country" in data
    assert "leagueCode" in data
    
