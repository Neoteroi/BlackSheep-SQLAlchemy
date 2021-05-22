import asyncio
from multiprocessing import Process
from time import sleep

import pytest
import uvicorn
from blacksheep.client import ClientSession
from blacksheep.client.pool import ClientConnectionPools

from tests.utils import get_sleep_time

from .app import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for all test cases."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client_session(server_host, server_port, event_loop):
    # It is important to pass the instance of ClientConnectionPools,
    # to ensure that the connections are reused and closed
    session = ClientSession(
        loop=event_loop,
        base_url=f"http://{server_host}:{server_port}",
        pools=ClientConnectionPools(event_loop),
    )
    yield session
    asyncio.run(session.close())


@pytest.fixture(scope="module")
def server_host():
    return "127.0.0.1"


@pytest.fixture(scope="module")
def server_port():
    return 44555


@pytest.fixture(scope="module")
def connection_string():
    return "sqlite:///example.db"


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=44555, log_level="debug")


@pytest.fixture(scope="module", autouse=True)
def server(server_host, server_port):
    server_process = Process(target=start_server)
    server_process.start()
    sleep(get_sleep_time())

    yield 1

    sleep(1.2)
    server_process.terminate()
