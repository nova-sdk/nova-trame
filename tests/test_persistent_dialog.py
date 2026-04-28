"""Unit tests for PersistentDialog."""

from trame.app import get_server
from trame_server.core import Server

from nova.trame.view.components import PersistentDialog
from nova.trame.view.theme import ThemedApp


def test_persistent_dialog() -> None:
    class MyTrameApp(ThemedApp):
        def __init__(self, server: Server = None) -> None:
            server = get_server(None, client_type="vue3")
            super().__init__(server=server)
            self.create_ui()

        def create_ui(self) -> None:
            with super().create_ui():
                dialog = PersistentDialog("config.test", max_width=500)
                assert dialog.v_model == "config.test"
                assert dialog.v_on_keydown_esc == "window.trame.state.state.config.test = false; flushState('config');"
                assert dialog.max_width == 500

                dialog = PersistentDialog("config.test2", close_on_escape=False, max_width=505)
                assert dialog.v_model == "config.test2"
                assert dialog.v_on_keydown_esc is None
                assert dialog.max_width == 505

    MyTrameApp()
