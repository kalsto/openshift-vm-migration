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
- This module allow administrators to remove references images.
- Note that if the C(namespace) is specified, only references images on Image stream
  for the corresponding namespace will be candidate for prune if only they are not
  used or references in another Image stream from another namespace.
- Analogous to C(oc adm prune images).
module: openshift_adm_prune_images
notes:
- To avoid SSL certificate validation errors when C(validate_certs) is I(True), the
  full certificate chain for the API server must be provided via C(ca_cert) or in
  the kubeconfig file.
options:
  all_images:
    default: true
    description:
    - Include images that were imported from external registries as candidates for
      pruning.
    - If pruned, all the mirrored objects associated with them will also be removed
      from the integrated registry.
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
  ignore_invalid_refs:
    default: false
    description:
    - If set to I(true), the pruning process will ignore all errors while parsing
      image references.
    - This means that the pruning process will ignore the intended connection between
      the object and the referenced image.
    - As a result an image may be incorrectly deleted as unused.
    type: bool
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
  keep_younger_than:
    description:
    - Specify the minimum age (in minutes) of an image and its referrers for it to
      be considered a candidate for pruning.
    type: int
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
    - Use to specify namespace for objects.
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
  prune_over_size_limit:
    default: false
    description:
    - Specify if images which are exceeding LimitRanges specified in the same namespace,
      should be considered for pruning.
    type: bool
  prune_registry:
    default: true
    description:
    - If set to I(false), the prune operation will clean up image API objects, but
      none of the associated content in the registry is removed.
    type: bool
  registry_ca_cert:
    description:
    - Path to a CA certificate used to contact registry. The full certificate chain
      must be provided to avoid certificate validation errors.
    type: path
  registry_url:
    description:
    - The address to use when contacting the registry, instead of using the default
      value.
    - This is useful if you can't resolve or reach the default registry but you do
      have an alternative route that works.
    - Particular transport protocol can be enforced using '<scheme>://' prefix.
    type: str
  registry_validate_certs:
    description:
    - Whether or not to verify the API server's SSL certificates. Can also be specified
      via K8S_AUTH_VERIFY_SSL environment variable.
    type: bool
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
- docker-image-py
short_description: Remove unreferenced images
version_added: 2.2.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
# Prune if only images and their referrers were more than an hour old
- name: Prune image with referrer been more than an hour old
  redhat.openshift.openshift_adm_prune_images:
    keep_younger_than: 60

# Remove images exceeding currently set limit ranges
- name: Remove images exceeding currently set limit ranges
  redhat.openshift.openshift_adm_prune_images:
    prune_over_size_limit: true

# Force the insecure http protocol with the particular registry host name
- name: Prune images using custom registry
  redhat.openshift.openshift_adm_prune_images:
    registry_url: http://registry.example.org
    registry_validate_certs: false
