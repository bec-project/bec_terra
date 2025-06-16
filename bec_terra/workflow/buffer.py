"""Module for Python based Buffer class handling data assets in a workflow."""

from __future__ import annotations

from logging import getLogger
from typing import Any

logger = getLogger(__name__)


class Buffer:
    """Buffer class for storing and managing data assets in a workflow."""

    def __init__(self, buffer: dict | None = None):
        """Initialize the Buffer with an optional buffer."""
        self.buffer = buffer if buffer is not None else {}

    def add_data_asset(self, data_asset_id: str, data_asset: Any) -> None:
        """Add a data asset to the buffer."""
        if data_asset_id in self.buffer:
            raise ValueError(f"Data asset {data_asset_id} already exists in the buffer.")
        self.buffer[data_asset_id] = data_asset

    def get_data_asset(self, data_asset_id: str) -> Any:
        """Retrieve a data asset from the buffer."""
        if data_asset_id not in self.buffer:
            raise KeyError(f"Data asset {data_asset_id} not found in the buffer.")
        return self.buffer[data_asset_id]

    def has_data_asset(self, data_asset_id: str) -> bool:
        """Check if a data asset exists in the buffer."""
        return data_asset_id in self.buffer

    def evict_data_asset(self, data_asset_id: str) -> None:
        """Evict a data asset from the buffer."""
        if self.has_data_asset(data_asset_id):
            del self.buffer[data_asset_id]
        else:
            raise KeyError(f"Data asset {data_asset_id} not found in the buffer.")
