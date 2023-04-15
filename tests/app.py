import sys
from dataclasses import dataclass
from typing import List

from sqlalchemy.sql.expression import select

import uvicorn
from blacksheep.messages import Response
from blacksheep.server import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from sqlalchemy import delete as sql_delete
from sqlalchemy import text

from blacksheepsqlalchemy import use_sqlalchemy
from tests.domain import Country

# hack to keep example code inside the tests folder without polluting the root folder
# of the repository
sys.path.append("../")

app = Application(show_error_details=True)

docs = OpenAPIHandler(info=Info(title="Example API", version="0.0.1"))
docs.bind_app(app)

use_sqlalchemy(app, connection_string="sqlite+aiosqlite:///example.db", echo=True)

get = app.router.get
post = app.router.post
delete = app.router.delete


@dataclass
class CreateCountryInput:
    id: str
    name: str


@dataclass
class CountryData:
    id: str
    name: str


@docs(tags=["db-connection"])
@post("/api/connection/countries")
async def create_country_1(db_connection, data: CreateCountryInput) -> Response:
    """
    Inserts a country using a database connection.
    """
    async with db_connection:
        await db_connection.execute(
            text("INSERT INTO country (id, name) VALUES (:id, :name)"),
            [{"id": data.id, "name": data.name}],
        )
        await db_connection.commit()
    return Response(201)


@docs(tags=["db-connection"])
@delete("/api/connection/countries/{country_id}")
async def delete_country_1(db_connection, country_id: str) -> Response:
    """
    Deletes a country by id using a database connection.
    """
    async with db_connection:
        await db_connection.execute(
            text("DELETE FROM country WHERE id = :id"),
            [{"id": country_id}],
        )
        await db_connection.commit()
    return Response(204)


@docs(tags=["db-connection"])
@get("/api/connection/countries")
async def get_countries_1(db_connection) -> List[CountryData]:
    """
    Fetches the countries using a database connection.
    """
    result = []
    async with db_connection:
        items = await db_connection.execute(text("SELECT * FROM country"))
        for item in items.fetchall():
            result.append(CountryData(item["id"], item["name"]))
    return result


@docs(tags=["ORM"])
@get("/api/orm/countries")
async def get_countries_2(db_session) -> List[CountryData]:
    """
    Fetches the countries using the ORM pattern.
    """
    result = []
    async with db_session:
        items = await db_session.execute(select(Country).order_by(Country.name))
        for item in items.fetchall():
            for country in item:
                result.append(CountryData(country.id, country.name))
    return result


@docs(tags=["ORM"])
@post("/api/orm/countries")
async def create_country_2(db_session, data: CreateCountryInput) -> Response:
    """
    Inserts a country using the ORM pattern.
    """
    async with db_session:
        db_session.add(Country(id=data.id, name=data.name))
        await db_session.commit()
    return Response(201)


@docs(tags=["ORM"])
@delete("/api/orm/countries/{country_id}")
async def delete_country_2(db_session, country_id: str) -> Response:
    """
    Deletes a country using the ORM pattern.
    """
    async with db_session:
        await db_session.execute(sql_delete(Country).where(Country.id == country_id))
        await db_session.commit()
    return Response(204)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=44566, log_level="debug")
