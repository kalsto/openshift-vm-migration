# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_localaccounts_globalpolicy module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This endpoint is a singleton: it
supports GET (read the current policy) and PUT (update the policy). There is
no create, delete, list, or MOID parameter, so ensure_present() always
resolves the existing singleton and updates it only when the desired values
differ from the current state.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_localaccounts_globalpolicy as module_under_test,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(patch_ansible_module, module_args, check_mode=False):
    """Helper: wire up the mocked Ansible module and return it."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = check_mode
    return mock_module


# ============================================================================
# Test UPDATE Operations
# ============================================================================


def test_update_policy(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating the global policy when the desired values differ."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "max_days": 90,
            "min_days": 1,
            "warn_days": 7,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    # Current policy differs from the desired values.
    mock_client.get.return_value = _response(
        200, {"max_days": 30, "min_days": 0, "warn_days": 5}
    )
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "max_days": {"before": 30, "after": 90},
        "min_days": {"before": 0, "after": 1},
        "warn_days": {"before": 5, "after": 7},
    }
    mock_client.put.assert_called_once()


def test_update_policy_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that no update happens when the policy already matches (idempotent)."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "max_days": 90,
            "min_days": 1,
            "warn_days": 7,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    # Current policy already matches the desired values.
    mock_client.get.return_value = _response(
        200, {"max_days": 90, "min_days": 1, "warn_days": 7}
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["diff"] == {}
    mock_client.put.assert_not_called()


def test_update_policy_partial(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating only a subset of the policy fields."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "minimum_length": 12,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(
        200, {"max_days": 90, "min_days": 1, "minimum_length": 8}
    )
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"minimum_length": {"before": 8, "after": 12}}
    # Only the supplied field is sent in the PUT body.
    mock_client.put.assert_called_once()
    call_args = mock_client.put.call_args
    assert call_args[1]["data"] == {"minimum_length": 12}


def test_update_policy_complexity_and_lockout(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating complexity and lockout related fields together."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "minimum_uppercase_char_count": 1,
            "minimum_special_char_count": 2,
            "failed_attempt_count_before_account_lockout": 3,
            "length_of_lockout_period_in_seconds": 1800,
            "managed_at_fleet": True,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(
        200,
        {
            "minimum_uppercase_char_count": 0,
            "minimum_special_char_count": 0,
            "failed_attempt_count_before_account_lockout": 5,
            "length_of_lockout_period_in_seconds": 300,
            "managed_at_fleet": False,
        },
    )
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "minimum_uppercase_char_count": {"before": 0, "after": 1},
        "minimum_special_char_count": {"before": 0, "after": 2},
        "failed_attempt_count_before_account_lockout": {"before": 5, "after": 3},
        "length_of_lockout_period_in_seconds": {"before": 300, "after": 1800},
        "managed_at_fleet": {"before": False, "after": True},
    }
    mock_client.put.assert_called_once()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating the policy in check mode reports change without PUT."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "max_days": 90,
            }
        )
        mock_module = _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, {"max_days": 30})

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {"max_days": {"before": 30, "after": 90}}
        # In check mode, no actual PUT should occur.
        mock_client.put.assert_not_called()

    def test_no_change_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test check mode with no changes reports no change."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "max_days": 30,
            }
        )
        mock_module = _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, {"max_days": 30})

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is False
        mock_client.put.assert_not_called()


# ============================================================================
# Test API Call Paths
# ============================================================================


class TestAPICallPath:
    """Test that the correct API paths are called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the singleton item endpoint."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "present", "max_days": 30})
        _run_module(patch_ansible_module, module_args)

        mock_client.get.return_value = _response(200, {"max_days": 30})

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/appliance/local-accounts/global-policy"

    def test_put_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that PUT uses the singleton item endpoint."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "present", "max_days": 90})
        _run_module(patch_ansible_module, module_args)

        mock_client.get.return_value = _response(200, {"max_days": 30})
        mock_client.put.return_value = _response(204, None)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.put.assert_called_once()
        call_args = mock_client.put.call_args
        assert call_args[0][0] == "/appliance/local-accounts/global-policy"


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are empty for this singleton."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """Test that there is no list endpoint."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT == "/appliance/local-accounts/global-policy"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/local-accounts/global-policy"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_operation_config(self):
        """Test that the UPDATE operation config targets the item endpoint."""
        assert (
            module_under_test.UPDATE_OPERATION.uri
            == "/appliance/local-accounts/global-policy"
        )
        assert module_under_test.UPDATE_OPERATION.http_method == "put"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_state(self):
        """Test that state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" in spec
        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present"]
        assert spec["state"]["default"] == "present"

    @pytest.mark.parametrize(
        "param_name",
        [
            "max_days",
            "min_days",
            "warn_days",
            "prior_password_remember_count",
            "failed_attempt_count_before_account_lockout",
            "length_of_lockout_period_in_seconds",
            "fail_interval_between_attempts",
            "minimum_length",
            "minimum_uppercase_char_count",
            "minimum_lowercase_char_count",
            "minimum_numerics_char_count",
            "minimum_special_char_count",
        ],
    )
    def test_int_params(self, param_name):
        """Test that the integer policy parameters are correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert param_name in spec
        assert spec[param_name]["type"] == "int"

    def test_managed_at_fleet_param(self):
        """Test that managed_at_fleet parameter is a boolean."""
        spec = module_under_test.create_module_argument_spec()

        assert "managed_at_fleet" in spec
        assert spec["managed_at_fleet"]["type"] == "bool"

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec
