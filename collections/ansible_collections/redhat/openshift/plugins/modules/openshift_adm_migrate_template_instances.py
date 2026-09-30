#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Alina Buzachis (@alinabuzachis)
description:
- Update TemplateInstances to point to the latest group-version-kinds.
- Analogous to C(oc adm migrate template-instances).
module: openshift_adm_migrate_template_instances
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
  namespace:
    description:
    - The namespace that the template can be found in.
    - If no namespace if specified, migrate objects in all namespaces.
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
short_description: Update TemplateInstances to point to the latest group-version-kinds
version_added: 2.2.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
- name: Migrate TemplateInstances in namespace=test
  redhat.openshift.openshift_adm_migrate_template_instances:
    namespace: test
  register: _result

- name: Migrate TemplateInstances in all namespaces
  redhat.openshift.openshift_adm_migrate_template_instances:
  register: _result
"""

RETURN = r"""result:
  description:
  - List with all TemplateInstances that have been migrated.
  elements: dict
  returned: success
  sample:
  - apiVersion: template.openshift.io/v1
    kind: TemplateInstance
    metadata:
      creationTimestamp: '2021-11-10T11:12:09Z'
      finalizers:
      - template.openshift.io/finalizer
      managedFields:
      - apiVersion: template.openshift.io/v1
        fieldsType: FieldsV1
        fieldsV1:
          f:spec:
            f:template:
              f:metadata:
                f:name: {}
              f:objects: {}
              f:parameters: {}
        manager: kubectl-create
        operation: Update
        time: '2021-11-10T11:12:09Z'
      - apiVersion: template.openshift.io/v1
        fieldsType: FieldsV1
        fieldsV1:
          f:metadata:
            f:finalizers:
              .: {}
              v:"template.openshift.io/finalizer": {}
          f:status:
            f:conditions: {}
        manager: openshift-controller-manager
        operation: Update
        time: '2021-11-10T11:12:09Z'
      - apiVersion: template.openshift.io/v1
        fieldsType: FieldsV1
        fieldsV1:
          f:status:
            f:objects: {}
        manager: OpenAPI-Generator
        operation: Update
        time: '2021-11-10T11:12:33Z'
      name: demo
      namespace: test
      resourceVersion: '545370'
      uid: 09b795d7-7f07-4d94-bf0f-2150ee66f88d
    spec:
      requester:
        groups:
        - system:masters
        - system:authenticated
        username: system:admin
      template:
        metadata:
          creationTimestamp: null
          name: template
        objects:
        - apiVersion: v1
          kind: Secret
          metadata:
            labels:
              foo: bar
            name: secret
        - apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: deployment
          spec:
            replicas: 0
            selector:
              matchLabels:
                key: value
            template:
              metadata:
                labels:
                  key: value
              spec:
                containers:
                - image: k8s.gcr.io/e2e-test-images/agnhost:2.32
                  name: hello-openshift
        - apiVersion: v1
          kind: Route
          metadata:
            name: route
          spec:
            to:
              name: foo
        parameters:
        - name: NAME
          value: ${NAME}
    status:
      conditions:
      - lastTransitionTime: '2021-11-10T11:12:09Z'
        message: ''
        reason: Created
        status: 'True'
        type: Ready
      objects:
      - ref:
          apiVersion: v1
          kind: Secret
          name: secret
          namespace: test
          uid: 33fad364-6d47-4f9c-9e51-92cba5602a57
      - ref:
          apiVersion: apps/v1
          kind: Deployment
          name: deployment
          namespace: test
          uid: 3b527f88-42a1-4811-9e2f-baad4e4d8807
      - ref:
          apiVersion: route.openshift.io/v1.Route
          kind: Route
          name: route
          namespace: test
          uid: 5b5411de-8769-4e27-ba52-6781630e4008
  - '...'
  type: list
"""


from ansible.module_utils.common.text.converters import to_native

from ansible_collections.redhat.openshift.plugins.module_utils.openshift_common import (
    AnsibleOpenshiftModule,
)

try:
    from kubernetes.dynamic.exceptions import DynamicApiError
except ImportError:
    pass

from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
    AUTH_ARG_SPEC,
    WAIT_ARG_SPEC,
)

transforms = {
    "Build": "build.openshift.io/v1",
    "BuildConfig": "build.openshift.io/v1",
    "DeploymentConfig": "apps.openshift.io/v1",
    "Route": "route.openshift.io/v1",
}


class OpenShiftMigrateTemplateInstances(AnsibleOpenshiftModule):
    def __init__(self, **kwargs):
        super(OpenShiftMigrateTemplateInstances, self).__init__(**kwargs)

    def patch_template_instance(self, resource, templateinstance):
        result = None

        try:
            result = resource.status.patch(templateinstance)
        except Exception as exc:
            self.fail_json(
                msg="Failed to migrate TemplateInstance {0} due to: {1}".format(
                    templateinstance["metadata"]["name"], to_native(exc)
                )
            )

        return result.to_dict()

    @staticmethod
    def perform_migrations(templateinstances):
        ti_list = []
        ti_to_be_migrated = []

        ti_list = (
            templateinstances.get("kind") == "TemplateInstanceList"
            and templateinstances.get("items")
            or [templateinstances]
        )

        for ti_elem in ti_list:
            objects = ti_elem["status"].get("objects")
            if objects:
                for i, obj in enumerate(objects):
                    object_type = obj["ref"]["kind"]
                    if (
                        object_type in transforms.keys()
                        and obj["ref"].get("apiVersion") != transforms[object_type]
                    ):
                        ti_elem["status"]["objects"][i]["ref"]["apiVersion"] = (
                            transforms[object_type]
                        )
                        ti_to_be_migrated.append(ti_elem)

        return ti_to_be_migrated

    def execute_module(self):
        templateinstances = None
        namespace = self.params.get("namespace")
        results = {"changed": False, "result": []}

        resource = self.find_resource(
            "templateinstances", "template.openshift.io/v1", fail=True
        )

        if namespace:
            # Get TemplateInstances from a provided namespace
            try:
                templateinstances = resource.get(namespace=namespace).to_dict()
            except DynamicApiError as exc:
                self.fail_json(
                    msg="Failed to retrieve TemplateInstances in namespace '{0}': {1}".format(
                        namespace, exc.body
                    ),
                    error=exc.status,
                    status=exc.status,
                    reason=exc.reason,
                )
            except Exception as exc:
                self.fail_json(
                    msg="Failed to retrieve TemplateInstances in namespace '{0}': {1}".format(
                        namespace, to_native(exc)
                    ),
                    error="",
                    status="",
                    reason="",
                )
        else:
            # Get TemplateInstances from all namespaces
            templateinstances = resource.get().to_dict()

            ti_to_be_migrated = self.perform_migrations(templateinstances)

            if ti_to_be_migrated:
                if self.check_mode:
                    self.exit_json(**{"changed": True, "result": ti_to_be_migrated})
                else:
                    for ti_elem in ti_to_be_migrated:
                        results["result"].append(
                            self.patch_template_instance(resource, ti_elem)
                        )
                    results["changed"] = True

        self.exit_json(**results)


def argspec():
    argument_spec = {}
    argument_spec.update(AUTH_ARG_SPEC)
    argument_spec.update(WAIT_ARG_SPEC)
    argument_spec["namespace"] = dict(type="str")

    return argument_spec


def main():
    argument_spec = argspec()
    module = OpenShiftMigrateTemplateInstances(
        argument_spec=argument_spec, supports_check_mode=True
    )
    module.run_module()


if __name__ == "__main__":
    main()
