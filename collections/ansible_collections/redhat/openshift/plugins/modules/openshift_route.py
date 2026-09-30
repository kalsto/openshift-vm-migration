#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Fabian von Feilitzsch (@fabianvf)
description:
- Looks up a Service and creates a new Route based on it.
- Analogous to `oc expose` and `oc create route` for creating Routes, but does not
  support creating Services.
- For creating Services from other resources, see kubernetes.core.k8s.
module: openshift_route
notes:
- To avoid SSL certificate validation errors when C(validate_certs) is I(True), the
  full certificate chain for the API server must be provided via C(ca_cert) or in
  the kubeconfig file.
options:
  annotations:
    description:
    - Specify the Route Annotations.
    - 'A set of key: value pairs.'
    type: dict
    version_added: 2.1.0
    version_added_collection: redhat.openshift
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
  hostname:
    description:
    - The hostname for the Route.
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
  labels:
    description:
    - Specify the labels to apply to the created Route.
    - 'A set of key: value pairs.'
    type: dict
  name:
    description:
    - The desired name of the Route to be created.
    - Defaults to the value of I(service)
    type: str
  namespace:
    description:
    - The namespace of the resource being targeted.
    - The Route will be created in this namespace as well.
    required: true
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
  path:
    description:
    - The path for the Route
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
  port:
    description:
    - Name or number of the port the Route will route traffic to.
    type: str
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
  service:
    aliases:
    - svc
    description:
    - The name of the service to expose.
    - Required when I(state) is not absent.
    type: str
  state:
    choices:
    - absent
    - present
    default: present
    description:
    - Determines if an object should be created, patched, or deleted. When set to
      C(present), an object will be created, if it does not already exist. If set
      to C(absent), an existing object will be deleted. If set to C(present), an existing
      object will be patched, if its attributes differ from those specified using
      I(resource_definition) or I(src).
    type: str
  termination:
    choices:
    - edge
    - passthrough
    - reencrypt
    - insecure
    default: insecure
    description:
    - The termination type of the Route.
    - If left empty no termination type will be set, and the route will be insecure.
    - When set to insecure I(tls) will be ignored.
    type: str
  tls:
    description:
    - TLS configuration for the newly created route.
    - Only used when I(termination) is set.
    suboptions:
      ca_certificate:
        description:
        - Path to a CA certificate file on the target host.
        - Not supported when I(termination) is set to passthrough.
        type: str
      certificate:
        description:
        - Path to a certificate file on the target host.
        - Not supported when I(termination) is set to passthrough.
        type: str
      destination_ca_certificate:
        description:
        - Path to a CA certificate file used for securing the connection.
        - Only used when I(termination) is set to reencrypt.
        - Defaults to the Service CA.
        type: str
      insecure_policy:
        choices:
        - allow
        - redirect
        - disallow
        default: disallow
        description:
        - Sets the InsecureEdgeTerminationPolicy for the Route.
        - Not supported when I(termination) is set to reencrypt.
        - When I(termination) is set to passthrough, only redirect is supported.
        - If not provided, insecure traffic will be disallowed.
        type: str
      key:
        description:
        - Path to a key file on the target host.
        - Not supported when I(termination) is set to passthrough.
        type: str
    type: dict
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
  wildcard_policy:
    choices:
    - Subdomain
    description:
    - The wildcard policy for the hostname.
    - Currently only Subdomain is supported.
    - If not provided, the default of None will be used.
    type: str
requirements:
- python >= 3.6
- kubernetes >= 12.0.0
- PyYAML >= 3.11
short_description: Expose a Service as an OpenShift Route.
version_added: 0.3.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
- name: Create hello-world deployment
  redhat.openshift.k8s:
    definition:
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: hello-kubernetes
        namespace: default
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: hello-kubernetes
        template:
          metadata:
            labels:
              app: hello-kubernetes
          spec:
            containers:
              - name: hello-kubernetes
                image: paulbouwer/hello-kubernetes:1.8
                ports:
                  - containerPort: 8080

