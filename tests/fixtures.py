from multiprocessing import Process
from time import sleep

import pytest
import uvicorn

from tests.utils import get_sleep_time

from .app import app


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
