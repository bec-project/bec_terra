"""Module for a thin message broker handling workflow messages within the Workflow engine."""

import queue
import threading
import uuid
from typing import Callable, Literal


class WorkflowBroker:
    """Message broker for handling workflow events and callbacks."""

    def __init__(self, logger=None):
        """Initialize the WorkflowBroker with a message queue."""
        self.event_queue = queue.Queue()
        self.event_registry: dict[str, list[Callable]] = {}
        self.callback_registry: dict[str, list[Callable]] = {}
        self._callback_thread = threading.Thread(target=self._process_events, daemon=True)
        self._callback_thread_event = threading.Event()
        self.logger = logger

    def _add_logs(self, message: str, loglevel: Literal["info", "warning", "debug"] = "info"):
        """Add logs to the logger if provided."""
        if self.logger:
            if loglevel == "info":
                self.logger.info(message)
            elif loglevel == "warning":
                self.logger.warning(message)
            elif loglevel == "debug":
                self.logger.debug(message)
        else:
            print(f"[{loglevel.upper()}] {message}")

    def start(self):
        """Start the callback processing thread."""
        if not self._callback_thread.is_alive():
            self._callback_thread.start()
        else:
            self._add_logs("Callback thread is already running.", loglevel="warning")

    def _process_events(self):
        """Process callback events from the queue."""
        while not self._callback_thread_event.is_set():
            try:
                event_id, file_reference, kwargs = self.event_queue.get(timeout=0.1)
                callbacks = self.callback_registry.get(event_id, [])
                for callback in callbacks:
                    try:
                        callback(file_reference, **kwargs)
                    except Exception as e:
                        self._add_logs(
                            f"Error executing callback for event {event_id}: {e}",
                            loglevel="warning",
                        )
            except queue.Empty:
                continue

    # TODO Do we want to have specific event types?
    def register_callback(self, event_id: str, callback: Callable) -> str:
        """Register a callback."""
        callback_id = str(uuid.uuid4())
        if event_id not in self.callback_registry:
            self.callback_registry[event_id] = []
        self.event_registry[callback_id] = callback
        self.callback_registry[event_id].append(callback)
        return callback_id

    def unregister_callback(self, callback_id: str) -> None:
        """Unregister a callback."""
        cb = self.event_registry.pop(callback_id, None)
        if cb is not None:
            for callbacks in self.callback_registry.values():
                if cb in callbacks:
                    callbacks.remove(cb)

    def publish_event(self, event_id: str, file_reference: str, **kwargs) -> None:
        """Publish an event to the broker."""
        event_data = (event_id, file_reference, kwargs)
        self._add_logs(f"Publishing event: {event_data}", loglevel="info")
        self.event_queue.put(event_data)
