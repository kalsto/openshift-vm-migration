# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_monitoring_query module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module has a single access pattern: a GET against the static endpoint
``/appliance/monitoring/query``. The endpoint has no path template parameters
and the module defines no list operation, so it behaves like an item-only info
module whose payload is the queried time-series data.

Notes on the current implementation:
- ``_perform_get_operation()`` builds the query from ``GET_OPERATION``'s
  ``query_spec`` and issues ``client.get(path, query=...)``, so the required
  ``item`` and ``names`` module options are sent to the API as query parameters.
- ``MOID_PARAMETER_HINTS`` is empty and the returned item dicts key their
  identifier as ``name``, so the base class never derives a top-level ``id``.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_monitoring_query as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)


@pytest.fixture(autouse=True)
def patch_ansible_module():
    """Automatically patch AnsibleModule for all tests."""
    with patch.object(module_under_test, "AnsibleModule") as mock:
        yield mock


@pytest.fixture(autouse=True)
def patch_create_client():
    """Automatically patch _create_client for all tests."""
    with patch.object(
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(patch_ansible_module, mock_client, module_args, check_mode=False):
    """Helper: wire up the mocked module/client and return the mock module."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode
    return mock_module


SAMPLE_ITEM = {
    "name": "cpu.util",
    "interval": "MINUTES5",
    "function": "AVG",
    "start_time": "2026-01-01T00:00:00.000Z",
    "end_time": "2026-01-02T00:00:00.000Z",
    "data": ["3.5", "4.1", "2.9"],
}

MEM_ITEM = {
    "name": "mem.util",
    "interval": "MINUTES5",
    "function": "AVG",
    "start_time": "2026-01-01T00:00:00.000Z",
    "end_time": "2026-01-02T00:00:00.000Z",
    "data": ["512000", "524288", "530012"],
}

QUERY_ARGS = {
    "item": {
        "interval": "MINUTES5",
        "function": "AVG",
        "start_time": "2026-01-01T00:00:00.000Z",
        "end_time": "2026-01-02T00:00:00.000Z",
    },
    "names": ["cpu.util", "mem.util"],
}


# ============================================================================
# Test Query (GET) Operations
# ============================================================================


def test_query_multiple_items(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Query returning several monitored items yields a list for info and value."""
    patch_create_client.return_value = mock_client
    module_args.update(QUERY_ARGS)
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, [SAMPLE_ITEM, MEM_ITEM])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # Multiple results -> both info and value are the full list.
    assert result["info"] == [SAMPLE_ITEM, MEM_ITEM]
    assert result["value"] == [SAMPLE_ITEM, MEM_ITEM]
    # No recognizable MOID attribute, so no top-level id.
    assert "id" not in result


def test_query_single_item(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """A single-item result preserves the dict shape in value."""
    patch_create_client.return_value = mock_client
    module_args.update({"names": ["cpu.util"], "item": QUERY_ARGS["item"]})
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, [SAMPLE_ITEM])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # info is always a list; a single result yields exactly one element.
    assert result["info"] == [SAMPLE_ITEM]
    # value preserves the single-resource dict shape.
    assert result["value"] == SAMPLE_ITEM
    assert "id" not in result


def test_query_single_dict_response(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """A bare dict response is normalized into a single-element info list."""
    patch_create_client.return_value = mock_client
    module_args.update({"names": ["cpu.util"], "item": QUERY_ARGS["item"]})
    _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_ITEM)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["info"] == [SAMPLE_ITEM]
    assert result["value"] == SAMPLE_ITEM
    assert "id" not in result


def test_query_empty_result(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """An empty list result yields empty info and an empty value dict."""
    patch_create_client.return_value = mock_client
    module_args.update(QUERY_ARGS)
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


def test_query_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """A 404 from the query endpoint yields empty info and an empty value dict."""
    patch_create_client.return_value = mock_client
    module_args.update(QUERY_ARGS)
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_query_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Querying in check mode still performs the read."""
        patch_create_client.return_value = mock_client
        module_args.update(QUERY_ARGS)
        _run_module(patch_ansible_module, mock_client, module_args, check_mode=True)
        mock_client.get.return_value = _response(200, [SAMPLE_ITEM])

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_ITEM
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_query_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """The GET targets the static query endpoint exactly once."""
        patch_create_client.return_value = mock_client
        module_args.update(QUERY_ARGS)
        _run_module(patch_ansible_module, mock_client, module_args)
        mock_client.get.return_value = _response(200, [SAMPLE_ITEM])

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/appliance/monitoring/query"
        # The item and names options are sent as query parameters.
        assert call_args.kwargs["query"] == {
            "item": QUERY_ARGS["item"],
            "names": QUERY_ARGS["names"],
        }


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """This endpoint exposes no MOID parameter."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """There is no list endpoint for the query module."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/monitoring/query"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the query endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/appliance/monitoring/query"
        assert module_under_test.GET_OPERATION.http_method == "get"
        # The query parameters are declared on the GET operation.
        assert (
            module_under_test.GET_OPERATION.build_query(
                {"item": {"interval": "MINUTES5"}, "names": ["cpu.util"]}
            )
            is not None
        )


# ============================================================================
# Test OperationConfig path building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path building for this module."""

    def test_get_build_path_is_static(self):
        """The query path has no template parameters and is always static."""
        assert (
            module_under_test.GET_OPERATION.build_path({})
            == "/appliance/monitoring/query"
        )

    def test_get_build_path_ignores_extra_params(self):
        """Unrelated params do not change the static query path."""
        assert (
            module_under_test.GET_OPERATION.build_path({"names": ["cpu.util"]})
            == "/appliance/monitoring/query"
        )

    def test_get_build_query_includes_item_and_names(self):
        """The query spec maps the item and names options into query params."""
        query = module_under_test.GET_OPERATION.build_query(
            {
                "item": {
                    "interval": "MINUTES5",
                    "function": "AVG",
                    "start_time": "2026-01-01T00:00:00.000Z",
                    "end_time": "2026-01-02T00:00:00.000Z",
                },
                "names": ["cpu.util", "mem.util"],
            }
        )
        assert query == {
            "item": {
                "interval": "MINUTES5",
                "function": "AVG",
                "start_time": "2026-01-01T00:00:00.000Z",
                "end_time": "2026-01-02T00:00:00.000Z",
            },
            "names": ["cpu.util", "mem.util"],
        }


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec

    def test_create_module_argument_spec_names(self):
        """The names parameter is a required list of strings with an alias."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"
        assert spec["names"]["aliases"] == ["filter_names"]
        assert spec["names"].get("required", False) is True

    def test_create_module_argument_spec_item(self):
        """The item parameter is a required dict with the expected suboptions."""
        spec = module_under_test.create_module_argument_spec()

        assert "item" in spec
        assert spec["item"]["type"] == "dict"
        assert spec["item"].get("required", False) is True

        options = spec["item"]["options"]
        assert set(options) == {"interval", "function", "start_time", "end_time"}

        assert options["interval"]["required"] is True
        assert options["interval"]["choices"] == [
            "MINUTES30",
            "HOURS2",
            "MINUTES5",
            "DAY1",
            "HOURS6",
        ]

        assert options["function"]["required"] is True
        assert options["function"]["choices"] == ["COUNT", "MAX", "AVG", "MIN"]

        assert options["start_time"]["required"] is True
        assert options["end_time"]["required"] is True
