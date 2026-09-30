# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_floppy_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_floppy_info as module_under_test,
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
# Test GET Operations (Single Resource)
# ============================================================================


def test_get_floppy_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific floppy drive by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "floppy": "8000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "floppy": "8000",
        "label": "Floppy drive 1",
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/boot.flp",
        },
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "8000"
    assert "value" in result
    assert result["value"]["label"] == "Floppy drive 1"
    assert result["value"]["backing"]["type"] == "IMAGE_FILE"
    assert result["value"]["start_connected"] is True


def test_get_floppy_with_host_device_backing(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a floppy drive with host device backing."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "floppy": "8001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "floppy": "8001",
        "label": "Floppy drive 2",
        "backing": {
            "type": "HOST_DEVICE",
            "host_device": "/dev/fd0",
        },
        "state": "NOT_CONNECTED",
        "start_connected": False,
        "allow_guest_control": False,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["id"] == "8001"
    assert result["value"]["backing"]["type"] == "HOST_DEVICE"
    assert result["value"]["backing"]["host_device"] == "/dev/fd0"


def test_get_floppy_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a floppy drive that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "floppy": "8999",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_floppy_drives(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all floppy drives on a VM."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"floppy": "8000"},
        {"floppy": "8001"},
    ]
    detail_response_1 = {
        "floppy": "8000",
        "label": "Floppy drive 1",
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/boot.flp",
        },
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
    }
    detail_response_2 = {
        "floppy": "8001",
        "label": "Floppy drive 2",
        "backing": {
            "type": "CLIENT_DEVICE",
        },
        "state": "NOT_CONNECTED",
        "start_connected": False,
        "allow_guest_control": False,
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response_1),
        _response(200, detail_response_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 2
    assert result["info"][0]["floppy"] == "8000"
    assert result["info"][1]["floppy"] == "8001"


def test_list_floppy_drives_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing floppy drives when none exist on the VM."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_single_floppy_drive(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when only one floppy drive exists."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"floppy": "8000"},
    ]
    detail_response = {
        "floppy": "8000",
        "label": "Floppy drive 1",
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/boot.flp",
        },
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["floppy"] == "8000"
    assert result["info"][0]["label"] == "Floppy drive 1"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a floppy drive in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1001",
                "floppy": "8000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "floppy": "8000",
            "label": "Floppy drive 1",
            "backing": {
                "type": "IMAGE_FILE",
                "image_file": "[datastore1] floppies/boot.flp",
            },
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["id"] == "8000"
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing floppy drives in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1001",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"floppy": "8000"},
        ]
        detail_response = {
            "floppy": "8000",
            "label": "Floppy drive 1",
        }

        mock_client.get.side_effect = [
            _response(200, list_response),
            _response(200, detail_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert "info" in result
        assert len(result["info"]) == 1


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm", "floppy"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm/{vm}/hardware/floppy"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/vcenter/vm/{vm}/hardware/floppy/{floppy}"
        )


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_vm(self):
        """Test that vm parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "vm" in spec
        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_floppy(self):
        """Test that floppy parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "floppy" in spec
        assert spec["floppy"]["type"] == "str"

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
