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
- This module starts a new build from the provided build config or build name.
- This module also cancel a new, pending or running build by requesting a graceful
  shutdown of the build. There may be a delay between requesting the build and the
  time the build is terminated.
- This can also restart a new build when the current is cancelled.
- Analogous to C(oc cancel-build) and C(oc start-build).
module: openshift_build
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
  build_args:
    description:
    - Specify a list of key-value pair to pass to Docker during the build.
    elements: dict
    suboptions:
      name:
        description:
        - docker build argument name.
        required: true
        type: str
      value:
        description:
        - docker build argument value.
        required: true
        type: str
    type: list
  build_config_name:
    description:
    - Specify the name of a build config from which a new build will be run.
    - Mutually exclusive with parameter I(build_name).
    type: str
  build_name:
    description:
    - Specify the name of a build which should be re-run.
    - Mutually exclusive with parameter I(build_config_name).
    type: str
  build_phases:
    choices:
    - New
    - Pending
    - Running
    default: []
    description:
    - List of state for build to cancel.
    - Ignored when C(state=started).
    elements: str
    type: list
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
  commit:
    description:
    - Specify the source code commit identifier the build should use; requires a build
      based on a Git repository.
    type: str
  context:
    description:
    - The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT
      environment variable.
    type: str
  env_vars:
    description:
    - Specify a list of key-value pair for an environment variable to set for the
      build container.
    elements: dict
    suboptions:
      name:
        description:
        - Environment variable name.
        required: true
        type: str
      value:
        description:
        - Environment variable value.
        required: true
        type: str
    type: list
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
  incremental:
    description:
    - Overrides the incremental setting in a source-strategy build, ignored if not
      specified.
    type: bool
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
  namespace:
    description:
    - Specify the namespace for the build or the build config.
    required: true
    type: str
  no_cache:
    description:
    - Overrides the noCache setting in a docker-strategy build, ignored if not specified.
    type: bool
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
  state:
    choices:
    - started
    - cancelled
    - restarted
    default: started
    description:
    - Determines if a Build should be started ,cancelled or restarted.
    - When set to C(restarted) a new build will be created after the current build
      is cancelled.
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
  wait:
    default: false
    description:
    - When C(state=started), specify whether to wait for a build to complete and exit
      with a non-zero return code if the build fails.
    - When I(state=cancelled), specify whether to wait for a build phase to be Cancelled.
    type: bool
  wait_sleep:
    default: 5
    description:
    - Number of seconds to sleep between checks.
    - Ignored if C(wait=false).
    type: int
  wait_timeout:
    default: 120
    description:
    - How long in seconds to wait for a build to complete.
    - Ignored if C(wait=false).
    type: int
requirements:
- python >= 3.6
- kubernetes >= 12.0.0
short_description: Start a new build or Cancel running, pending, or new builds.
version_added: 2.3.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
# Starts build from build config default/hello-world
- name: Starts build from build config
  redhat.openshift.openshift_build:
    namespace: default
    build_config_name: hello-world

# Starts build from a previous build "default/hello-world-1"
- name: Starts build from a previous build
  redhat.openshift.openshift_build:
    namespace: default
    build_name: hello-world-1

# Cancel the build with the given name
- name: Cancel build from default namespace
  redhat.openshift.openshift_build:
    namespace: "default"
    build_name: ruby-build-1
    state: cancelled

# Cancel the named build and create a new one with the same parameters
- name: Cancel build from default namespace and create a new one
  redhat.openshift.openshift_build:
    namespace: "default"
    build_name: ruby-build-1
    state: restarted

# Cancel all builds created from 'ruby-build' build configuration that are in 'new' state
- name: Cancel build from default namespace and create a new one
  redhat.openshift.openshift_build:
    namespace: "default"
    build_config_name: ruby-build
    build_phases:
      - New
    state: cancelled
"""

RETURN = r"""builds:
  contains:
    api_version:
      description: The versioned schema of this representation of an object.
      returned: success
      type: str
    kind:
      description: Represents the REST resource this object represents.
      returned: success
      type: str
    metadata:
      description: Standard object metadata. Includes name, namespace, annotations,
        labels, etc.
      returned: success
      type: dict
    spec:
      description: Specific attributes of the build.
      returned: success
      type: dict
    status:
      description: Current status details for the object.
      returned: success
      type: dict
  description:
  - The builds that were started/cancelled.
  returned: success
  type: complex
"""


import copy

from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
    AUTH_ARG_SPEC,
)


def argument_spec():
    args = copy.deepcopy(AUTH_ARG_SPEC)

    args_options = dict(
        name=dict(type="str", required=True), value=dict(type="str", required=True)
    )

    args.update(
        dict(
            state=dict(
                type="str",
                choices=["started", "cancelled", "restarted"],
                default="started",
            ),
            build_args=dict(type="list", elements="dict", options=args_options),
            commit=dict(type="str"),
            env_vars=dict(type="list", elements="dict", options=args_options),
            build_name=dict(type="str"),
            build_config_name=dict(type="str"),
            namespace=dict(type="str", required=True),
            incremental=dict(type="bool"),
            no_cache=dict(type="bool"),
            wait=dict(type="bool", default=False),
            wait_sleep=dict(type="int", default=5),
            wait_timeout=dict(type="int", default=120),
            build_phases=dict(
                type="list",
                elements="str",
                default=[],
                choices=["New", "Pending", "Running"],
            ),
        )
    )
    return args


def main():
    mutually_exclusive = [
        ("build_name", "build_config_name"),
    ]
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_builds import (
        OpenShiftBuilds,
    )

    module = OpenShiftBuilds(
        argument_spec=argument_spec(),
        mutually_exclusive=mutually_exclusive,
        required_one_of=[
            [
                "build_name",
                "build_config_name",
            ]
        ],
    )
    module.run_module()


if __name__ == "__main__":
    main()
