"""pytest Fixture for setting up the Selenium driver and the server."""

from functools import partial
from multiprocessing import Process
from time import sleep
from typing import Generator

from pytest import fixture
from selenium.webdriver import Firefox, FirefoxOptions
from trame.app import get_server
from trame_client.widgets.core import HTML_CTX

from tests.gallery import main


def _setup_selenium() -> Firefox:
    options = FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("--height=20000")

    driver = Firefox(options=options)
    driver.get("http://localhost:8080")
    driver.implicitly_wait(10)

    return driver


@fixture(autouse=True, scope="session")
def driver() -> Generator[Firefox, None, None]:
    server_process = Process(target=partial(main, open_browser=False))
    server_process.start()

    # TODO: Surely there's a better way to wait for the server to start.
    sleep(1)

    yield _setup_selenium()

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
