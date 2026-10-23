"""pytest Fixture for setting up the Selenium driver and the server."""

from functools import partial
from http.client import HTTPConnection
from multiprocessing import Process
from time import monotonic, sleep
from typing import Generator

from pytest import fixture
from selenium.webdriver import Firefox, FirefoxOptions
from trame.app import get_server
from trame_client.widgets.core import HTML_CTX

from tests.gallery import main

SERVER_HOST = "localhost"
SERVER_PORT = 8080
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def _wait_for_server(timeout: float = 60.0) -> None:
    """Poll the gallery server until it serves a response.

    Startup time varies a lot with machine load, so we can't assume a fixed delay is enough.
    """
    deadline = monotonic() + timeout
    last_error: Exception = TimeoutError("server never started")

    while monotonic() < deadline:
        connection = HTTPConnection(SERVER_HOST, SERVER_PORT, timeout=1)
        try:
            connection.request("GET", "/index.html")
            connection.getresponse().read()
            return
        except OSError as e:  # Connection refused/reset while Trame is still coming up.
            last_error = e
            sleep(0.1)
        finally:
            connection.close()

    raise RuntimeError(f"Gallery server did not start within {timeout} seconds") from last_error


def _setup_selenium() -> Firefox:
    options = FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("--height=20000")

    driver = Firefox(options=options)
    driver.get(SERVER_URL)
    driver.implicitly_wait(10)

    return driver


@fixture(autouse=True, scope="session")
def driver() -> Generator[Firefox, None, None]:
    server_process = Process(target=partial(main, open_browser=False))
    server_process.start()

    _wait_for_server()

    driver = _setup_selenium()

    yield driver

    driver.quit()
    server_process.terminate()


@fixture(autouse=True)
def ambient_server() -> Generator[None, None, None]:
    """Publish a server for tests that build widgets outside of an app.

    As of trame-client v4 a widget resolves its rendering implementation from its server during __init__, so
    constructing one with no server in scope raises. Tests that drive the gallery through Selenium are
    unaffected; this only covers the ones that instantiate components directly.
    """
    previous = HTML_CTX._server
    HTML_CTX._server = get_server("tests", client_type="vue3")

    yield

    HTML_CTX._server = previous
