"""View implementation for PersistentDialog."""

from typing import Any, Tuple, Union
from warnings import warn

from trame.app import get_server
from trame.widgets import vuetify3 as vuetify
from trame_server.core import State

from nova.trame._internal.utils import get_state_name, get_state_param


class PersistentDialog(vuetify.VDialog):
    """Component for creating a Vuetify dialog that closes on the escape key but not outside clicks."""

    def __init__(
        self,
        v_model: Union[str, Tuple],
        close_on_escape: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructor for PersistentDialog.

        For all parameters, tuples have a special syntax. See :ref:`TrameTuple <api_trame_tuple>` for a description of
        it.

        Parameters
        ----------
        v_model : Union[str, Tuple]
            The state variable determining if the dialog is opened or closed.
        close_on_escape : bool
            If true, then the dialog will still close when the user presses the escape key. Defaults to true. This
            parameter does not support binding as dynamic behavior here would present a confusing user experience.
        **kwargs
            All other arguments will be passed to the underlying
            `Dialog component <https://trame.readthedocs.io/en/latest/trame.widgets.vuetify3.html#trame.widgets.vuetify3.VDialog>`_.

        Returns
        -------
        None
        """
        self._server = get_server(None, client_type="vue3")
        self._v_model = v_model
        self._field_name = get_state_param(self.state, v_model)
        self._model_name = get_state_name(self._field_name)

        if "persistent" in kwargs:
            warn(
                "PersistentDialog will ignore the provided 'persistent' parameter as it forces persistent=True.",
                stacklevel=1,
            )
            kwargs.pop("persistent", None)

        if close_on_escape:
            super().__init__(
                v_model=self._v_model,
                v_on_keydown_esc=(
                    f"window.trame.state.state.{self._field_name} = false; flushState('{self._model_name}');"
                ),
                persistent=True,
                **kwargs,
            )
        else:
            super().__init__(v_model=self._v_model, persistent=True, **kwargs)

    @property
    def state(self) -> State:
        return self._server.state
