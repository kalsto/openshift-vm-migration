#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
- Aubin Bikouo (@abikouo)
description:
- In order to sync/prune OpenShift Group records with those from an external provider,
  determine which Groups you wish to sync and where their records live.
- Analogous to `oc adm prune groups` and `oc adm group sync`.
- LDAP sync configuration file syntax can be found here U(https://docs.openshift.com/container-platform/4.9/authentication/ldap-syncing.html).
- The bindPassword attribute of the LDAP sync configuration is expected to be a string,
  please use ansible-vault encryption to secure this information.
module: openshift_adm_groups_sync
notes:
- To avoid SSL certificate validation errors when C(validate_certs) is I(True), the
  full certificate chain for the API server must be provided via C(ca_cert) or in
  the kubeconfig file.
options:
  allow_groups:
    default: []
    description:
    - Allowed groups, could be openshift group name or LDAP group dn value.
    - When parameter C(type) is set to I(ldap) this should contains only LDAP group
      definition like I(cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat).
    elements: str
    type: list
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
  deny_groups:
    default: []
    description:
    - Denied groups, could be openshift group name or LDAP group dn value.
    - When parameter C(type) is set to I(ldap) this should contains only LDAP group
      definition like I(cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat).
    - The elements specified in this list will override the ones specified in C(allow_groups).
    elements: str
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
    - absent
    - present
    default: present
    description:
    - Determines if the group should be sync when set to C(present) or pruned when
      set to C(absent).
    type: str
  sync_config:
    aliases:
    - config
    - src
    description:
    - Provide a valid YAML definition of an LDAP sync configuration.
    required: true
    type: dict
  type:
    choices:
    - ldap
    - openshift
    default: ldap
    description:
    - which groups allow and deny list entries refer to.
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
- python-ldap
short_description: Sync OpenShift Groups with records from an external provider.
version_added: 2.1.0
version_added_collection: redhat.openshift
"""

EXAMPLES = """
# Prune all orphaned groups
- name: Prune all orphan groups
  openshift_adm_groups_sync:
    state: absent
    src: "{{ lookup('file', '/path/to/ldap-sync-config.yaml') | from_yaml }}"

# Prune all orphaned groups from a list of specific groups specified in allow_groups
- name: Prune all orphan groups from a list of specific groups specified in allow_groups
  openshift_adm_groups_sync:
    state: absent
    src: "{{ lookup('file', '/path/to/ldap-sync-config.yaml') | from_yaml }}"
    allow_groups:
      - cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat
      - cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat

# Sync all groups from an LDAP server
- name: Sync all groups from an LDAP server
  openshift_adm_groups_sync:
    src:
      kind: LDAPSyncConfig
      apiVersion: v1
      url: ldap://localhost:1390
      insecure: true
      bindDN: cn=admin,dc=example,dc=org
      bindPassword: adminpassword
      rfc2307:
        groupsQuery:
          baseDN: "cn=admins,ou=groups,dc=example,dc=org"
          scope: sub
          derefAliases: never
          filter: (objectClass=*)
          pageSize: 0
        groupUIDAttribute: dn
        groupNameAttributes: [cn]
        groupMembershipAttributes: [member]
        usersQuery:
          baseDN: "ou=users,dc=example,dc=org"
          scope: sub
          derefAliases: never
          pageSize: 0
        userUIDAttribute: dn
        userNameAttributes: [mail]
        tolerateMemberNotFoundErrors: true
        tolerateMemberOutOfScopeErrors: true

# Sync all groups except the ones from the deny_groups  from an LDAP server
- name: Sync all groups from an LDAP server using deny_groups
  openshift_adm_groups_sync:
    src: "{{ lookup('file', '/path/to/ldap-sync-config.yaml') | from_yaml }}"
    deny_groups:
      - cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat
      - cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat

# Sync all OpenShift Groups that have been synced previously with an LDAP server
- name: Sync all OpenShift Groups that have been synced previously with an LDAP server
  openshift_adm_groups_sync:
    src: "{{ lookup('file', '/path/to/ldap-sync-config.yaml') | from_yaml }}"
    type: openshift
"""

RETURN = r"""builds:
  description:
  - The groups that were created, updated or deleted
  elements: dict
  returned: success
  sample:
  - apiVersion: user.openshift.io/v1
    kind: Group
    metadata:
      annotations:
        openshift.io/ldap.sync-time: '2021-12-17T12:20:28.125282'
        openshift.io/ldap.uid: cn=developers,ou=groups,ou=rfc2307,dc=ansible,dc=redhat
        openshift.io/ldap.url: localhost:1390
      creationTimestamp: '2021-12-17T11:09:49Z'
      labels:
        openshift.io/ldap.host: localhost
      managedFields:
      - apiVersion: user.openshift.io/v1
        fieldsType: FieldsV1
        fieldsV1:
          f:metadata:
            f:annotations:
              .: {}
              f:openshift.io/ldap.sync-time: {}
              f:openshift.io/ldap.uid: {}
              f:openshift.io/ldap.url: {}
            f:labels:
              .: {}
              f:openshift.io/ldap.host: {}
          f:users: {}
        manager: OpenAPI-Generator
        operation: Update
        time: '2021-12-17T11:09:49Z'
      name: developers
      resourceVersion: '2014696'
      uid: 8dc211cb-1544-41e1-96b1-efffeed2d7d7
    users:
    - jordanbulls@ansible.org
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
            state=dict(type="str", choices=["absent", "present"], default="present"),
            type=dict(type="str", choices=["ldap", "openshift"], default="ldap"),
            sync_config=dict(type="dict", aliases=["config", "src"], required=True),
            deny_groups=dict(type="list", elements="str", default=[]),
            allow_groups=dict(type="list", elements="str", default=[]),
        )
    )
    return args


def main():
    from ansible_collections.redhat.openshift.plugins.module_utils.openshift_groups import (
        OpenshiftGroupsSync,
    )

    module = OpenshiftGroupsSync(
        argument_spec=argument_spec(), supports_check_mode=True
    )
    module.run_module()


if __name__ == "__main__":
    main()
