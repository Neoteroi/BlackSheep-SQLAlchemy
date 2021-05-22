from blacksheep.contents import JSONContent
import pytest
from .fixtures import *  # NoQA
from blacksheep.server import Application
from blacksheep.client import ClientSession
from blacksheepsqlalchemy import use_sqlalchemy


async def insert_fetch_delete_scenario(
    client_session: ClientSession, option: str, country_code: str, country_name: str
):
    response = await client_session.post(
        "/api/connection/countries",
        JSONContent({"id": country_code, "name": country_name}),
    )

    assert response.status == 201

    response = await client_session.get(f"/api/{option}/countries")

    assert response.status == 200

    countries = await response.json()

    country = next((item for item in countries if item["id"] == country_code), None)
    assert country is not None
    assert country["name"] == country_name

    response = await client_session.delete(f"/api/{option}/countries/{country_code}")

    assert response.status == 204

    response = await client_session.get(f"/api/{option}/countries")

    assert response.status == 200

    countries = await response.json()

    country = next((item for item in countries if item["id"] == country_code), None)
    assert country is None


@pytest.mark.asyncio
async def test_using_connection(client_session: ClientSession):
    await insert_fetch_delete_scenario(client_session, "connection", "jp", "Japan")


@pytest.mark.asyncio
async def test_using_orm(client_session: ClientSession):
    await insert_fetch_delete_scenario(client_session, "orm", "kr", "South Korea")


def test_throws_for_missing_engine_and_connection_string():
    app = Application()
    with pytest.raises(TypeError):
        use_sqlalchemy(app, connection_string="")

    with pytest.raises(TypeError):
        use_sqlalchemy(app, connection_string=None)
