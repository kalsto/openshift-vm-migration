# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_localaccounts_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module supports two access patterns:
- GET a single local account by ``username`` (``/appliance/local-accounts/{username}``).
- LIST all local accounts (``/appliance/local-accounts``) when no ``username`` is given.

The LIST endpoint returns an array of identifier *strings* (usernames). The
shared ``_list_resource_details()`` helper maps each identifier onto the get
operation's ``{username}`` path parameter, then fetches per-account details and
merges the identifier back into each result.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_localaccounts_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
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
    mock_module.check_mode = check_mode
    return mock_module


SAMPLE_ACCOUNT = {
    "fullname": "Root User",
    "email": "root@example.com",
    "roles": ["superAdmin"],
    "enabled": True,
    "has_password": True,
    "min_days_between_password_change": 1,
    "max_days_between_password_change": 90,
    "warn_days_before_password_expiration": 7,
}


# ============================================================================
# Test GET Operations (single account by username)
# ============================================================================


def test_get_account_by_username(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific local account by username."""
    patch_create_client.return_value = mock_client
    module_args.update({"username": "root"})
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_ACCOUNT)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # value preserves the single-resource dict shape.
    assert result["value"] == SAMPLE_ACCOUNT
    # info is always a list; the single account yields exactly one element.
    assert result["info"] == [SAMPLE_ACCOUNT]
    # The account payload carries no username/resource_id key, so no id is set.
    assert "id" not in result


def test_get_account_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting an account when the endpoint returns 404."""
    patch_create_client.return_value = mock_client
    module_args.update({"username": "ghost"})
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
# Test LIST Operations
# ============================================================================


def test_list_all_accounts(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all accounts when no username is given.

    ``GET /appliance/local-accounts`` returns identifier strings; each is
    mapped onto the get operation's path parameter, fetched for details, and
    the identifier is merged back into the result.
    """
    patch_create_client.return_value = mock_client
    # No username -> falls back to the LIST endpoint.
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)

    root_detail = {"enabled": True, "roles": ["superAdmin"], "has_password": True}
    test_detail = {"enabled": False, "roles": ["operator"], "has_password": True}
    # First call: LIST (strings), then a detail GET for each identifier.
    mock_client.get.side_effect = [
        _response(200, ["root", "test-user"]),
        _response(200, root_detail),
        _response(200, test_detail),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # Listing yields a list for both info and value.
    assert result["info"] == [
        {"username": "root", **root_detail},
        {"username": "test-user", **test_detail},
    ]
    assert result["value"] == result["info"]
    # A list result has no single id.
    assert "id" not in result

    # The correct list + detail paths were queried in order.
    paths = [call.args[0] for call in mock_client.get.call_args_list]
    assert paths == [
        "/appliance/local-accounts",
        "/appliance/local-accounts/root",
        "/appliance/local-accounts/test-user",
    ]


def test_list_accounts_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when no local accounts exist."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == []
    assert "id" not in result


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting an account in check mode still performs the read."""
        patch_create_client.return_value = mock_client
        module_args.update({"username": "root"})
        mock_module = _run_module(
            patch_ansible_module, mock_client, module_args, check_mode=True
        )
        mock_client.get.return_value = _response(200, SAMPLE_ACCOUNT)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_ACCOUNT
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the correct item API path."""
        patch_create_client.return_value = mock_client
        module_args.update({"username": "root"})
        _run_module(patch_ansible_module, mock_client, module_args)
        mock_client.get.return_value = _response(200, SAMPLE_ACCOUNT)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/appliance/local-accounts/root"


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hint is the username."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["username"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/appliance/local-accounts"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/local-accounts/{username}"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/local-accounts/{username}"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation_config(self):
        """Test that the LIST operation config targets the list endpoint."""
        assert module_under_test.LIST_OPERATION.uri == "/appliance/local-accounts"
        assert module_under_test.LIST_OPERATION.http_method == "get"


# ============================================================================
# Test OperationConfig path building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path building for this module."""

    def test_get_build_path_with_username(self):
        """GET path is populated from the username parameter."""
        path = module_under_test.GET_OPERATION.build_path({"username": "root"})
        assert path == "/appliance/local-accounts/root"

    def test_get_build_path_missing_username_raises(self):
        """GET path building requires the username path parameter."""
        from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
            RequiredPathParameterError,
        )

        with pytest.raises(RequiredPathParameterError):
            module_under_test.GET_OPERATION.build_path({})

    def test_list_build_path_is_static(self):
        """LIST path has no template parameters."""
        assert (
            module_under_test.LIST_OPERATION.build_path({})
            == "/appliance/local-accounts"
        )


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

    def test_create_module_argument_spec_username(self):
        """Test that the username parameter is defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert "username" in spec
        assert spec["username"]["type"] == "str"
        assert not spec["username"].get("required", False)

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
