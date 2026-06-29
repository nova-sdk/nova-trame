"""Help box for showing version and tool documentation."""

import os

from trame.widgets import html
from trame.widgets import vuetify3 as vuetify

TOOL_VERSION = os.getenv("NOVA_TOOL_VERSION", "")
DOCS_LINK = os.getenv("NOVA_TOOL_DOCS_LINK", "")


class HelpBox:
    """Help box for showing version and tool documentation."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        if not TOOL_VERSION and not DOCS_LINK:
            return

        with vuetify.VBtn(icon=True):
            vuetify.VIcon("mdi-help")

            with vuetify.VMenu(activator="parent", close_on_content_click=False):
                with vuetify.VCard(classes="pa-4"):
                    if TOOL_VERSION:
                        vuetify.VCardSubtitle(f"This tool is currently running version {TOOL_VERSION}.")
                    if DOCS_LINK:
                        with vuetify.VCardText(classes="pb-0"):
                            with vuetify.VBtn(href=DOCS_LINK, raw_attrs=['target="_blank"']):
                                vuetify.VIcon("mdi-open-in-new")
                                html.Span("View Documentation")
