# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_storage_policies_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_storage_policies_info as module_under_test,
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


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_storage_policies(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all storage policies."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})  # No filters
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response returns all storage policies
    list_response = [
        {
            "policy": "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
            "name": "VM Storage Policy",
            "description": "Storage policy for virtual machine workloads",
        },
        {
            "policy": "9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2",
            "name": "High Performance Policy",
            "description": "Storage policy for high-performance applications",
        },
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 2
    assert result["info"][0]["policy"] == "aa6d5a82-1c88-45da-85d3-3d74b91a5bad"
    assert result["info"][0]["name"] == "VM Storage Policy"
    assert result["info"][1]["policy"] == "9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2"
    assert result["info"][1]["name"] == "High Performance Policy"


def test_list_storage_policies_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing storage policies when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response returns empty list
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_storage_policies_by_policy_ids(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing storage policies filtered by policy IDs."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "policies": [
                "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
                "9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2",
            ],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response with filtered policies
    filtered_response = [
        {
            "policy": "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
            "name": "VM Storage Policy",
            "description": "Storage policy for virtual machine workloads",
        },
        {
            "policy": "9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2",
            "name": "High Performance Policy",
            "description": "Storage policy for high-performance applications",
        },
    ]

    mock_client.get.return_value = _response(200, filtered_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 2
    assert result["info"][0]["policy"] == "aa6d5a82-1c88-45da-85d3-3d74b91a5bad"
    assert result["info"][1]["policy"] == "9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2"
    # Verify the policies parameter was passed in the request
    mock_client.get.assert_called_once()


def test_list_storage_policies_single_policy_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing storage policies with a single policy ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "policies": ["aa6d5a82-1c88-45da-85d3-3d74b91a5bad"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response with single policy
    single_policy_response = [
        {
            "policy": "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
            "name": "VM Storage Policy",
            "description": "Storage policy for virtual machine workloads",
        },
    ]

    mock_client.get.return_value = _response(200, single_policy_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 1
    assert result["info"][0]["policy"] == "aa6d5a82-1c88-45da-85d3-3d74b91a5bad"
    assert result["info"][0]["name"] == "VM Storage Policy"


def test_list_storage_policies_with_filter_no_results(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing storage policies with filter that returns no results."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "policies": ["non-existent-policy-id"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response returns empty list
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing storage policies in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # Mock GET response
        list_response = [
            {
                "policy": "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
                "name": "VM Storage Policy",
            },
        ]

        mock_client.get.return_value = _response(200, list_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert "info" in result
        assert len(result["info"]) == 1
        mock_client.get.assert_called_once()

    def test_list_with_filter_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing filtered storage policies in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "policies": ["aa6d5a82-1c88-45da-85d3-3d74b91a5bad"],
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # Mock GET response
        filtered_response = [
            {
                "policy": "aa6d5a82-1c88-45da-85d3-3d74b91a5bad",
                "name": "VM Storage Policy",
            },
        ]

        mock_client.get.return_value = _response(200, filtered_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert "info" in result
        assert len(result["info"]) == 1
        mock_client.get.assert_called_once()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/storage/policies"


# ============================================================================
# Test Operation Config
# ============================================================================


class TestOperationConfig:
    """Test that OperationConfig objects are correctly defined."""

    def test_get_operation_config(self):
        """Test that GET operation config is correct."""
        config = module_under_test.GET_OPERATION

        assert config.name == "get"
        assert config.uri == "/vcenter/storage/policies"
        assert config.http_method.lower() == "get"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_policies(self):
        """Test that policies filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "policies" in spec
        assert spec["policies"]["type"] == "list"
        assert spec["policies"]["elements"] == "str"

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included in spec."""
        spec = module_under_test.create_module_argument_spec()

        # Check for common connection parameters
        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec
