# Lean Ansible bindings for OpenShift Virtualization


This repository hosts the `redhat.openshift_virtualization` Ansible Collection, which provides virtual machine operations and an inventory source for use with Ansible.

## Ansible and Python version compatibility

This collection has been tested against Ansible versions **>=2.16,<=2.19** and Python versions **>=3.10,<=3.13**.

See the [Red Hat Ansible Automation Platform Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform) for supported combinations.


## Included content

### Plugins

* `kubevirt`: Inventory source for KubeVirt VirtualMachines
* `kubevirt_vm`: Create or delete KubeVirt VirtualMachines
* `kubevirt_vm_info`: Describe KubeVirt VirtualMachines
* `kubevirt_vmi_info`: Describe KubeVirt VirtualMachineInstances

## Using this collection

### Installing the Collection from Ansible Galaxy

Before using the collection, you need to setup Ansible Automation Hub as galaxy server; then install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install redhat.openshift_virtualization
```


### Build and install locally

Clone the repository, checkout the tag you want to build, or pick the main branch for the development version; then:
```bash
ansible-galaxy collection build .
ansible-galaxy collection install kubevirt-core-*.tar.gz
```

### Dependencies

#### Ansible collections

* [kubernetes.core](https://console.redhat.com/ansible/automation-hub/repo/published/kubernetes/core)>=5.2.0,<7.0.0

To install all the dependencies, you need to setup Ansible Automation Hub as galaxy server; then install them with:
```bash
ansible-galaxy collection install -r requirements.yml
```


#### Python libraries

- jsonpatch
- kubernetes>=28.1.0
- PyYAML>=3.11

To install all the dependencies:
```bash
pip install -r requirements.txt
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Support

This collection is maintained by Red Hat OpenShift Virtualization.

As Red Hat Ansible Certified Content, this collection is entitled to support through the Ansible Automation Platform (AAP) using the **Create issue** button on the top right corner.

## Providing feedback and reporting issues

If you encounter any issues with this collection please go to the [Red Hat Customer Portal](https://access.redhat.com/support/cases/#/case/new/get-support?caseCreate=true) and open a support case.

Additionally, to report an issue or to improve this collection, you can also log in to your [Red Hat Jira account](https://issues.redhat.com) and submit a [Jira issue](https://issues.redhat.com/secure/CreateIssueDetails!init.jspa?pid=12323181&issuetype=1&components=12364490&priority=10200&summary=[redhat.openshift_virtualization]&customfield_12316142).

## Testing

The collection includes unit and integration tests. The integration tests require a working cluster.

### Running tests

To run tests the `ansible-test` tool is required. See [Testing Ansible and Collections](https://docs.ansible.com/ansible/latest/dev_guide/testing_running_locally.html#testing-ansible-and-collections)
on how to run the collection's tests.


<!--start support -->
<!--end support -->

## Licensing

Apache License 2.0

See [LICENSE](https://github.com/redhat/redhat.openshift_virtualization/blob/main/LICENSE) to see the full text.
