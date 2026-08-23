import pytest
from httpx import AsyncClient
from tests.conftest import auth_header, create_test_admin, login_admin, create_test_user, login_user
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.anyio
async def test_update_player_by_id_success(client: AsyncClient, db_session: AsyncSession):
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
        json={"name": "Test", "position": "Goalkeeper", "dateOfBirth": "1973-08-11", "nationality": "France", "team_id": team_id},
        headers=headers
    )

    assert player_response.status_code == 201
    player_id = player_response.json()["id"]

    update_response = await client.patch(
        f"/api/admin/players/{player_id}",
        json={
            "name": "Franc Lampdard",
            "position": "Offence",
            "dateOfBirth": "1973-09-11",
            "nationality": "England"
        },
        headers=headers
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Franc Lampdard"
    assert data["position"] == "Offence"
    assert data["dateOfBirth"] == "1973-09-11"
    assert data["nationality"] == "England"

@pytest.mark.anyio
async def test_update_by_non_uthorized(client: AsyncClient):
    update_response = await client.patch(
        "/api/admin/players/99999"
    )
        
    assert update_response.status_code == 401

@pytest.mark.anyio
async def test_update_by_non_admin(client:AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    update_response = await client.patch(
        "/api/admin/players/99999",
        headers=headers
    )
        
    assert update_response.status_code == 403

@pytest.mark.anyio
async def test_update_player_by_id_negative(client: AsyncClient, db_session: AsyncSession):
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
        json={"name": "Test", "position": "Goalkeeper", "dateOfBirth": "1973-08-11", "nationality": "France", "team_id": team_id},
        headers=headers
    )

    assert player_response.status_code == 201
    player_id = player_response.json()["id"]

    name_update_response = await client.patch(
        f"/api/admin/players/{player_id}",
        json={
            "name": {"name": "New_name"}
        },
        headers=headers
    )

    assert name_update_response.status_code == 422

    position_update_response = await client.patch(
            f"/api/admin/players/{player_id}",
            json={
                "position": "Offense"
            },
            headers=headers
        )
    
    assert position_update_response.status_code == 422

    date_update_response = await client.patch(
            f"/api/admin/players/{player_id}",
            json={
                "dateOfBirth": "not_a_date"
            },
            headers=headers
        )
    
    assert date_update_response.status_code == 422

    nationality_update_response = await client.patch(
            f"/api/admin/players/{player_id}",
            json={
                "nationality": {"country": "France"}
            },
            headers=headers
        )
    
    assert nationality_update_response.status_code == 422

@pytest.mark.anyio
async def test_delete_player_by_admin(client: AsyncClient, db_session: AsyncSession):
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
        json={"name": "Test", "position": "Goalkeeper", "dateOfBirth": "1973-08-11", "nationality": "France", "team_id": team_id},
        headers=headers
    )

    assert player_response.status_code == 201
    player_id = player_response.json()["id"]

    delete_response = await client.delete(
        f"/api/admin/players/{player_id}",
        headers=headers 
    )

    assert delete_response.status_code == 204
    get_response = await client.get(f"/api/players/{player_id}")
    assert get_response.status_code == 404

@pytest.mark.anyio
async def test_delete_non_existing_player(client: AsyncClient, db_session: AsyncSession):
    await create_test_admin(client, db_session)
    token = await login_admin(client)
    headers = auth_header(token)

    delete_response = await client.delete(
            "/api/admin/players/99999",
            headers=headers
        )
            
    assert delete_response.status_code == 404


@pytest.mark.anyio
async def test_delete_by_non_uthorized(client: AsyncClient):
    delete_response = await client.delete(
        "/api/admin/players/99999"
    )
        
    assert delete_response.status_code == 401

@pytest.mark.anyio
async def test_delete_by_non_admin(client:AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    delete_response = await client.delete(
        "/api/admin/players/99999",
        headers=headers
    )
        
    assert delete_response.status_code == 403


            