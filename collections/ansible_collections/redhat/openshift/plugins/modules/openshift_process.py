#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Copyright (c) 2020-2021, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
author: Fabian von Feilitzsch (@fabianvf)
description:
- Processes a specified OpenShift template with the provided template.
- Templates can be provided inline, from a file, or specified by name and namespace
  in the cluster.
- Analogous to `oc process`.
- For CRUD operations on Template resources themselves, see the redhat.openshift.k8s
  module.
module: openshift_process
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
  name:
    description:
    - The name of the Template to process.
    - The Template must be present in the cluster.
    - When provided, I(namespace) is required.
    - Mutually exclusive with I(resource_definition) or I(src)
    type: str
  namespace:
    description:
    - The namespace that the template can be found in.
    type: str
  namespace_target:
    description:
    - The namespace that resources should be created, updated, or deleted in.
    - Only used when I(state) is present or absent.
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
  parameter_file:
    description:
    - A path to a file containing template parameter values to override/set values
      in the Template.
    - Corresponds to the `--param-file` argument to oc process.
    type: str
  parameters:
    description:
    - 'A set of key: value pairs that will be used to set/override values in the Template.'
    - Corresponds to the `--param` argument to oc process.
    type: dict
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
  resource_definition:
    aliases:
    - definition
    - inline
    description:
    - Provide a valid YAML definition (either as a string, list, or dict) for an object
      when creating or updating.
    - 'NOTE: I(kind), I(api_version), I(name), and I(namespace) will be overwritten
      by corresponding values found in the provided I(resource_definition).'
  src:
    description:
    - 'Provide a path to a file containing a valid YAML definition of an object or
      objects to be created or updated. Mutually exclusive with I(resource_definition).
      NOTE: I(kind), I(api_version), I(name), and I(namespace) will be overwritten
      by corresponding values found in the configuration read in from the I(src) file.'
    - Reads from the local file system. To read from the Ansible controller's file
      system, including vaulted files, use the file lookup plugin or template lookup
      plugin, combined with the from_yaml filter, and pass the result to I(resource_definition).
      See Examples below.
    - The URL to manifest files that can be used to create the resource. Added in
      version 2.4.0.
    - Mutually exclusive with I(template) in case of M(kubernetes.core.k8s) module.
    type: path
  state:
    choices:
    - absent
    - present
    - rendered
    default: rendered
    description:
    - Determines what to do with the rendered Template.
    - The state I(rendered) will render the Template based on the provided parameters,
      and return the rendered objects in the I(resources) field. These can then be
      referenced in future tasks.
    - The state I(present) will cause the resources in the rendered Template to be
      created if they do not already exist, and patched if they do.
    - The state I(absent) will delete the resources in the rendered Template.
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
    - Whether to wait for certain resource kinds to end up in the desired state.
    - By default the module exits once Kubernetes has received the request.
    - Implemented for C(state=present) for C(Deployment), C(DaemonSet) and C(Pod),
      and for C(state=absent) for all resource kinds.
    - For resource kinds without an implementation, C(wait) returns immediately unless
      C(wait_condition) is set.
    type: bool
  wait_condition:
    description:
    - Specifies a custom condition on the status to wait for.
    - Ignored if C(wait) is not set or is set to False.
    suboptions:
      reason:
        description:
        - The value of the reason field in your desired condition
        - For example, if a C(Deployment) is paused, The C(Progressing) C(type) will
          have the C(DeploymentPaused) reason.
        - The possible reasons in a condition are specific to each resource type in
          Kubernetes.
        - See the API documentation of the status field for a given resource to see
          possible choices.
        type: str
      status:
        choices:
        - 'True'
        - 'False'
        - Unknown
        default: 'True'
        description:
        - The value of the status field in your desired condition.
        - For example, if a C(Deployment) is paused, the C(Progressing) C(type) will
          have the C(Unknown) status.
        type: str
      type:
        description:
        - The type of condition to wait for.
        - For example, the C(Pod) resource will set the C(Ready) condition (among
          others).
        - Required if you are specifying a C(wait_condition).
        - If left empty, the C(wait_condition) field will be ignored.
        - The possible types for a condition are specific to each resource type in
          Kubernetes.
        - See the API documentation of the status field for a given resource to see
          possible choices.
        type: str
    type: dict
  wait_sleep:
    default: 5
    description:
    - Number of seconds to sleep between checks.
    type: int
  wait_timeout:
    default: 120
    description:
    - How long in seconds to wait for the resource to end up in the desired state.
    - Ignored if C(wait) is not set.
    type: int
