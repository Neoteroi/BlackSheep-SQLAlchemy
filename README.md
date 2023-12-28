[![Build](https://github.com/Neoteroi/BlackSheep-SQLAlchemy/actions/workflows/build.yml/badge.svg)](https://github.com/Neoteroi/BlackSheep-SQLAlchemy/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/BlackSheep-SQLAlchemy.svg?color=blue)](https://pypi.org/project/BlackSheep-SQLAlchemy/)
[![versions](https://img.shields.io/pypi/pyversions/blacksheep-sqlalchemy.svg)](https://github.com/Neoteroi/BlackSheep-SQLAlchemy/)
[![license](https://img.shields.io/github/license/Neoteroi/blacksheep-sqlalchemy.svg)](https://github.com/Neoteroi/BlackSheep-SQLAlchemy/blob/main/LICENSE)

# BlackSheep-SQLAlchemy
Extension for [BlackSheep](https://github.com/Neoteroi/BlackSheep) that
simplifies the use of SQLAlchemy in the web framework.

```bash
pip install blacksheep-sqlalchemy
```

**Important:** this library only supports `rodi` dependency injection
container. However, the implementation can be used for reference to configure
other DI containers to work with SQLAlchemy.

## How to use

```python
from blacksheep.server import Application
from blacksheepsqlalchemy import use_sqlalchemy

app = Application()

use_sqlalchemy(app, connection_string="<CONNECTION_STRING>")

```

After registering SQLAlchemy, services are configured in the application, so
they are automatically resolved in any request handler requiring a SQLAlchemy
db connection or db session; for example:

```python

@get("/api/countries")
async def get_countries(db_connection) -> List[CountryData]:
    """
    Fetches the countries using a database connection.
    """
    result = []
    async with db_connection:
        items = await db_connection.execute(text("SELECT * FROM country"))
        for item in items.fetchall():
            result.append(CountryData(item["id"], item["name"]))
    return result

```

Services can be injected at any level of the resolution graph, so `BlackSheep`
and `rodi` support out of the box the scenario of db connections or db sessions
referenced in the business logic but not directly by the front-end layer
(depending on programmers' preference and their notion of best practices when
building web apps).

Services can be injected in the following ways:

| By alias      | By type annotation | Value                                               |
| ------------- | ------------------ | --------------------------------------------------- |
| db_connection | AsyncConnection    | instance of AsyncConnection (scoped to web request) |
| db_session    | AsyncSession       | instance of AsyncSession (scoped to web request)    |
| db_engine     | AsyncEngine        | instance of AsyncEngine (singleton)                 |

---

For example, using SQLite:

* requires driver: `pip install aiosqlite`
* connection string: `sqlite+aiosqlite:///example.db`

See the `tests` folder for a [working example](https://github.com/Neoteroi/BlackSheep-SQLAlchemy/blob/main/tests/app.py)
using database migrations applied with `Alembic`, and a documented API that offers methods to fetch, create,
delete countries objects.

---

### Note
BlackSheep is designed to be used in `async` way, therefore this library
requires the use of an asynchronous driver.

## References

* [SQLAlchemy - support for asyncio](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)

## Documentation
Please refer to the [documentation website](https://www.neoteroi.dev/blacksheep/).
