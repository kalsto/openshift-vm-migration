# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ...common.utils import (  # pylint: disable=unused-import
    AnsibleFailJson,
    CONNECTION_PARAMS,
    fail_json,
    mock_client,
)


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.params = CONNECTION_PARAMS
    module.fail_json = fail_json
    return module


@pytest.fixture
def info_module(mock_module, mock_client):
    list_path = "/vcenter/resource-pool"
    item_path = "/vcenter/resource-pool/{resource_pool}"

    get_operation_config = OperationConfig(
        name="get",
        uri=item_path,
        http_method="get",
    )

    list_operation_config = OperationConfig(
        name="list",
        uri=list_path,
        http_method="get",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module_instance = VmwareRestInfoModuleBase(
            module=mock_module,
            moid_parameter_hints=["resource_pool"],
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )

    return module_instance


def test_info_module_initialization(info_module):
    assert info_module.list_operation_config.uri == "/vcenter/resource-pool"
    assert (
        info_module.get_operation_config.uri == "/vcenter/resource-pool/{resource_pool}"
    )
    assert "resource_pool" in info_module.moid_parameter_hints


def test_normalize_info_results_single_resource(info_module):
    # single_resource=True: value is the single dict and id is extracted from it
    query_results = [{"resource_pool": "pool-1", "name": "my_pool"}]
    result = info_module.normalize_info_results(query_results, single_resource=True)

    assert result["id"] == "pool-1"
    assert result["value"] == {"resource_pool": "pool-1", "name": "my_pool"}
    assert result["info"] == [{"resource_pool": "pool-1", "name": "my_pool"}]


def test_normalize_info_results_single_resource_without_moid(info_module):
    # single_resource=True but the resource has no recognizable MOID attribute:
    # value is still a dict, but no id key is added
    query_results = [{"name": "my_pool"}]
    result = info_module.normalize_info_results(query_results, single_resource=True)

    assert "id" not in result
    assert result["value"] == {"name": "my_pool"}
    assert result["info"] == [{"name": "my_pool"}]


def test_normalize_info_results_single_resource_non_dict(info_module):
    # single_resource=True with a bare scalar (e.g. appliance health status string):
    # value preserves the scalar and no id is added
    query_results = ["green"]
    result = info_module.normalize_info_results(query_results, single_resource=True)

    assert "id" not in result
    assert result["value"] == "green"
    assert result["info"] == ["green"]


def test_normalize_info_results_multiple_items(info_module):
    # single_resource=False: value preserves the list shape and no id is added
    query_results = [
        {"resource_pool": "pool-1", "name": "pool_1"},
        {"resource_pool": "pool-2", "name": "pool_2"},
    ]
    result = info_module.normalize_info_results(query_results, single_resource=False)

    assert "id" not in result
    assert result["value"] == query_results
    assert result["info"] == query_results


def test_normalize_info_results_empty_single_resource(info_module):
    # single_resource=True with no results: value is an empty dict
    result = info_module.normalize_info_results([], single_resource=True)

    assert result == {"info": [], "value": {}}


def test_normalize_info_results_empty_list(info_module):
    # single_resource=False with no results: value is an empty list
    result = info_module.normalize_info_results([], single_resource=False)

    assert result == {"info": [], "value": []}


def test_normalize_info_results_rejects_non_list(info_module):
    with pytest.raises(AnsibleFailJson):
        info_module.normalize_info_results({"not": "a list"}, single_resource=True)


def test_list_resource_details_success(info_module, mock_client):
    # Mock list operation returning resource summaries
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1"},
        {"resource_pool": "pool-2"},
    ]

    # Mock get operations for each resource
    get_response_1 = MagicMock()
    get_response_1.status = 200
    get_response_1.json = {
        "resource_pool": "pool-1",
        "name": "pool_1",
        "cpu_allocation": {},
    }

    get_response_2 = MagicMock()
    get_response_2.status = 200
    get_response_2.json = {
        "resource_pool": "pool-2",
        "name": "pool_2",
        "memory_allocation": {},
    }

    mock_client.get.side_effect = [get_response_1, get_response_2]

    # Mock the _perform_list_operation to return the summaries
    with patch.object(
        info_module,
        "_perform_list_operation",
        return_value=[{"resource_pool": "pool-1"}, {"resource_pool": "pool-2"}],
    ):
        result = info_module._list_resource_details()

    assert len(result) == 2
    assert result[0] == {
        "resource_pool": "pool-1",
        "name": "pool_1",
        "cpu_allocation": {},
    }
    assert result[1] == {
        "resource_pool": "pool-2",
        "name": "pool_2",
        "memory_allocation": {},
    }


