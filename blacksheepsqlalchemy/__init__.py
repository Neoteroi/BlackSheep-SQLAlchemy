from typing import Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    AsyncConnection,
)
from blacksheep.server import Application


def __configure_services(
    app: Application,
    engine: AsyncEngine,
    db_engine_alias: str,
    db_connection_alias: str,
    db_session_alias: str,
) -> None:
    # Note: pytest-cov generates false negatives for the following three functions
    # defined locally; they work and this is verified by tests

    async def dispose_engine(_):
        nonlocal engine
        await engine.dispose()

    app.on_stop += dispose_engine

    def connection_factory() -> AsyncConnection:
        return engine.connect()

    def session_factory() -> AsyncSession:
        return AsyncSession(engine, expire_on_commit=False)

    app.services.add_instance(engine)
    app.services.add_alias(db_engine_alias, AsyncEngine)

    app.services.add_scoped_by_factory(connection_factory)
    app.services.add_alias(db_connection_alias, AsyncConnection)

    app.services.add_scoped_by_factory(session_factory)
    app.services.add_alias(db_session_alias, AsyncSession)


def use_sqlalchemy(
    app: Application,
    *,
    connection_string: Optional[str] = None,
    echo: bool = False,
    engine: Optional[AsyncEngine] = None,
    db_engine_alias: str = "db_engine",
    db_connection_alias: str = "db_connection",
    db_session_alias: str = "db_session",
) -> None:
    """
    Configures the given application to use SQLAlchemy and provide services that can be
    injected in request handlers.
    """
    if engine is None:
        if not connection_string:
            raise TypeError(
                "Either pass a connection_string or an instance of "
                "sqlalchemy.ext.asyncio.AsyncEngine"
            )
        engine = create_async_engine(connection_string, echo=echo)

    assert engine is not None
    __configure_services(
        app, engine, db_engine_alias, db_connection_alias, db_session_alias
    )