"""

RETURN = r"""deleted_images:
  description:
  - The images deleted.
  elements: dict
  returned: success
  sample:
  - apiVersion: image.openshift.io/v1
    dockerImageLayers:
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:5e0b432e8ba9d9029a000e627840b98ffc1ed0c5172075b7d3e869be0df0fe9b
      size: 54932878
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:a84cfd68b5cea612a8343c346bfa5bd6c486769010d12f7ec86b23c74887feb2
      size: 5153424
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:e8b8f2315954535f1e27cd13d777e73da4a787b0aebf4241d225beff3c91cbb1
      size: 10871995
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:0598fa43a7e793a76c198e8d45d8810394e1cfc943b2673d7fcf5a6fdc4f45b3
      size: 54567844
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:83098237b6d3febc7584c1f16076a32ac01def85b0d220ab46b6ebb2d6e7d4d4
      size: 196499409
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:b92c73d4de9a6a8f6b96806a04857ab33cf6674f6411138603471d744f44ef55
      size: 6290769
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:ef9b6ee59783b84a6ec0c8b109c409411ab7c88fa8c53fb3760b5fde4eb0aa07
      size: 16812698
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:c1f6285e64066d36477a81a48d3c4f1dc3c03dddec9e72d97da13ba51bca0d68
      size: 234
    - mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip
      name: sha256:a0ee7333301245b50eb700f96d9e13220cdc31871ec9d8e7f0ff7f03a17c6fb3
      size: 2349241
    dockerImageManifestMediaType: application/vnd.docker.distribution.manifest.v2+json
    dockerImageMetadata:
      Architecture: amd64
      Config:
        Cmd:
        - python3
        Env:
        - PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        - LANG=C.UTF-8
        - GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
        - PYTHON_VERSION=3.8.12
        - PYTHON_PIP_VERSION=21.2.4
        - PYTHON_SETUPTOOLS_VERSION=57.5.0
        - PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py
        - PYTHON_GET_PIP_SHA256=c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309
        Image: sha256:cc3a2931749afa7dede97e32edbbe3e627b275c07bf600ac05bc0dc22ef203de
      Container: b43fcf5052feb037f6d204247d51ac8581d45e50f41c6be2410d94b5c3a3453d
      ContainerConfig:
        Cmd:
        - /bin/sh
        - -c
        - '#(nop) '
        - CMD ["python3"]
        Env:
        - PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        - LANG=C.UTF-8
        - GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
        - PYTHON_VERSION=3.8.12
        - PYTHON_PIP_VERSION=21.2.4
        - PYTHON_SETUPTOOLS_VERSION=57.5.0
        - PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py
        - PYTHON_GET_PIP_SHA256=c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309
        Hostname: b43fcf5052fe
        Image: sha256:cc3a2931749afa7dede97e32edbbe3e627b275c07bf600ac05bc0dc22ef203de
      Created: '2021-12-03T01:53:41Z'
      DockerVersion: 20.10.7
      Id: sha256:f746089c9d02d7126bbe829f788e093853a11a7f0421049267a650d52bbcac37
      Size: 347487141
      apiVersion: image.openshift.io/1.0
      kind: DockerImage
    dockerImageMetadataVersion: '1.0'
    dockerImageReference: python@sha256:a874dcabc74ca202b92b826521ff79dede61caca00ceab0b65024e895baceb58
    kind: Image
    metadata:
      annotations:
        image.openshift.io/dockerLayersOrder: ascending
      creationTimestamp: '2021-12-07T07:55:30Z'
      name: sha256:a874dcabc74ca202b92b826521ff79dede61caca00ceab0b65024e895baceb58
      resourceVersion: '1139214'
      uid: 33be6ab4-af79-4f44-a0fd-4925bd473c1f
  - '...'
  type: list
updated_image_streams:
  description:
  - The images streams updated.
  elements: dict
  returned: success
  sample:
  - apiVersion: image.openshift.io/v1
    kind: ImageStream
    metadata:
      annotations:
        openshift.io/image.dockerRepositoryCheck: '2021-12-07T07:55:30Z'
      creationTimestamp: '2021-12-07T07:55:30Z'
      generation: 1
      name: python
      namespace: images
      resourceVersion: '1139215'
      uid: 443bad2c-9fd4-4c8f-8a24-3eca4426b07f
    spec:
      lookupPolicy:
        local: false
      tags:
      - annotations: null
        from:
          kind: DockerImage
          name: python:3.8.12
        generation: 1
        importPolicy:
          insecure: true
        name: 3.8.12
        referencePolicy:
          type: Source
    status:
      dockerImageRepository: image-registry.openshift-image-registry.svc:5000/images/python
      publicDockerImageRepository: default-route-openshift-image-registry.apps-crc.testing/images/python
      tags: []
  - '...'
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
            namespace=dict(type="str"),
            all_images=dict(type="bool", default=True),
            keep_younger_than=dict(type="int"),
            prune_over_size_limit=dict(type="bool", default=False),
            registry_url=dict(type="str"),
            registry_validate_certs=dict(type="bool"),
            registry_ca_cert=dict(type="path"),
            prune_registry=dict(type="bool", default=True),
            ignore_invalid_refs=dict(type="bool", default=False),
        )
    )
    return args


def main():
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_adm_prune_images import (
        OpenShiftAdmPruneImages,
    )

    module = OpenShiftAdmPruneImages(
        argument_spec=argument_spec(), supports_check_mode=True
    )
    module.run_module()


if __name__ == "__main__":
    main()