- name: Create Service for the hello-world deployment
  redhat.openshift.k8s:
    definition:
      apiVersion: v1
      kind: Service
      metadata:
        name: hello-kubernetes
        namespace: default
      spec:
        ports:
          - port: 80
            targetPort: 8080
        selector:
          app: hello-kubernetes

- name: Expose the insecure hello-world service externally
  redhat.openshift.openshift_route:
    service: hello-kubernetes
    namespace: default
    insecure_policy: allow
    annotations:
      haproxy.router.openshift.io/balance: roundrobin
  register: route
"""

RETURN = r"""duration:
  description: elapsed time of task in seconds
  returned: when C(wait) is true
  sample: 48
  type: int
result:
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
          description: The name of the created Route
          type: str
        namespace:
          description: The namespace of the create Route
          type: str
      description: Standard object metadata. Includes name, namespace, annotations,
        labels, etc.
      returned: success
      type: complex
    spec:
      contains:
        host:
          description: Host is an alias/DNS that points to the service.
          type: str
        path:
          description: Path that the router watches for, to route traffic for to the
            service.
          type: str
        port:
          contains:
            targetPort:
              description: The target port on pods selected by the service this route
                points to.
              type: str
          description: Defines a port mapping from a router to an endpoint in the
            service endpoints.
          type: complex
        tls:
          contains:
            caCertificate:
              description: Provides the cert authority certificate contents.
              type: str
            certificate:
              description: Provides certificate contents.
              type: str
            destinationCACertificate:
              description: Provides the contents of the ca certificate of the final
                destination.
              type: str
            insecureEdgeTerminationPolicy:
              description: Indicates the desired behavior for insecure connections
                to a route.
              type: str
            key:
              description: Provides key file contents.
              type: str
            termination:
              description: Indicates termination type.
              type: str
          description: Defines config used to secure a route and provide termination.
          type: complex
        to:
          contains:
            kind:
              description: The kind of target that the route is referring to. Currently,
                only 'Service' is allowed.
              type: str
            name:
              description: Name of the service/target that is being referred to. e.g.
                name of the service.
              type: str
            weight:
              description: Specifies the target's relative weight against other target
                reference objects.
              type: int
          description: Specifies the target that resolve into endpoints.
          type: complex
        wildcardPolicy:
          description: Wildcard policy if any for the route.
          type: str
      description: Specification for the Route
      returned: success
      type: complex
    status:
      contains:
        ingress:
          contains:
            conditions:
              contains:
                status:
                  description: The status of the condition. Can be True, False, Unknown.
                  type: str
                type:
                  description: The type of the condition. Currently only 'Ready'.
                  type: str
              description: Array of status conditions for the Route ingress.
              type: complex
            host:
              description: The host string under which the route is exposed.
              type: str
            routerCanonicalHostname:
              description: The external host name for the router that can be used
                as a CNAME for the host requested for this route. May not be set.
              type: str
            routerName:
              description: A name chosen by the router to identify itself.
              type: str
            wildcardPolicy:
              description: The wildcard policy that was allowed where this route is
                exposed.
              type: str
          description: List of places where the route may be exposed.
          type: complex
      description: Current status details for the Route
      returned: success
      type: complex
  description:
  - The Route object that was created or updated. Will be empty in the case of deletion.
  returned: success
  type: complex
