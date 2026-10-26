"""Monitors the websocket connections between the Trame server and its clients."""

import logging
from asyncio import CancelledError, Task, create_task, get_running_loop, sleep
from inspect import isawaitable
from typing import Any, Callable, Optional, Set

from wslink.websocket import LinkProtocol

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClientConnectionMonitor(LinkProtocol):
    """Calls a callback once no client has been connected to the server for a given duration.

    Trame's :code:`on_client_exited` lifecycle hook is sent by the browser as the page is unloaded, so it never fires
    when a connection simply drops (the user's machine goes to sleep, the network goes away, the tab is discarded).
    We watch the websocket connections directly instead so that any kind of disconnect is caught.

    The timeout is also started once the server is ready, so an application that nobody ever connects to will be
    cleaned up as well.
    """

    def __init__(self, timeout: float, callback: Callable[[], Any]) -> None:
        super().__init__()

        self.timeout = timeout
        self.callback = callback
        self._client_ids: Set[str] = set()
        self._timeout_task: Optional[Task] = None

    # wslink expects a camel-case name here :(
    def onConnect(self, request: Any, client_id: str) -> None:  # noqa: N802
        self._client_ids.add(client_id)
        self.cancel_timeout()

    # wslink expects a camel-case name here :(
    def onClose(self, client_id: str) -> None:  # noqa: N802
        self._client_ids.discard(client_id)
        self.schedule_timeout()

    def schedule_timeout(self) -> None:
        if self._client_ids:
            return  # We only count down while nobody is connected.

        self.cancel_timeout()

        try:
            get_running_loop()
        except RuntimeError:
            logger.warning("No running event loop, cannot monitor client disconnects.")
            return

        self._timeout_task = create_task(self._wait_for_timeout())

    def cancel_timeout(self) -> None:
        if self._timeout_task:
            self._timeout_task.cancel()
            self._timeout_task = None

    async def _wait_for_timeout(self) -> None:
        try:
            await sleep(self.timeout)
        except CancelledError:
            return  # A client reconnected before the timeout elapsed.

        try:
            result = self.callback()
            if isawaitable(result):
                await result
        except Exception as e:
            logger.error(f"Client disconnect callback failed: {e}")
