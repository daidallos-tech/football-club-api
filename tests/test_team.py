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
    
@pytest.mark.anyio
async def test_get_teams_with_paginate_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)


    for i in range(5):
        response = await client.post(
            "/api/admin/teams",
            json={
                "name": f"Team {i}",
                "shortName": f"T{i}",
                "tla": f"L{i}", 
                "founded": 1900 + i,
                "country": f"Contry {i}",
                "leagueCode": f"F{i}"
            },
            headers=headers,
        )
        assert response.status_code == 201

    response = await client.get("/api/teams/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5

    response = await client.get("/api/teams/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2

    response = await client.get("/api/teams/?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 2

@pytest.mark.anyio
async def test_get_teams_search_by_parameters_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    teams_to_create = [
        {"name": "Chelsea FC", "shortName": "CHE", "tla": "CHE", "founded": 1905, "country": "England", "leagueCode": "PL"},
        {"name": "Arsenal FC", "shortName": "ARS", "tla": "ARS", "founded": 1886, "country": "England", "leagueCode": "PL"},
        {"name": "Paris Saint-Germain", "shortName": "PSG", "tla": "PSG", "founded": 1970, "country": "France", "leagueCode": "FL"},
    ]

    for team in teams_to_create:
        res = await client.post("/api/admin/teams", json=team, headers=headers)
        assert res.status_code == 201

    name_response = await client.get("/api/teams/?name=Chelsea FC&limit=50&offset=0")
    
    assert name_response.status_code == 200
    data = name_response.json()

    assert data["total"] == 1  
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Chelsea FC"
    assert data["limit"] == 50
    assert data["offset"] == 0

    league_response = await client.get("/api/teams/?league=pl&limit=50&offset=0")

    assert league_response.status_code == 200
    data = league_response.json()
    assert data["total"] == 2  
    assert len(data["items"]) == 2
    assert data["limit"] == 50
    assert data["offset"] == 0

    league_response = await client.get("/api/teams/?country=england&limit=50&offset=0")

    assert league_response.status_code == 200
    data = league_response.json()
    assert data["total"] == 2  
    assert len(data["items"]) == 2
    assert data["limit"] == 50
    assert data["offset"] == 0

@pytest.mark.anyio
async def test_get_non_existing_team_by_id(client: AsyncClient):
    response = await client.get(
            "/api/teams/9999"
        )
    
    assert response.status_code == 404

@pytest.mark.anyio
async def test_get_non_existing_teams_by_paramaters(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    teams_to_create = [
        {"name": "Chelsea FC", "shortName": "CHE", "tla": "CHE", "founded": 1905, "country": "England", "leagueCode": "PL"},
        {"name": "Arsenal FC", "shortName": "ARS", "tla": "ARS", "founded": 1886, "country": "England", "leagueCode": "PL"},
        {"name": "Paris Saint-Germain", "shortName": "PSG", "tla": "PSG", "founded": 1970, "country": "France", "leagueCode": "FL"},
    ]

    for team in teams_to_create:
        res = await client.post("/api/admin/teams", json=team, headers=headers)
        assert res.status_code == 201

    name_response = await client.get("/api/teams/?name=Barcelona&limit=50&offset=0")
    
    assert name_response.status_code == 200
    data = name_response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0

    league_response = await client.get("/api/teams/?league=None&limit=50&offset=0")

    assert name_response.status_code == 200
    data = name_response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0

    league_response = await client.get("/api/teams/?country=Germany&limit=50&offset=0")

    assert name_response.status_code == 200
    data = name_response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0