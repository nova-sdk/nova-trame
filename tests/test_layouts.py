"""Unit tests for GridLayout, HBoxLayout, and VBoxLayout."""

from trame.widgets import html
from trame.widgets import vuetify3 as vuetify

from nova.trame.view.layouts import GridLayout, HBoxLayout, VBoxLayout


def test_grid() -> None:
    with GridLayout(columns=3, stretch=True):
        html.Div("Test 1")
        html.Div("Test 2", row_span=2, column_span=2)


def test_complex_layout() -> None:
    # [ setup complex layout example ]
    class LMRLayout:
        def __init__(self) -> None:
            with GridLayout(rows=1, columns=10, halign="center", valign="center"):
                self.left = html.Div(column_span=2)  # 20% width
                self.middle = html.Div(column_span=5)  # 50% width
                self.right = html.Div(column_span=3)  # 30% width

    my_layout = LMRLayout()
    with my_layout.left:
        vuetify.VBtn("Left Button")
    # [ setup complex layout example complete ]


def test_hbox() -> None:
    with HBoxLayout(stretch=True):
        html.Div("Test 1")
        html.Div("Test 2")


def test_vbox() -> None:
    with VBoxLayout(stretch=True):
        html.Div("Test 1")
        html.Div("Test 2")


def test_style_attributes() -> None:
    # Test dict-typed style
    with GridLayout(style={"height": "40px"}):
        html.Div("Test", style={"height": "100%"})
    with HBoxLayout(style={"height": "40px"}):
        html.Div("Test", style={"height": "100%"})
    with VBoxLayout(style={"height": "40px"}):
        html.Div("Test", style={"height": "100%"})

    # Test string-typed style
    with GridLayout(style="height: 40px"):
        html.Div("Test", style="height: 40px")
    with HBoxLayout(style="height: 40px"):
        html.Div("Test", style="height: 40px")
    with VBoxLayout(style="height: 40px"):
        html.Div("Test", style="height: 40px")


def test_child_overrides_are_rendered() -> None:
    # trame-client v4 only makes a child's kwargs readable after it has been connected to its parent, so the
    # layouts apply halign/valign/stretch/row_span/column_span at render time. Assert on the rendered markup
    # to make sure those overrides still land on the child.
    with GridLayout(columns=3) as grid:
        html.Div("A", row_span=2, column_span=2, halign="center")
        html.Div("B", stretch=True)

    markup = grid.html
    assert "grid-row-end: span 2;" in markup
    assert "grid-column-end: span 2;" in markup
    assert "justify-self: center;" in markup
    assert "flex-1-1" in markup

    with HBoxLayout() as hbox:
        html.Div("C", classes="mine", valign="end", stretch=False)

    markup = hbox.html
    assert "align-self: end;" in markup
    # The child's own classes must be preserved alongside the ones the layout adds.
    assert 'class="mine flex-0-1"' in markup

    # Rendering again must not re-apply the styling.
    assert hbox.html == markup
