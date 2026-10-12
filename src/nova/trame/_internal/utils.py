"""Internal utilities for nova-trame."""

from typing import Any, Tuple, Union

from trame_client.widgets.core import AbstractElement
from trame_server.core import State

from nova.mvvm._internal.utils import rgetdictvalue, rsetdictvalue


# Trame state handlers don't work on nested properties. When writing Trame state handlers (e.g. flushState, dirty, or
# change), we instead use the name of the top-level property. For example, "config.parameter_group_a.option_x" becomes
# "config".
def get_state_name(name: str) -> str:
    return name.split(".")[0]


# Reads a state parameter from Trame. For internal use only, if you're using this in your application you're violating
# the MVVM framework. :)
def get_state_param(state: State, value: Union[Any, Tuple]) -> Any:
    if isinstance(value, tuple):
        return rgetdictvalue(state, value[0])

    return value


# Reads a keyword argument that was passed to a Trame widget, returning `default` if it wasn't passed or was passed
# as None. Trame v4 moved these off of the widget itself and onto a per-client-type rendering implementation, so we
# check both locations. Reading one as an attribute instead would log "<Widget>.<name> is missing" under v4.
def get_widget_kwarg(widget: AbstractElement, name: str, default: Any = None) -> Any:
    impl = getattr(widget, "_impl", None)  # Trame v4
    if impl is not None:
        value = impl.get(name) if impl.has(name) else None
    else:  # Trame v3
        value = widget._py_attr.get(name)

    return default if value is None else value


# Writes a state parameter to Trame. For internal use only, if you're using this in your application you're violating
# the MVVM framework. :)
def set_state_param(state: State, value: Union[Any, Tuple], new_value: Any = None) -> Any:
    with state:
        if isinstance(value, tuple):
            if new_value is not None:
                rsetdictvalue(state, value[0], new_value)
            elif len(value) > 1:
                rsetdictvalue(state, value[0], value[1])
            state.dirty(get_state_name(value[0]))

    return get_state_param(state, value)
