"""Trame implementation of the HBoxLayout class."""

from typing import Any, Optional, Union
from warnings import warn

from trame.widgets import html
from trame_client.widgets.core import AbstractElement

from .utils import merge_styles


class HBoxLayout(html.Div):
    """Creates an element that horizontally stacks its children."""

    def __init__(
        self,
        height: Optional[Union[int, str]] = None,
        width: Optional[Union[int, str]] = None,
        halign: Optional[str] = None,
        valign: Optional[str] = None,
        gap: Optional[Union[int, str]] = "0em",
        vspace: Optional[Union[int, str]] = "0em",
        stretch: bool = False,
        **kwargs: Any,
    ) -> None:
        """Constructor for HBoxLayout.

        Parameters
        ----------
        height : optional[int | str]
            The height of this box. If an integer is provided, it is interpreted as pixels. If a string is provided,
            the string is treated as a CSS value.
        width : optional[int | str]
            The width of this box. If an integer is provided, it is interpreted as pixels. If a string is provided,
            the string is treated as a CSS value.
        halign : optional[str]
            The horizontal alignment of items in the grid. See `MDN
            <https://developer.mozilla.org/en-US/docs/Web/CSS/justify-items>`__ for available options.
        valign : optional[str]
            The vertical alignment of items in the grid. See `MDN
            <https://developer.mozilla.org/en-US/docs/Web/CSS/align-items>`__ for available options.
        gap : optional[str]
            The horizontal gap to place between items. Can be any CSS gap value (e.g. "4px" or "0.25em"). Defaults to no
            gap between items.
        vspace : optional[str]
            The vertical gap to place between items. Can be any CSS gap value (e.g. "4px" or "0.25em"). Defaults to no
            gap between items.
        stretch : optional[bool]
            If True, then this layout component will stretch to attempt to fill the space of it's parent container.
            Defaults to False.
        kwargs : Any
            Additional keyword arguments to pass to html.Div.

        Returns
        -------
        None

        Example
        -------
        .. literalinclude:: ../tests/gallery/views/app.py
            :start-after: setup hbox
            :end-before: setup hbox complete
            :dedent:
        """
        classes = kwargs.pop("classes", [])
        if isinstance(classes, list):
            classes = " ".join(classes)

        if stretch:
            classes += " flex-1-1 overflow-y-auto"
        else:
            classes += " flex-0-1"

        v_show = kwargs.get("v_show", None)
        if v_show:
            classes = (f"{v_show} ? '{classes} d-flex flex-row' : '{classes}'",)
        else:
            classes += " d-flex flex-row"

        widget_style = self.get_root_styles(height, width, halign, valign, gap, vspace)
        user_style = kwargs.pop("style", {})

        super().__init__(classes=classes, style=merge_styles(widget_style, user_style), **kwargs)

    def get_root_styles(
        self,
        height: Optional[Union[int, str]],
        width: Optional[Union[int, str]],
        halign: Optional[str],
        valign: Optional[str],
        gap: Optional[Union[int, str]],
        vspace: Optional[Union[int, str]],
    ) -> dict:
        height = f"{height}px" if isinstance(height, int) else height
        width = f"{width}px" if isinstance(width, int) else width
        gap = f"{gap}px" if isinstance(gap, int) else gap
        vspace = f"{vspace}px" if isinstance(vspace, int) else vspace

        styles = {}

        if height:
            styles["height"] = height
        if width:
            styles["width"] = width
        if halign:
            styles["justify-content"] = halign
        if valign:
            styles["align-items"] = valign
        if gap:
            styles["gap"] = gap
        if vspace:
            styles["margin-bottom"] = vspace

        return styles

    def add_child(self, child: Union[AbstractElement, str]) -> AbstractElement:
        """Add a child to the box.

        Do not call this directly. Instead, use Trame's `with` syntax, which will call this method internally. This
        method is documented here as a reference for the halign, stretch, and valign parameters.

        Parameters
        ----------
        child : `AbstractElement \
            <https://trame.readthedocs.io/en/latest/core.widget.html#trame_client.widgets.core.AbstractElement>`_ | str
            The child to add to the grid.
        halign : str
            NOTE: This parameter is valid at the box level but not for individual elements due to limitations in the CSS
            flexbox. Instead, you can use `VSpacer <https://trame.readthedocs.io/en/latest/trame.widgets.vuetify3.html>`__
            to add horizontal space between elements.
        stretch : bool
            Allows overriding the stretch parameter declared at the box level for a single child.
        valign : str
            Allows overriding the vertical alignment declared at the box level for a single child.

        Returns
        -------
        None

        Example
        -------
        .. literalinclude:: ../tests/gallery/views/app.py
            :start-after: grid row and column span example
            :end-before: grid row and column span example end
            :dedent:
        """
        if isinstance(child, str):
            child = html.Div(child)

        if "style" not in child._py_attr or child.style is None:
            child.style = ""
        if "classes" not in child._py_attr or child.classes is None:
            child.classes = ""

        if "halign" in child._py_attr:
            warn(
                (
                    "halign cannot change the horizontal alignment of individual elements in an HBoxLayout due to "
                    "limitations in the CSS flexbox. Instead, use `trame.widgets.vuetify3.VSpacer` in between your "
                    "elements to manipulate horizontal alignment."
                ),
                stacklevel=1,
            )
        if "stretch" in child._py_attr:
            if child.stretch:
                child.classes += " flex-1-1"
            else:
                child.classes += " flex-0-1"
        if "valign" in child._py_attr:
            child.style += f" align-self: {child.valign};"

        super().add_child(child)
