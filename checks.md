Pre-Checks and Tests:
- VM must be powered on - this is mandatory and non-negotiable. If a VM is powered off, nothing else happens for that VM
  - vmware_vm_powerstate
- Check for QEMU guest agent - differs from Windows to Linux
- Need the vmware agent installed and running
- Snapshots - another full stop. Check for them before attempting to migrate
  - vmware_guest_snapshot / vmware_guest_snapshot_info
- We should have a map from all networks to all networks - make sure the vlan from the VM has a matching NetworkAttachmentDefinition
- Provider Certifications - need to ensure the vCenter cert's that are stored in the MTV are valid at each stage. Might have to build a rotate-process
- Typo in the VM name. Don't proceed if it doesn't go further
- collect firmware, machine version, boot mode, tpm, secure boot
- collect disk usage, cpu, ram, number of nics


Initial check (2+weeks ideally lead time, to allow for time to fix issues that may arise)
- collect facts has to be enhanced by a bunch of vmware collections listed above
- tpm: might be from vmware_guest_tpm
  - must be configured in vCenter already
- QEMU agent: might be vmware_guest_tools_info
- network might be vmware_guest_network
- should look at what vmware_vm_info provides
- look at vsphere_vswitch_info
- check for snapshots

Do we want to check vmware_host snmp, ntp, ipv6, sriov, vmnic_info ? Any of those things? Resource Pools or tags? Do they use tags for anything DRS related currently?


Can gather facts about ESXi host using community.vmware.vmware_host_config_info

