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
- Image streams allow you to control which images are rolled out to your builds and
  applications.
- This module fetches the latest version of an image from a remote repository and
  updates the image stream tag if it does not match the previous value.
- Running the module multiple times will not create duplicate entries.
- When importing an image, only the image metadata is copied, not the image contents.
- Analogous to C(oc import-image).
module: openshift_import_image
notes:
- To avoid SSL certificate validation errors when C(validate_certs) is I(True), the
  full certificate chain for the API server must be provided via C(ca_cert) or in
  the kubeconfig file.
options:
  all:
    default: false
    description:
    - If set to I(true), import all tags from the provided source on creation or if
      C(source) is specified.
    type: bool
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
    - Image stream to import tag into.
    - This can be provided as a list of images streams or a single value.
    required: true
    type: raw
  namespace:
    description:
    - Use to specify namespace for image stream to create/update.
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
  reference_policy:
    choices:
    - source
    - local
    default: source
    description:
    - Allow to request pullthrough for external image when set to I(local).
    type: str
  scheduled:
    default: false
    description:
    - Set each imported Docker image to be periodically imported from a remote repository.
    type: bool
  source:
    description:
    - A Docker image repository to import images from.
    - Should be provided as 'registry.io/repo/image'
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
  validate_registry_certs:
    description:
    - If set to I(true), allow importing from registries that have invalid HTTPS certificates.
      or are hosted via HTTP. This parameter will take precedence over the insecure
      annotation.
    type: bool
requirements:
- python >= 3.6
- kubernetes >= 12.0.0
- docker-image-py
short_description: Import the latest image information from a tag in a container image
  registry.
version_added: 2.2.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
# Import tag latest into a new image stream.
- name: Import tag latest into new image stream
  redhat.openshift.openshift_import_image:
    namespace: testing
    name: mystream
    source: registry.io/repo/image:latest

# Update imported data for tag latest in an already existing image stream.
- name: Update imported data for tag latest
  redhat.openshift.openshift_import_image:
    namespace: testing
    name: mystream

# Update imported data for tag 'stable' in an already existing image stream.
- name: Update imported data for tag latest
  redhat.openshift.openshift_import_image:
    namespace: testing
    name: mystream:stable

# Update imported data for all tags in an existing image stream.
- name: Update imported data for all tags
  redhat.openshift.openshift_import_image:
    namespace: testing
    name: mystream
    all: true

# Import all tags into a new image stream.
- name: Import all tags into a new image stream.
  redhat.openshift.openshift_import_image:
    namespace: testing
    name: mystream
    source: registry.io/repo/image:latest
    all: true

# Import all tags into a new image stream for a list of image streams
- name: Import all tags into a new image stream.
  redhat.openshift.openshift_import_image:
    namespace: testing
    name:
      - mystream1
      - mystream2
      - mystream3
    source: registry.io/repo/image:latest
    all: true
"""

RETURN = r"""result:
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
      description: Specific attributes of the object. Will vary based on the I(api_version)
        and I(kind).
      returned: success
      type: dict
    status:
      description: Current status details for the object.
      returned: success
      type: dict
  description:
  - List with all ImageStreamImport that have been created.
  elements: dict
  returned: success
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
            namespace=dict(type="str", required=True),
            name=dict(type="raw", required=True),
            all=dict(type="bool", default=False),
            validate_registry_certs=dict(type="bool"),
            reference_policy=dict(
                type="str", choices=["source", "local"], default="source"
            ),
            scheduled=dict(type="bool", default=False),
            source=dict(type="str"),
        )
    )
    return args


def main():
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_import_image import (
        OpenShiftImportImage,
    )

    module = OpenShiftImportImage(
        argument_spec=argument_spec(), supports_check_mode=True
    )
    module.run_module()


if __name__ == "__main__":
    main()
