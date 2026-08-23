import pytest
from httpx import AsyncClient
from tests.conftest import create_test_admin, auth_header, login_admin
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.anyio
async def test_get_player_by_id(client:AsyncClient, db_session: AsyncSession):
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
    player_response = await client.post(
        "/api/admin/players",
        json={
            "name": "Test",
            "position": "Goalkeeper",
            "dateOfBirth": "1973-08-11",
            "nationality": "Test",
            "team_id": team_id
        },
        headers=headers
    )

    assert player_response.status_code == 201
    player_id = player_response.json()["id"]

    response = await client.get(
        f"/api/players/{player_id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["position"] == "Goalkeeper"
    assert data["dateOfBirth"] == "1973-08-11"
    assert data["nationality"] == "Test"
    assert "team_id" in data 

@pytest.mark.anyio
async def test_get_non_existing_player_by_id(client: AsyncClient):
    response = await client.get(
        f"/api/players/99999"
    )

    assert response.status_code == 404

@pytest.mark.anyio
async def test_get_players_with_paginate_success(client: AsyncClient, db_session: AsyncSession):
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


    for i in range(5):
        response = await client.post(
            "/api/admin/players",
            json={
                "name": f"Test {i}",
                "position": "Goalkeeper",
                "dateOfBirth": f"1973-08-1{i}",
                "nationality": f"Test {i}",
                "team_id": team_id
            },
            headers=headers,
        )
        assert response.status_code == 201

    response = await client.get("/api/players/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5

    response = await client.get("/api/players/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2

    response = await client.get("/api/players/?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 2


@pytest.mark.anyio
async def test_get_players_with_paginate_success(client: AsyncClient, db_session: AsyncSession):
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

    players = [
        {"name": "Test", "position": "Goalkeeper", "dateOfBirth": "1973-08-11", "nationality": "France", "team_id": team_id},
        {"name": "Test", "position": "Defence", "dateOfBirth": "1973-08-12", "nationality": "Spain", "team_id": team_id},
        {"name": "Test", "position": "Offence", "dateOfBirth": "1973-08-13", "nationality": "Spain", "team_id": team_id}
    ]

    for player in players:
        res = await client.post("/api/admin/players", json=player, headers=headers)
        assert res.status_code == 201

    position_response = await client.get("/api/players/?position=offence&limit=50&offset=0")
        
    assert position_response.status_code == 200
    data = position_response.json()

    assert data["total"] == 1  
    assert len(data["items"]) == 1
    assert data["items"][0]["position"] == "Offence"
    assert data["limit"] == 50
    assert data["offset"] == 0

    nationality_response = await client.get("/api/players/?nationality=spain&limit=50&offset=0")

    assert nationality_response.status_code == 200
    data = nationality_response.json()
    assert data["total"] == 2  
    assert len(data["items"]) == 2
    assert data["limit"] == 50
    assert data["offset"] == 0
