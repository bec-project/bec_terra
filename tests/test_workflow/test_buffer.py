"""Module for testing the workflow buffer."""

import numpy as np
import pytest

from bec_terra.workflow.buffer import Buffer

# pylint: disable:redefined-outer-name


@pytest.fixture
def buffer():
    """Fixture to create a Buffer instance."""
    data_asset_id = "test_asset"
    data_asset = np.random.rand(10)
    buf = Buffer()
    buf.add_data_asset(data_asset_id, data_asset)
    yield buf


def test_has_data_asset(buffer):
    """Test adding a data asset to the buffer."""
    assert buffer.has_data_asset("test_asset") is True


def test_get_data_asset(buffer):
    """Test retrieving a data asset from the buffer."""
    data_asset = buffer.get_data_asset("test_asset")
    assert isinstance(data_asset, np.ndarray)


def test_add_data_asset(buffer):
    """Test adding a data asset to the buffer."""
    data_asset_id = "new_asset"
    data_asset = np.random.rand(10)
    buffer.add_data_asset(data_asset_id, data_asset)
    assert buffer.has_data_asset(data_asset_id) is True
    data_asset_retrieved = buffer.get_data_asset(data_asset_id)
    assert np.array_equal(data_asset_retrieved, data_asset) is True


def test_evict_data_asset(buffer):
    """Test evicting a data asset from the buffer."""
    data_asset_id = "test_asset"
    assert buffer.has_data_asset(data_asset_id) is True
    buffer.evict_data_asset(data_asset_id)
    assert buffer.has_data_asset(data_asset_id) is False