requirements:
- python >= 3.6
- kubernetes >= 12.0.0
- PyYAML >= 3.11
short_description: Process an OpenShift template.openshift.io/v1 Template
version_added: 0.3.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
- name: Process a template in the cluster
  redhat.openshift.openshift_process:
    name: nginx-example
    namespace: openshift # only needed if using a template already on the server
    parameters:
      NAMESPACE: openshift
      NAME: test123
    state: rendered
  register: result

- name: Create the rendered resources using apply
  redhat.openshift.k8s:
    namespace: default
    definition: '{{ item }}'
    wait: true
    apply: true
  loop: '{{ result.resources }}'

- name: Process a template with parameters from an env file and create the resources
  redhat.openshift.openshift_process:
    name: nginx-example
    namespace: openshift
    namespace_target: default
    parameter_file: 'files/nginx.env'
    state: present
    wait: true

- name: Process a local template and create the resources
  redhat.openshift.openshift_process:
    src: files/example-template.yaml
    parameter_file: files/example.env
    namespace_target: default
    state: present

- name: Process a local template, delete the resources, and wait for them to terminate
  redhat.openshift.openshift_process:
    src: files/example-template.yaml
    parameter_file: files/example.env
    namespace_target: default
    state: absent
    wait: true
"""

RETURN = r"""resources:
  contains:
    apiVersion:
      description: The versioned schema of this representation of an object.
      returned: success
      type: str
    kind:
      description: Represents the REST resource this object represents.
      returned: success
      type: str
    metadata:
      contains:
        name:
          description: The name of the resource
          type: str
        namespace:
          description: The namespace of the resource
          type: str
      description: Standard object metadata. Includes name, namespace, annotations,
        labels, etc.
      returned: success
      type: complex
    spec:
      description: Specific attributes of the object. Will vary based on the I(api_version)
        and I(kind).
      returned: success
      type: dict
    status:
      contains:
        conditions:
          description: Array of status conditions for the object. Not guaranteed to
            be present
          type: complex
      description: Current status details for the object.
      returned: success
      type: dict
  description:
  - The rendered resources defined in the Template
  returned: on success when state is rendered
  type: complex
result:
  contains:
    apiVersion:
      description: The versioned schema of this representation of an object.
      returned: success
      type: str
    duration:
      description: elapsed time of task in seconds
      returned: when C(wait) is true
      sample: 48
      type: int
    items:
      description: Returned only when multiple yaml documents are passed to src or
        resource_definition
      returned: when resource_definition or src contains list of objects
      type: list
    kind:
      description: Represents the REST resource this object represents.
      returned: success
      type: str
    metadata:
      contains:
        name:
          description: The name of the resource
          type: str
        namespace:
          description: The namespace of the resource
          type: str
      description: Standard object metadata. Includes name, namespace, annotations,
        labels, etc.
      returned: success
      type: complex
    spec:
      description: Specific attributes of the object. Will vary based on the I(api_version)
        and I(kind).
      returned: success
      type: dict
    status:
      contains:
        conditions:
          description: Array of status conditions for the object. Not guaranteed to
            be present
          type: complex
      description: Current status details for the object.
      returned: success
      type: complex
  description:
  - The created, patched, or otherwise present object. Will be empty in the case of
    a deletion.
  returned: on success when state is present or absent
  type: complex
"""


from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
    AUTH_ARG_SPEC,
    RESOURCE_ARG_SPEC,
    WAIT_ARG_SPEC,
)


def argspec():
    argument_spec = {}
    argument_spec.update(AUTH_ARG_SPEC)
    argument_spec.update(WAIT_ARG_SPEC)
    argument_spec.update(RESOURCE_ARG_SPEC)
    argument_spec["state"] = dict(
        type="str", default="rendered", choices=["present", "absent", "rendered"]
    )
    argument_spec["namespace"] = dict(type="str")
    argument_spec["namespace_target"] = dict(type="str")
    argument_spec["parameters"] = dict(type="dict")
    argument_spec["name"] = dict(type="str")
    argument_spec["parameter_file"] = dict(type="str")

    return argument_spec


def main():
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_process import (
        OpenShiftProcess,
    )

    module = OpenShiftProcess(argument_spec=argspec(), supports_check_mode=True)
    module.run_module()


if __name__ == "__main__":
    main()
