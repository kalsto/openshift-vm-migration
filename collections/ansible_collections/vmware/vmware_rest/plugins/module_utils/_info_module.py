# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ._module_base import (
    VmwareRestModuleBase,
)
from ._errors import RequiredPathParameterError
from ._operation_configs import OperationConfig


class VmwareRestInfoModuleBase(VmwareRestModuleBase):
    def __init__(
        self,
        module,
        moid_parameter_hints: list,
        get_operation_config: OperationConfig,
        list_operation_config: OperationConfig = None,
    ):
        super().__init__(
            module=module,
            moid_parameter_hints=moid_parameter_hints,
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )

    def get_resource_info(self) -> dict:
        """
        Gather information about one or more resources, based on the module parameters.
        Uses the get endpoint when possible, otherwise falls back to the list endpoint.
        """
        try:
            resource = self._perform_get_operation()
            # force results into a list
            if not resource:
                resource = []
            elif not isinstance(resource, list):
                resource = [resource]
            return self.normalize_info_results(
                query_results=resource, single_resource=(len(resource) <= 1)
            )
        except RequiredPathParameterError:
            if self.list_operation_config is None:
                raise

        # Fall through to list operation when GET requires a path parameter we don't have
        return self.normalize_info_results(
            query_results=self._list_resource_details(),
            single_resource=(self.get_operation_config is None),
        )

    def _list_resource_details(self) -> list:
        result = []
        http_method = getattr(self.client, self.get_operation_config.http_method)
        for resource in self._perform_list_operation():
            if isinstance(resource, dict):
                # The list endpoint returned resource summaries (dicts). If the
                # summary doesn't provide the get operation's path parameter, it
                # cannot be enriched via a per-item lookup and is already
                # complete, so use it as-is.
                if self._unfilled_get_path_parameter({**self.params, **resource}):
                    result.append(resource)
                    continue
                enrichment = resource
            else:
                # The list endpoint returned bare identifier strings. Map each
                # identifier onto the unfilled path parameter of the get
                # operation so the detail lookup can be built.
                path_param = self._unfilled_get_path_parameter(self.params)
                enrichment = {path_param: resource} if path_param else {}

            params = {**self.params, **enrichment}
            path = self.get_operation_config.build_path(params=params)
            query = self.get_operation_config.build_query(params=params)
            response = http_method(path, query=query)
            if not response:
                self.module.fail_json(
                    "Error while looking up more details about a resource: %s" % path
                )

            if response.status == 404:
                self.module.warn(
                    "Resource at %s could not be queried. It may have been deleted or modified during this operation."
                    % path
                )
                continue

            result.append({**enrichment, **response.json})
        return result

    def _unfilled_get_path_parameter(self, params: dict):
        """
        Return the name of the first path parameter in the get operation's URI
        that is not already populated by the given params, or None if all are
        populated. Used to map a bare identifier string returned by a list
        endpoint onto the get operation's path template.
        """
        for placeholder in re.findall(r"\{(\w+)\}", self.get_operation_config.uri):
            if not params.get(placeholder):
                return placeholder
        return None

    def normalize_info_results(
        self, query_results: list, single_resource: bool
    ) -> dict:
        """
        Takes a query result from an INFO module query, and formats it
        to be consistent with expected INFO module outputs.
        Always returns info (list[dict]) and value in the result.
        - info is always a list[dict], regardless of the query type.
        - value preserves the shape of the query: a dict when a single resource
          was fetched by ID (single_resource=True), a list[dict] when listing.
        - id (str) is added when a single resource was fetched and has a
          recognizable MOID attribute.
        """
        if not isinstance(query_results, list):
            self.module.fail_json(
                "Module got unexpected non-list results from an INFO endpoint. This is an unsupported response, and a bug.",
                result_type=str(type(query_results)),
            )

        results = {"info": query_results}

        if single_resource:
            results["value"] = query_results[0] if query_results else {}
            if query_results:
                resource_id = self._get_moid_attribute_value_from_resource(
                    resource=query_results[0]
                )
                if resource_id:
                    results["id"] = resource_id
        else:
            results["value"] = query_results

        return results