"""


import copy

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.redhat.openshift.plugins.module_utils.openshift_common import (
    AnsibleOpenshiftModule,
)

try:
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.runner import (
        perform_action,
    )
    from ansible_collections.kubernetes.core.plugins.module_utils.k8s.waiter import (
        Waiter,
    )
    from ansible_collections.kubernetes.core.plugins.module_utils.args_common import (
        AUTH_ARG_SPEC,
        WAIT_ARG_SPEC,
        COMMON_ARG_SPEC,
    )
except ImportError as e:
    pass
    AUTH_ARG_SPEC = WAIT_ARG_SPEC = COMMON_ARG_SPEC = {}

try:
    from kubernetes.dynamic.exceptions import DynamicApiError, NotFoundError
except ImportError:
    pass


class OpenShiftRoute(AnsibleOpenshiftModule):
    def __init__(self):
        super(OpenShiftRoute, self).__init__(
            argument_spec=self.argspec,
            supports_check_mode=True,
        )

        self.append_hash = False
        self.apply = False
        self.warnings = []
        self.params["merge_type"] = None

    @property
    def argspec(self):
        spec = copy.deepcopy(AUTH_ARG_SPEC)
        spec.update(copy.deepcopy(WAIT_ARG_SPEC))
        spec.update(copy.deepcopy(COMMON_ARG_SPEC))

        spec["service"] = dict(type="str", aliases=["svc"])
        spec["namespace"] = dict(required=True, type="str")
        spec["labels"] = dict(type="dict")
        spec["name"] = dict(type="str")
        spec["hostname"] = dict(type="str")
        spec["path"] = dict(type="str")
        spec["wildcard_policy"] = dict(choices=["Subdomain"], type="str")
        spec["port"] = dict(type="str")
        spec["tls"] = dict(
            type="dict",
            options=dict(
                ca_certificate=dict(type="str"),
                certificate=dict(type="str"),
                destination_ca_certificate=dict(type="str"),
                key=dict(type="str", no_log=False),
                insecure_policy=dict(
                    type="str",
                    choices=["allow", "redirect", "disallow"],
                    default="disallow",
                ),
            ),
        )
        spec["termination"] = dict(
            choices=["edge", "passthrough", "reencrypt", "insecure"], default="insecure"
        )
        spec["annotations"] = dict(type="dict")

        return spec

    def execute_module(self):
        service_name = self.params.get("service")
        namespace = self.params["namespace"]
        termination_type = self.params.get("termination")
        if termination_type == "insecure":
            termination_type = None
        state = self.params.get("state")

        if state != "absent" and not service_name:
            self.fail_json("If 'state' is not 'absent' then 'service' must be provided")

        # We need to do something a little wonky to wait if the user doesn't supply a custom condition
        custom_wait = (
            self.params.get("wait")
            and not self.params.get("wait_condition")
            and state != "absent"
        )
        if custom_wait:
            # Don't use default wait logic in perform_action
            self.params["wait"] = False

        route_name = self.params.get("name") or service_name
        labels = self.params.get("labels")
        hostname = self.params.get("hostname")
        path = self.params.get("path")
        wildcard_policy = self.params.get("wildcard_policy")
        port = self.params.get("port")
        annotations = self.params.get("annotations")

        if termination_type and self.params.get("tls"):
            tls_ca_cert = self.params["tls"].get("ca_certificate")
            tls_cert = self.params["tls"].get("certificate")
            tls_dest_ca_cert = self.params["tls"].get("destination_ca_certificate")
            tls_key = self.params["tls"].get("key")
            tls_insecure_policy = self.params["tls"].get("insecure_policy")
            if tls_insecure_policy == "disallow":
                tls_insecure_policy = None
        else:
            tls_ca_cert = tls_cert = tls_dest_ca_cert = tls_key = (
                tls_insecure_policy
            ) = None

        route = {
            "apiVersion": "route.openshift.io/v1",
            "kind": "Route",
            "metadata": {
                "name": route_name,
                "namespace": namespace,
                "labels": labels,
            },
            "spec": {},
        }

        if annotations:
            route["metadata"]["annotations"] = annotations

        if state != "absent":
            route["spec"] = self.build_route_spec(
                service_name,
                namespace,
                port=port,
                wildcard_policy=wildcard_policy,
                hostname=hostname,
                path=path,
                termination_type=termination_type,
                tls_insecure_policy=tls_insecure_policy,
                tls_ca_cert=tls_ca_cert,
                tls_cert=tls_cert,
                tls_key=tls_key,
                tls_dest_ca_cert=tls_dest_ca_cert,
            )

        result = perform_action(self.svc, route, self.params)
        timeout = self.params.get("wait_timeout")
        sleep = self.params.get("wait_sleep")
        if custom_wait:
            v1_routes = self.find_resource("Route", "route.openshift.io/v1", fail=True)
            waiter = Waiter(self.client, v1_routes, wait_predicate)
            success, result["result"], result["duration"] = waiter.wait(
                timeout=timeout, sleep=sleep, name=route_name, namespace=namespace
            )

        self.exit_json(**result)

    def build_route_spec(
        self,
        service_name,
        namespace,
        port=None,
        wildcard_policy=None,
        hostname=None,
        path=None,
        termination_type=None,
        tls_insecure_policy=None,
        tls_ca_cert=None,
        tls_cert=None,
        tls_key=None,
        tls_dest_ca_cert=None,
    ):
        v1_services = self.find_resource("Service", "v1", fail=True)
        try:
            target_service = v1_services.get(name=service_name, namespace=namespace)
        except NotFoundError:
            if not port:
                self.fail_json(
                    msg="You need to provide the 'port' argument when exposing a non-existent service"
                )
            target_service = None
        except DynamicApiError as exc:
            self.fail_json(
                msg="Failed to retrieve service to be exposed: {0}".format(exc.body),
                error=exc.status,
                status=exc.status,
                reason=exc.reason,
            )
        except Exception as exc:
            self.fail_json(
                msg="Failed to retrieve service to be exposed: {0}".format(
                    to_native(exc)
                ),
                error="",
                status="",
                reason="",
            )

        route_spec = {
            "tls": {},
            "to": {
                "kind": "Service",
                "name": service_name,
            },
            "port": {
                "targetPort": self.set_port(target_service, port),
            },
            "wildcardPolicy": wildcard_policy,
        }

        # Want to conditionally add these so we don't overwrite what is automically added when nothing is provided
        if termination_type:
            route_spec["tls"] = dict(termination=termination_type.capitalize())
            if tls_insecure_policy:
                if termination_type == "edge":
                    route_spec["tls"][
                        "insecureEdgeTerminationPolicy"
                    ] = tls_insecure_policy.capitalize()
                elif termination_type == "passthrough":
                    if tls_insecure_policy != "redirect":
                        self.fail_json(
                            "'redirect' is the only supported insecureEdgeTerminationPolicy for passthrough routes"
                        )
                    route_spec["tls"][
                        "insecureEdgeTerminationPolicy"
                    ] = tls_insecure_policy.capitalize()
                elif termination_type == "reencrypt":
                    self.fail_json(
                        "'tls.insecure_policy' is not supported with reencrypt routes"
                    )
            else:
                route_spec["tls"]["insecureEdgeTerminationPolicy"] = None
            if tls_ca_cert:
                if termination_type == "passthrough":
                    self.fail_json(
                        "'tls.ca_certificate' is not supported with passthrough routes"
                    )
                route_spec["tls"]["caCertificate"] = tls_ca_cert
            if tls_cert:
                if termination_type == "passthrough":
                    self.fail_json(
                        "'tls.certificate' is not supported with passthrough routes"
                    )
                route_spec["tls"]["certificate"] = tls_cert
            if tls_key:
                if termination_type == "passthrough":
                    self.fail_json("'tls.key' is not supported with passthrough routes")
                route_spec["tls"]["key"] = tls_key
            if tls_dest_ca_cert:
                if termination_type != "reencrypt":
                    self.fail_json(
                        "'destination_certificate' is only valid for reencrypt routes"
                    )
                route_spec["tls"]["destinationCACertificate"] = tls_dest_ca_cert
        else:
            route_spec["tls"] = None
        if hostname:
            route_spec["host"] = hostname
        if path:
            route_spec["path"] = path

        return route_spec

    def set_port(self, service, port_arg):
        if port_arg:
            return port_arg
        for p in service.spec.ports:
            if p.protocol == "TCP":
                if p.name is not None:
                    return p.name
                return p.targetPort
        return None


def wait_predicate(route):
    if not (route.status and route.status.ingress):
        return False
    for ingress in route.status.ingress:
        match = [x for x in ingress.conditions if x.type == "Admitted"]
        if not match:
            return False
        match = match[0]
        if match.status != "True":
            return False
    return True


def main():
    OpenShiftRoute().run_module()


if __name__ == "__main__":
    main()