def test_list_resource_details_handles_404(info_module, mock_client, mock_module):
    # Mock list operation returning resource summaries
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [{"resource_pool": "pool-1"}]

    # Mock get operation returning 404
    get_response = MagicMock()
    get_response.status = 404

    mock_client.get.return_value = get_response

    # Mock the _perform_list_operation to return the summaries
    with patch.object(
        info_module,
        "_perform_list_operation",
        return_value=[{"resource_pool": "pool-1"}],
    ):
        info_module._list_resource_details()

    mock_module.warn.assert_called_once()


def test_list_resource_details_bare_string_identifiers(info_module, mock_client):
    # Some list endpoints (e.g. /appliance/local-accounts) return bare
    # identifier strings rather than summary dicts. Each string must be mapped
    # onto the unfilled path parameter of the get operation so the detail
    # lookup can be built.
    get_response_1 = MagicMock()
    get_response_1.status = 200
    get_response_1.json = {"name": "pool_1"}

    get_response_2 = MagicMock()
    get_response_2.status = 200
    get_response_2.json = {"name": "pool_2"}

    mock_client.get.side_effect = [get_response_1, get_response_2]

    with patch.object(
        info_module,
        "_perform_list_operation",
        return_value=["pool-1", "pool-2"],
    ):
        result = info_module._list_resource_details()

    # The get operation must be called with the identifier substituted into the
    # {resource_pool} path template.
    assert [call.args[0] for call in mock_client.get.call_args_list] == [
        "/vcenter/resource-pool/pool-1",
        "/vcenter/resource-pool/pool-2",
    ]
    # The enrichment (the mapped identifier) is merged into each result.
    assert result[0] == {"resource_pool": "pool-1", "name": "pool_1"}
    assert result[1] == {"resource_pool": "pool-2", "name": "pool_2"}


def test_list_resource_details_full_dicts_without_path_param(info_module, mock_client):
    # Some list endpoints (e.g. /appliance/monitoring) return full resource
    # dicts whose identifier attribute is named differently than the get
    # operation's path parameter ("id" vs "{resource_pool}"). Since the dict
    # cannot supply the path parameter, it is already complete and is returned
    # as-is without a redundant per-item detail lookup.
    items = [
        {"id": "cpu.util", "name": "CPU utilization"},
        {"id": "mem.util", "name": "Memory utilization"},
    ]
    with patch.object(info_module, "_perform_list_operation", return_value=items):
        result = info_module._list_resource_details()

    # No per-item get lookups are performed.
    mock_client.get.assert_not_called()
    assert result == items


def test_list_resource_details_includes_query_params(mock_module, mock_client):
    # The get operation's query_spec must be honored for per-item detail
    # lookups performed during the list-then-enrich fallback, not just for
    # the direct-get path in _module_base.py.
    get_operation_config = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="get",
        query_spec={"verbose": {"required": False}},
    )
    list_operation_config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="get",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module_instance = VmwareRestInfoModuleBase(
            module=mock_module,
            moid_parameter_hints=["resource_pool"],
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )
    module_instance.params = {**module_instance.params, "verbose": True}

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"name": "pool_1"}
    mock_client.get.return_value = get_response

    with patch.object(
        module_instance,
        "_perform_list_operation",
        return_value=["pool-1"],
    ):
        module_instance._list_resource_details()

    mock_client.get.assert_called_once_with(
        "/vcenter/resource-pool/pool-1", query={"verbose": True}
    )


def test_get_resource_info_with_resource_id(info_module, mock_client):
    info_module.params["resource_pool"] = "pool-1"

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = {"resource_pool": "pool-1", "name": "my_pool"}

    mock_client.get.return_value = mock_response

    result = info_module.get_resource_info()

    assert result["id"] == "pool-1"
    assert result["value"] == {"resource_pool": "pool-1", "name": "my_pool"}
    assert result["info"] == [{"resource_pool": "pool-1", "name": "my_pool"}]


def test_get_resource_info_not_found_returns_empty(info_module, mock_client):
    info_module.params["resource_pool"] = "pool-nonexistent"

    mock_response = MagicMock()
    mock_response.status = 404

    mock_client.get.return_value = mock_response

    result = info_module.get_resource_info()

    assert result == {"info": [], "value": {}}


def test_get_resource_info_falls_back_to_list(info_module, mock_client):
    # No resource_pool param, so get operation should fail with RequiredPathParameterError
    # and fall back to listing
    get_response_1 = MagicMock()
    get_response_1.status = 200
    get_response_1.json = {"resource_pool": "pool-1", "name": "pool_1"}

    get_response_2 = MagicMock()
    get_response_2.status = 200
    get_response_2.json = {"resource_pool": "pool-2", "name": "pool_2"}

    mock_client.get.side_effect = [get_response_1, get_response_2]

    with patch.object(
        info_module,
        "_perform_list_operation",
        return_value=[{"resource_pool": "pool-1"}, {"resource_pool": "pool-2"}],
    ):
        result = info_module.get_resource_info()

    assert len(result["info"]) == 2
    assert result["info"][0]["resource_pool"] == "pool-1"
    assert result["info"][1]["resource_pool"] == "pool-2"
