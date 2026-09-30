# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_infraprofile_configs as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


# ============================================================================
# Test ACTION Operations - Export
# ============================================================================


def test_action_export_all_profiles(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test exporting all profiles with no filters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "export",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    export_response = {"config": "exported-json-spec"}
    mock_client.post.return_value = _response(200, export_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["value"] == export_response
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/infraprofile/configs?action=export"
    # All body fields are optional, so an empty body is sent when none are set.
    assert call_args[1]["data"] == {}


def test_action_export_specific_profile(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test exporting a specific profile with a description."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "export",
            "profiles": ["ApplianceManagement"],
            "description": "Backup taken before upgrade",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {"config": "spec"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/infraprofile/configs?action=export"
    assert call_args[1]["data"]["profiles"] == ["ApplianceManagement"]
    assert call_args[1]["data"]["description"] == "Backup taken before upgrade"


# ============================================================================
# Test ACTION Operations - Validate
# ============================================================================


def test_action_validate(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test validating a configuration specification."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "validate",
            "config_spec": '{"profiles": []}',
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {"status": "VALID"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["value"] == {"status": "VALID"}
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/appliance/infraprofile/configs?action=validate&vmw-task=true"
    )
    assert call_args[1]["data"]["config_spec"] == '{"profiles": []}'


# ============================================================================
# Test ACTION Operations - Import
# ============================================================================


def test_action_import_with_profile_spec(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test importing a configuration specification with a nested profile_spec."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "import",
            "config_spec": '{"profiles": []}',
            "profile_spec": {
                "description": "Restore appliance configuration",
                "profiles": ["ApplianceManagement"],
                "encryption_key": None,
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/appliance/infraprofile/configs?action=import&vmw-task=true"
    )
    assert call_args[1]["data"]["config_spec"] == '{"profiles": []}'
    assert call_args[1]["data"]["profile_spec"]["description"] == (
        "Restore appliance configuration"
    )
    assert call_args[1]["data"]["profile_spec"]["profiles"] == ["ApplianceManagement"]
    # None-valued nested params are omitted from the built body.
    assert "encryption_key" not in call_args[1]["data"]["profile_spec"]


def test_action_import_without_profile_spec(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test importing with only the required config_spec."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "import",
            "config_spec": '{"profiles": []}',
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    call_args = mock_client.post.call_args
    assert call_args[1]["data"]["config_spec"] == '{"profiles": []}'
    assert "profile_spec" not in call_args[1]["data"]


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_export_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test export action in check mode does not call the API."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "export",
                "profiles": ["ApplianceManagement"],
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

    def test_import_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test import action in check mode does not call the API."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "import",
                "config_spec": '{"profiles": []}',
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

    def test_validate_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test validate action in check mode does not call the API."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "validate",
                "config_spec": '{"profiles": []}',
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
# Test Unsupported State
# ============================================================================


def test_unsupported_state_fails(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that an unsupported state calls fail_json."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    # A state value that is not in ACTION_OPERATIONS.
    module_args.update({"state": "bogus"})
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    mock_module.fail_json.assert_called_once()
    assert "Unsupported state" in exc.value.kwargs["msg"]


# ============================================================================
# Test Operation Configs
# ============================================================================


class TestOperationConfigs:
    """Test that the action OperationConfig objects build paths and bodies."""

    def test_export_config_build_body_empty(self):
        """Export builds an empty body when no optional params are set."""
        config = module_under_test.ACTION_OPERATIONS["export"]
        body = config.build_body(params={})
        assert body == {}

    def test_export_config_build_body(self):
        """Export includes only the optional params that are provided."""
        config = module_under_test.ACTION_OPERATIONS["export"]
        body = config.build_body(
            params={"profiles": ["ApplianceManagement"], "description": "d"}
        )
        assert body == {"profiles": ["ApplianceManagement"], "description": "d"}

    def test_import_config_build_path(self):
        """Import builds the expected static action path."""
        config = module_under_test.ACTION_OPERATIONS["import"]
        assert (
            config.build_path(params={})
            == "/appliance/infraprofile/configs?action=import&vmw-task=true"
        )

    def test_import_config_build_body_nested(self):
        """Import recurses into the profile_spec subspec."""
        config = module_under_test.ACTION_OPERATIONS["import"]
        body = config.build_body(
            params={
                "config_spec": "spec",
                "profile_spec": {
                    "description": "d",
                    "profiles": ["p1"],
                },
            }
        )
        assert body == {
            "config_spec": "spec",
            "profile_spec": {"description": "d", "profiles": ["p1"]},
        }


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
        assert module_under_test.ITEM_ENDPOINT == "/appliance/infraprofile/configs"

    def test_action_operations_keys(self):
        """Test that action operations are correctly defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "export",
            "import",
            "validate",
        }


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
        assert spec["state"]["choices"] == ["export", "import", "validate"]
        assert spec["state"]["required"] is True

    def test_create_module_argument_spec_config_spec(self):
        """Test that config_spec parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "config_spec" in spec
        assert spec["config_spec"]["type"] == "str"

    def test_create_module_argument_spec_profiles(self):
        """Test that profiles parameter is a list of strings."""
        spec = module_under_test.create_module_argument_spec()

        assert "profiles" in spec
        assert spec["profiles"]["type"] == "list"
        assert spec["profiles"]["elements"] == "str"

    def test_create_module_argument_spec_encryption_key_no_log(self):
        """Test that encryption_key is marked no_log."""
        spec = module_under_test.create_module_argument_spec()

        assert "encryption_key" in spec
        assert spec["encryption_key"]["no_log"] is True

    def test_create_module_argument_spec_profile_spec_suboptions(self):
        """Test that profile_spec is a dict with the expected suboptions."""
        spec = module_under_test.create_module_argument_spec()

        assert "profile_spec" in spec
        assert spec["profile_spec"]["type"] == "dict"
        suboptions = spec["profile_spec"]["options"]
        assert set(suboptions.keys()) == {
            "encryption_key",
            "description",
            "profiles",
        }
        assert suboptions["encryption_key"]["no_log"] is True
