#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Chris Houseknecht <@chouseknecht>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
- Chris Houseknecht (@chouseknecht)
- Fabian von Feilitzsch (@fabianvf)
description:
- Use the Kubernetes Python client to perform CRUD operations on K8s objects.
- Pass the object definition from a source file or inline. See examples for reading
  files and using Jinja templates or vault-encrypted files.
- Access to the full range of K8s APIs.
- Use the M(kubernetes.core.k8s_info) module to obtain a list of items about an object
  of type C(kind).
- Authenticate using either a config file, certificates, password or token.
- Supports check mode.
- Optimized for OKD/OpenShift Kubernetes flavors.
module: k8s
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
  api_version:
    aliases:
    - api
    - version
    default: v1
    description:
    - Use to specify the API version.
    - Use to create, delete, or discover an object without providing a full resource
      definition.
    - Use in conjunction with I(kind), I(name), and I(namespace) to identify a specific
      object.
    - If I(resource definition) is provided, the I(apiVersion) value from the I(resource_definition)
      will override this option.
    type: str
  append_hash:
    default: false
    description:
    - Whether to append a hash to a resource name for immutability purposes
    - Applies only to ConfigMap and Secret resources
    - The parameter will be silently ignored for other resource kinds
    - The full definition of an object is needed to generate the hash - this means
      that deleting an object created with append_hash will only work if the same
      object is passed with state=absent (alternatively, just use state=absent with
      the name including the generated hash and append_hash=no)
    type: bool
  apply:
    default: false
    description:
    - C(apply) compares the desired resource definition with the previously supplied
      resource definition, ignoring properties that are automatically generated
    - C(apply) works better with Services than 'force=yes'
    - mutually exclusive with C(merge_type)
    type: bool
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
  continue_on_error:
    default: false
    description:
    - Whether to continue on creation/deletion errors when multiple resources are
      defined.
    - This has no effect on the validation step which is controlled by the C(validate.fail_on_error)
      parameter.
    type: bool
    version_added: 2.0.0
    version_added_collection: redhat.openshift
  delete_options:
    description:
    - Configure behavior when deleting an object.
    - Only used when I(state=absent).
    suboptions:
      gracePeriodSeconds:
        description:
        - Specify how many seconds to wait before forcefully terminating.
        - Only implemented for Pod resources.
        - If not specified, the default grace period for the object type will be used.
        type: int
      preconditions:
        description:
        - Specify condition that must be met for delete to proceed.
        suboptions:
          resourceVersion:
            description:
            - Specify the resource version of the target object.
            type: str
          uid:
            description:
            - Specify the UID of the target object.
            type: str
        type: dict
      propagationPolicy:
        choices:
        - Foreground
        - Background
        - Orphan
        description:
        - Use to control how dependent objects are deleted.
        - If not specified, the default policy for the object type will be used. This
          may vary across object types.
        type: str
    type: dict
    version_added: 1.2.0
    version_added_collection: kubernetes.core
  force:
    default: false
    description:
    - If set to C(yes), and I(state) is C(present), an existing object will be replaced.
    type: bool
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
  kind:
    description:
    - Use to specify an object model.
    - Use to create, delete, or discover an object without providing a full resource
      definition.
    - Use in conjunction with I(api_version), I(name), and I(namespace) to identify
      a specific object.
    - If I(resource definition) is provided, the I(kind) value from the I(resource_definition)
      will override this option.
    type: str
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
  merge_type:
    choices:
    - merge
    - strategic-merge
    description:
    - Whether to override the default patch merge approach with a specific type. By
      default, the strategic merge will typically be used.
    - For example, Custom Resource Definitions typically aren't updatable by the usual
      strategic merge. You may want to use C(merge) if you see "strategic merge patch
      format is not supported"
    - See U(https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/#use-a-json-merge-patch-to-update-a-deployment)
    - If more than one merge_type is given, the merge_types will be tried in order
    - Defaults to C(['strategic-merge', 'merge']), which is ideal for using the same
      parameters on resource kinds that combine Custom Resources and built-in resources.
    - mutually exclusive with C(apply)
    - I(merge_type=json) has been removed in version 4.0.0. Please use M(kubernetes.core.k8s_json_patch)
      instead.
    elements: str
    type: list
  name:
    description:
    - Use to specify an object name.
    - Use to create, delete, or discover an object without providing a full resource
      definition.
    - Use in conjunction with I(api_version), I(kind) and I(namespace) to identify
      a specific object.
    - If I(resource definition) is provided, the I(metadata.name) value from the I(resource_definition)
      will override this option.
    type: str
  namespace:
    description:
    - Use to specify an object namespace.
    - Useful when creating, deleting, or discovering an object without providing a
      full resource definition.
    - Use in conjunction with I(api_version), I(kind), and I(name) to identify a specific
      object.
    - If I(resource definition) is provided, the I(metadata.namespace) value from
      the I(resource_definition) will override this option.
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
    - patched
    default: present
    description:
    - Determines if an object should be created, patched, or deleted. When set to
      C(present), an object will be created, if it does not already exist. If set
      to C(absent), an existing object will be deleted. If set to C(present), an existing
      object will be patched, if its attributes differ from those specified using
      I(resource_definition) or I(src).
    - C(patched) state is an existing resource that has a given patch applied. If
      the resource doesn't exist, silently skip it (do not raise an error).
    type: str
  template:
    description:
    - Provide a valid YAML template definition file for an object when creating or
      updating.
    - Value can be provided as string or dictionary.
    - Mutually exclusive with C(src) and C(resource_definition).
    - Template files needs to be present on the Ansible Controller's file system.
    - Additional parameters can be specified using dictionary.
    - 'Valid additional parameters - '
    - 'C(newline_sequence) (str): Specify the newline sequence to use for templating
      files. valid choices are "\n", "\r", "\r\n". Default value "\n".'
    - 'C(block_start_string) (str): The string marking the beginning of a block. Default
      value "{%".'
    - 'C(block_end_string) (str): The string marking the end of a block. Default value
      "%}".'
    - 'C(variable_start_string) (str): The string marking the beginning of a print
      statement. Default value "{{".'
    - 'C(variable_end_string) (str): The string marking the end of a print statement.
      Default value "}}".'
    - 'C(trim_blocks) (bool): Determine when newlines should be removed from blocks.
      When set to C(yes) the first newline after a block is removed (block, not variable
      tag!). Default value is true.'
    - 'C(lstrip_blocks) (bool): Determine when leading spaces and tabs should be stripped.
      When set to C(yes) leading spaces and tabs are stripped from the start of a
      line to a block. This functionality requires Jinja 2.7 or newer. Default value
      is false.'
    type: raw
    version_added: 2.0.0
    version_added_collection: redhat.openshift
  username:
    description:
    - Provide a username for authenticating with the API. Can also be specified via
      K8S_AUTH_USERNAME environment variable.
    - Please note that this only works with clusters configured to use HTTP Basic
      Auth. If your cluster has a different form of authentication (e.g. OAuth2 in
      OpenShift), this option will not work as expected and you should look into the
      M(community.okd.k8s_auth) module, as that might do what you need.
    type: str
  validate:
    description:
    - how (if at all) to validate the resource definition against the kubernetes schema.
      Requires the kubernetes-validate python module
    suboptions:
      fail_on_error:
        description: whether to fail on validation errors.
        type: bool
      strict:
        default: true
        description: whether to fail when passing unexpected properties
        type: bool
      version:
        description: version of Kubernetes to validate against. defaults to Kubernetes
          server version
        type: str
    type: dict
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
short_description: Manage OpenShift objects
"""

EXAMPLES = """
- name: Create an OCP project
  redhat.openshift.k8s:
    state: present
    resource_definition:
      apiVersion: project.openshift.io/v1
      kind: Project
      metadata:
        name: testing

- name: Create a k8s namespace
  redhat.openshift.k8s:
    name: testing
    api_version: v1
    kind: Namespace
    state: present

- name: Create a Service object from an inline definition
  redhat.openshift.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Service
      metadata:
        name: web
        namespace: testing
        labels:
          app: galaxy
          service: web
      spec:
        selector:
          app: galaxy
          service: web
        ports:
          - protocol: TCP
            targetPort: 8000
            name: port-8000-tcp
            port: 8000

- name: Remove an existing Service object
  redhat.openshift.k8s:
    state: absent
    api_version: v1
    kind: Service
    namespace: testing
    name: web

# Passing the object definition from a file

- name: Create a Deployment by reading the definition from a local file
  redhat.openshift.k8s:
    state: present
    src: /testing/deployment.yml

- name: >-
    Read definition file from the Ansible controller file system.
    If the definition file has been encrypted with Ansible Vault it will automatically be decrypted.
  redhat.openshift.k8s:
    state: present
    definition: "{{ lookup('file', '/testing/deployment.yml') | from_yaml }}"

- name: Read definition file from the Ansible controller file system after Jinja templating
  redhat.openshift.k8s:
    state: present
    definition: "{{ lookup('template', '/testing/deployment.yml') | from_yaml }}"

- name: fail on validation errors
  redhat.openshift.k8s:
    state: present
    definition: "{{ lookup('template', '/testing/deployment.yml') | from_yaml }}"
    validate:
      fail_on_error: true

- name: warn on validation errors, check for unexpected properties
  redhat.openshift.k8s:
    state: present
    definition: "{{ lookup('template', '/testing/deployment.yml') | from_yaml }}"
    validate:
      fail_on_error: false
      strict: true
"""

RETURN = r"""result:
  contains:
    api_version:
      description: The versioned schema of this representation of an object.
      returned: success
      type: str
    duration:
      description: elapsed time of task in seconds
      returned: when C(wait) is true
      sample: 48
      type: int
    error:
      description: Error while trying to create/delete the object.
      returned: error
      type: complex
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
      description: Standard object metadata. Includes name, namespace, annotations,
        labels, etc.
      returned: success
      type: complex
    spec:
      description: Specific attributes of the object. Will vary based on the I(api_version)
        and I(kind).
      returned: success
      type: complex
    status:
      description: Current status details for the object.
      returned: success
      type: complex
  description:
  - The created, patched, or otherwise present object. Will be empty in the case of
    a deletion.
  returned: success
  type: complex
"""


from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
    NAME_ARG_SPEC,
    RESOURCE_ARG_SPEC,
    AUTH_ARG_SPEC,
    WAIT_ARG_SPEC,
    DELETE_OPTS_ARG_SPEC,
)


def validate_spec():
    return dict(
        fail_on_error=dict(type="bool"),
        version=dict(),
        strict=dict(type="bool", default=True),
    )


def argspec():
    argument_spec = {}
    argument_spec.update(NAME_ARG_SPEC)
    argument_spec.update(RESOURCE_ARG_SPEC)
    argument_spec.update(AUTH_ARG_SPEC)
    argument_spec.update(WAIT_ARG_SPEC)
    argument_spec["merge_type"] = dict(
        type="list", elements="str", choices=["merge", "strategic-merge"]
    )
    argument_spec["validate"] = dict(type="dict", default=None, options=validate_spec())
    argument_spec["append_hash"] = dict(type="bool", default=False)
    argument_spec["apply"] = dict(type="bool", default=False)
    argument_spec["template"] = dict(type="raw", default=None)
    argument_spec["delete_options"] = dict(
        type="dict", default=None, options=DELETE_OPTS_ARG_SPEC
    )
    argument_spec["continue_on_error"] = dict(type="bool", default=False)
    argument_spec["state"] = dict(
        default="present", choices=["present", "absent", "patched"]
    )
    argument_spec["force"] = dict(type="bool", default=False)
    return argument_spec


def main():
    mutually_exclusive = [
        ("resource_definition", "src"),
        ("merge_type", "apply"),
        ("template", "resource_definition"),
        ("template", "src"),
    ]

    from ansible_collections.redhat.openshift.plugins.module_utils.k8s import OKDRawModule

    module = OKDRawModule(
        argument_spec=argspec(),
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive,
    )
    module.run_module()


if __name__ == "__main__":
    main()
