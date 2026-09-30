# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_floppy CRUD module.

Tests validate the module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_floppy as module_under_test,
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


# ============================================================================
# Test CREATE Operations
# ============================================================================


def test_create_floppy_with_image_backing(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a new floppy drive backed by an image file."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8000",
            "backing": {
                "type": "IMAGE_FILE",
                "image_file": "[datastore1] floppies/boot.flp",
            },
            "start_connected": True,
            "allow_guest_control": True,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)
    mock_client.post.return_value = _response(201, "8000")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "8000"
    mock_client.post.assert_called_once()


def test_create_floppy_with_client_device(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a new floppy drive backed by a client device."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8001",
            "backing": {
                "type": "CLIENT_DEVICE",
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)
    mock_client.post.return_value = _response(201, "8001")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "8001"
    mock_client.post.assert_called_once()


def test_create_floppy_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a floppy drive that already exists with same state (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8000",
            "backing": {
                "type": "IMAGE_FILE",
                "image_file": "[datastore1] floppies/boot.flp",
            },
            "start_connected": True,
            "allow_guest_control": True,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/boot.flp",
        },
        "start_connected": True,
        "allow_guest_control": True,
    }

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "8000"
    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test UPDATE Operations
# ============================================================================


def test_update_floppy_allow_guest_control(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a floppy drive's allow_guest_control setting."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8000",
            "allow_guest_control": False,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "allow_guest_control": True,
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "8000"
    assert result["diff"] == {"allow_guest_control": {"before": True, "after": False}}
    mock_client.patch.assert_called_once()


def test_update_floppy_backing(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a floppy drive's backing configuration."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8000",
            "backing": {
                "type": "IMAGE_FILE",
                "image_file": "[datastore1] floppies/new.flp",
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/old.flp",
        },
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "8000"
    assert "diff" in result
    assert "backing" in result["diff"]
    mock_client.patch.assert_called_once()


def test_update_floppy_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a floppy drive with no changes (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "floppy": "8000",
            "start_connected": True,
            "allow_guest_control": False,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "start_connected": True,
        "allow_guest_control": False,
    }

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "8000"
    mock_client.patch.assert_not_called()


# ============================================================================
# Test DELETE Operations
# ============================================================================


def test_delete_floppy(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a floppy drive."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "vm": "vm-1001",
            "floppy": "8000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "backing": {
            "type": "IMAGE_FILE",
            "image_file": "[datastore1] floppies/boot.flp",
        },
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware/floppy/8000"


def test_delete_floppy_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a floppy drive that doesn't exist (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
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
    assert result["changed"] is False
    mock_client.delete.assert_not_called()


# ============================================================================
# Test ACTION Operations (connect / disconnect)
# ============================================================================


def test_connect_floppy(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test connecting a floppy drive."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "connect",
            "vm": "vm-1001",
            "floppy": "8000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.post.assert_called_once()


def test_disconnect_floppy(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test disconnecting a floppy drive."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "disconnect",
            "vm": "vm-1001",
            "floppy": "8000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.post.assert_called_once()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test creating a floppy drive in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "vm": "vm-1001",
                "floppy": "8000",
                "backing": {
                    "type": "IMAGE_FILE",
                    "image_file": "[datastore1] floppies/boot.flp",
                },
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(404, None)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating a floppy drive in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "vm": "vm-1001",
                "floppy": "8000",
                "allow_guest_control": True,
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        current_state = {
            "allow_guest_control": False,
        }

        mock_client.get.return_value = _response(200, current_state)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {
            "allow_guest_control": {"before": False, "after": True}
        }
        mock_client.patch.assert_not_called()

    def test_delete_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test deleting a floppy drive in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "absent",
                "vm": "vm-1001",
                "floppy": "8000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        current_state = {
            "backing": {"type": "IMAGE_FILE"},
        }

        mock_client.get.return_value = _response(200, current_state)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.delete.assert_not_called()

    def test_connect_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test connecting a floppy drive in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "connect",
                "vm": "vm-1001",
                "floppy": "8000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()

    def test_disconnect_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test disconnecting a floppy drive in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "disconnect",
                "vm": "vm-1001",
                "floppy": "8000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()


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

    def test_create_module_argument_spec_state(self):
        """Test that state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" in spec
        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == [
            "present",
            "absent",
            "connect",
            "disconnect",
        ]
        assert spec["state"]["default"] == "present"

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

    def test_create_module_argument_spec_backing(self):
        """Test that backing parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "backing" in spec
        assert spec["backing"]["type"] == "dict"
        assert "options" in spec["backing"]
        assert "type" in spec["backing"]["options"]
        assert spec["backing"]["options"]["type"]["choices"] == [
            "IMAGE_FILE",
            "HOST_DEVICE",
            "CLIENT_DEVICE",
        ]
        assert "image_file" in spec["backing"]["options"]
        assert "host_device" in spec["backing"]["options"]

    def test_create_module_argument_spec_start_connected(self):
        """Test that start_connected parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "start_connected" in spec
        assert spec["start_connected"]["type"] == "bool"

    def test_create_module_argument_spec_allow_guest_control(self):
        """Test that allow_guest_control parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "allow_guest_control" in spec
        assert spec["allow_guest_control"]["type"] == "bool"
