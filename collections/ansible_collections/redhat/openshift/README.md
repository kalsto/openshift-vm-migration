# OpenShift Collection for Ansible

This repo hosts the `redhat.openshift` Ansible Collection.

## Description
The collection includes a variety of Ansible content to help automate the management of applications in OpenShift clusters, as well as the provisioning and maintenance of clusters themselves.


## Installation

### Installing the Collection from Automation Hub

Before using the OpenShift collection, you need to install it with the Automation Hub CLI:

    ansible-galaxy collection install redhat.openshift

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat.openshift
    version: 5.0.0
```

### Installing the Kubernetes Python Library

Content in this collection requires the [Kubernetes Python client](https://pypi.org/project/kubernetes/) to interact with Kubernetes' APIs. You can install it with:

    pip3 install kubernetes

## Use Cases

### Using modules from the OpenShift Collection in your playbooks

It's preferable to use content in this collection using their Fully Qualified Collection Namespace (FQCN), for example `redhat.openshift.openshift`:

```yaml
---
plugin: redhat.openshift.openshift
connections:
  - namespaces:
    - testing
```

For documentation on how to use individual plugins included in this collection, please see the links in the 'Included content' section earlier in this README.

### Ansible Turbo mode Tech Preview

The `redhat.openshift` collection supports Ansible Turbo mode as a tech preview via the `cloud.common` collection. By default, this feature is disabled. To enable Turbo mode, set the environment variable `ENABLE_TURBO_MODE=1` on the managed node. For example:

```yaml
---
- hosts: remote
  environment:
    ENABLE_TURBO_MODE: 1
  tasks:
    ...
```

Please read more about Ansible Turbo mode - [here](https://github.com/ansible-collections/redhat.openshift/blob/main/docs/ansible_turbo_mode.rst).


## Support

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

For the latest supported versions, refer to the release notes below.

If you encounter issues or have questions, you can submit a support request through the following channels:
 - GitHub Issues: Report bugs, request features, or ask questions by opening an issue in the [GitHub repository](https://github.com/openshift/redhat.openshift/).

## Release notes

See the [raw generated changelog](https://github.com/openshift/redhat.openshift/blob/main/CHANGELOG.rst).

## More Information

For more information about Ansible's Kubernetes and OpenShift integrations, join the `#ansible-kubernetes` channel on [libera.chat](https://libera.chat/) IRC, and browse the resources in the [Kubernetes Working Group](https://github.com/ansible/community/wiki/Kubernetes) Community wiki page.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.
