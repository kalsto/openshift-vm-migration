#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
- Aubin Bikouo (@abikouo)
description:
- This module allow administrators to remove references to the specified roles, clusterroles,
  users, and groups.
- Analogous to C(oc adm prune auth).
module: openshift_adm_prune_auth
notes:
- To avoid SSL certificate validation errors when C(validate_certs) is I(True), the
  full certificate chain for the API server must be provided via C(ca_cert) or in
  the kubeconfig file.
options:
  api_key:
    description:
    - Token used to authenticate with the API. Can also be specified via K8S_AUTH_API_KEY
      environment variable.
    type: str
  ca_cert:
    aliases:
    - ssl_ca_cert
    description:
    - Path to a CA certificate used to authenticate with the API. The full certificate
      chain must be provided to avoid certificate validation errors. Can also be specified
      via K8S_AUTH_SSL_CA_CERT environment variable.
    type: path
  client_cert:
    aliases:
    - cert_file
    description:
    - Path to a certificate used to authenticate with the API. Can also be specified
      via K8S_AUTH_CERT_FILE environment variable.
    type: path
  client_key:
    aliases:
    - key_file
    description:
    - Path to a key file used to authenticate with the API. Can also be specified
      via K8S_AUTH_KEY_FILE environment variable.
    type: path
  context:
    description:
    - The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT
      environment variable.
    type: str
  host:
    description:
    - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST
      environment variable.
    type: str
  impersonate_groups:
    description:
    - Group(s) to impersonate for the operation.
    - 'Can also be specified via K8S_AUTH_IMPERSONATE_GROUPS environment. Example:
      Group1,Group2'
    elements: str
    type: list
    version_added: 2.3.0
    version_added_collection: kubernetes.core
  impersonate_user:
    description:
    - Username to impersonate for the operation.
    - Can also be specified via K8S_AUTH_IMPERSONATE_USER environment.
    type: str
    version_added: 2.3.0
    version_added_collection: kubernetes.core
  kubeconfig:
    description:
    - Path to an existing Kubernetes config file. If not provided, and no other connection
      options are provided, the Kubernetes client will attempt to load the default
      configuration file from I(~/.kube/config). Can also be specified via K8S_AUTH_KUBECONFIG
      environment variable.
    - Multiple Kubernetes config file can be provided using separator ';' for Windows
      platform or ':' for others platforms.
    - The kubernetes configuration can be provided as dictionary. This feature requires
      a python kubernetes client version >= 17.17.0. Added in version 2.2.0.
    type: raw
  label_selectors:
    description:
    - Selector (label query) to filter on.
    - Mutually exclusive with option I(name).
    elements: str
    type: list
  name:
    description:
    - Use to specify an object name to remove.
    - Mutually exclusive with option I(label_selectors).
    - If neither I(name) nor I(label_selectors) are specified, prune all resources
      in the namespace.
    type: str
  namespace:
    description:
    - Use to specify an object namespace.
    - Ignored when I(resource) is set to C(clusterroles).
    type: str
  no_proxy:
    description:
    - The comma separated list of hosts/domains/IP/CIDR that shouldn't go through
      proxy. Can also be specified via K8S_AUTH_NO_PROXY environment variable.
    - Please note that this module does not pick up typical proxy settings from the
      environment (e.g. NO_PROXY).
    - This feature requires kubernetes>=19.15.0. When kubernetes library is less than
      19.15.0, it fails even no_proxy set in correct.
    - example value is "localhost,.local,.example.com,127.0.0.1,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
    type: str
    version_added: 2.3.0
    version_added_collection: kubernetes.core
  password:
    description:
    - Provide a password for authenticating with the API. Can also be specified via
      K8S_AUTH_PASSWORD environment variable.
    - Please read the description of the C(username) option for a discussion of when
      this option is applicable.
    type: str
  persist_config:
    description:
    - Whether or not to save the kube config refresh tokens. Can also be specified
      via K8S_AUTH_PERSIST_CONFIG environment variable.
    - When the k8s context is using a user credentials with refresh tokens (like oidc
      or gke/gcloud auth), the token is refreshed by the k8s python client library
      but not saved by default. So the old refresh token can expire and the next auth
      might fail. Setting this flag to true will tell the k8s python client to save
      the new refresh token to the kube config file.
    - Default to false.
    - Please note that the current version of the k8s python client library does not
      support setting this flag to True yet.
    - 'The fix for this k8s python library is here: https://github.com/kubernetes-client/python-base/pull/169'
    type: bool
  proxy:
    description:
    - The URL of an HTTP proxy to use for the connection. Can also be specified via
      K8S_AUTH_PROXY environment variable.
    - Please note that this module does not pick up typical proxy settings from the
      environment (e.g. HTTP_PROXY).
    type: str
  proxy_headers:
    description:
    - The Header used for the HTTP proxy.
    - Documentation can be found here U(https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html?highlight=proxy_headers#urllib3.util.make_headers).
    suboptions:
      basic_auth:
        description:
        - Colon-separated username:password for basic authentication header.
        - Can also be specified via K8S_AUTH_PROXY_HEADERS_BASIC_AUTH environment.
        type: str
      proxy_basic_auth:
        description:
        - Colon-separated username:password for proxy basic authentication header.
        - Can also be specified via K8S_AUTH_PROXY_HEADERS_PROXY_BASIC_AUTH environment.
        type: str
      user_agent:
        description:
        - String representing the user-agent you want, such as foo/1.0.
        - Can also be specified via K8S_AUTH_PROXY_HEADERS_USER_AGENT environment.
        type: str
    type: dict
    version_added: 2.0.0
    version_added_collection: kubernetes.core
  resource:
    choices:
    - roles
    - clusterroles
    - users
    - groups
    description:
    - The specified resource to remove.
    required: true
    type: str
  username:
    description:
    - Provide a username for authenticating with the API. Can also be specified via
      K8S_AUTH_USERNAME environment variable.
    - Please note that this only works with clusters configured to use HTTP Basic
      Auth. If your cluster has a different form of authentication (e.g. OAuth2 in
      OpenShift), this option will not work as expected and you should look into the
      M(community.okd.k8s_auth) module, as that might do what you need.
    type: str
  validate_certs:
    aliases:
    - verify_ssl
    description:
    - Whether or not to verify the API server's SSL certificates. Can also be specified
      via K8S_AUTH_VERIFY_SSL environment variable.
    type: bool
requirements:
- python >= 3.6
- kubernetes >= 12.0.0
short_description: Removes references to the specified roles, clusterroles, users,
  and groups
version_added: 2.2.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
- name: Prune all roles from default namespace
  openshift_adm_prune_auth:
    resource: roles
    namespace: testing

- name: Prune clusterroles using label selectors
  openshift_adm_prune_auth:
    resource: roles
    namespace: testing
    label_selectors:
      - phase=production
"""

RETURN = r"""authorization:
  description: list of OAuthClientAuthorization deleted.
  returned: I(resource=users)
  type: list
cluster_role_binding:
  description: list of cluster role binding deleted.
  returned: always
  type: list
group:
  description: list of Security Context Constraints deleted.
  returned: I(resource=users)
  type: list
role_binding:
  description: list of role binding deleted.
  returned: I(resource=users) or I(resource=groups) or I(resource=clusterroles)
  type: list
security_context_constraints:
  description: list of Security Context Constraints deleted.
  returned: I(resource=users) or I(resource=groups)
  type: list
"""


import copy

from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
    AUTH_ARG_SPEC,
)


def argument_spec():
    args = copy.deepcopy(AUTH_ARG_SPEC)
    args.update(
        dict(
            resource=dict(
                type="str",
                required=True,
                choices=["roles", "clusterroles", "users", "groups"],
            ),
            namespace=dict(type="str"),
            name=dict(type="str"),
            label_selectors=dict(type="list", elements="str"),
        )
    )
    return args


def main():
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_adm_prune_auth import (
        OpenShiftAdmPruneAuth,
    )

    module = OpenShiftAdmPruneAuth(
        argument_spec=argument_spec(),
        mutually_exclusive=[("name", "label_selectors")],
        supports_check_mode=True,
    )
    module.run_module()


if __name__ == "__main__":
    main()
