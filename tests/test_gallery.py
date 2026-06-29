"""Tries to create an instance of the gallery's App class."""

import pytest

from tests.gallery import App


@pytest.mark.asyncio
async def test_gallery() -> None:
    app = App()
    assert app.state.trame__title == "Widget Gallery"
