"""Tests theme.py."""

import pytest

from nova.trame import ThemedApp, get_app


def test_theme_configuration() -> None:
    app = ThemedApp(vuetify_config_overrides={"primary": "#ff0000"})
    assert app.vuetify_config["theme"]["themes"]["CompactTheme"]["colors"]["primary"] == "#ff0000"


def test_set_theme() -> None:
    app = ThemedApp()
    app.set_theme("CompactTheme", force=True)
    assert app.state.nova__theme == "CompactTheme"
    try:
        app.set_theme("FakeTheme")
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert str(e).startswith("Theme 'FakeTheme' not found")


def test_inheritance() -> None:
    # [setup app]
    from trame.widgets import vuetify3 as vuetify
    from trame_server.core import Server

    class MyTrameApp(ThemedApp):
        def __init__(self, server: Server = None) -> None:
            super().__init__(server=server)

            self.create_ui()

        def create_ui(self) -> None:
            with super().create_ui() as layout:
                with layout.content:
                    vuetify.VBtn("Hello World")

    # [setup app complete]


def test_nav_drawer() -> None:
    from trame.widgets import vuetify3 as vuetify
    from trame_server.core import Server

    class MyTrameApp(ThemedApp):
        def __init__(self, server: Server = None) -> None:
            super().__init__(server=server)

            self.create_ui()

        def create_ui(self) -> None:
            with super().create_ui() as layout:
                with layout.content:
                    vuetify.VBtn("Hello World")

            with self.add_drawer(open=True, width=600):
                assert layout.drawer == 600


def test_get_app() -> None:
    app1 = ThemedApp()
    app2 = ThemedApp(name="test")

    assert app1 == get_app()
    assert app2 == get_app("test")


@pytest.mark.asyncio
async def test_client_disconnected() -> None:
    class MyTrameApp(ThemedApp):
        def __init__(self) -> None:
            super().__init__(name="disconnect_test")

            self.client_disconnect_timeout = 0.01
            self.disconnected = False

        async def on_client_disconnected(self) -> None:
            self.disconnected = True

    app = MyTrameApp()
    monitor = app._connection_monitor

    monitor.onConnect(None, "client_1")
    monitor.onConnect(None, "client_2")
    monitor.onClose("client_1")
    assert monitor._timeout_task is None  # Another client is still connected.

    monitor.onClose("client_2")
    assert monitor._timeout_task is not None  # The last client disconnected, so the timeout is now running.

    monitor.onConnect(None, "client_3")
    assert monitor._timeout_task is None  # The client reconnected, so the timeout was cancelled.

    monitor.onClose("client_3")
    assert monitor._timeout_task is not None
    await monitor._timeout_task  # Waiting on the task itself keeps this from racing the event loop.
    assert app.disconnected
