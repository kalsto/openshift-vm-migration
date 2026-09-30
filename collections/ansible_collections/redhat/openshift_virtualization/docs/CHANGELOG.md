<table>
<thead>
<tr class="header">
<th>OpenShift Virtualization Collection for Ansible Release Notes</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td></td>
</tr>
<tr class="even">
<td><div class="contents">
<p>Topics</p>
</div></td>
</tr>
<tr class="odd">
<td><p>This changelog describes changes after version 1.0.0.</p></td>
</tr>
<tr class="even">
<td>v2.3.0</td>
</tr>
</tbody>
</table>

# Release Summary

This release adds support for managing VM lifecycle using
state=started/stopped/restarted in redhat\_vm and introduces the
default\_win\_ansible\_connection option for the inventory plugin. It
also fixes the handling of the user-configured strict option in the
inventory plugin and adds compatibility with
ansible-openshift\_virtualization 2.21.

# Minor Changes

-   chore(ci): add ansible 2.21 and fix docs build
    [\#237](https://github.com/redhat/redhat.openshift_virtualization/pull/237)
-   feat(inventory): add `default_win_ansible_connection` option
    [\#240](https://github.com/redhat/redhat.openshift_virtualization/pull/240)
-   feat(redhat\_vm): add `state=started/stopped/restarted` to manage VM
    lifecycle
    [\#242](https://github.com/redhat/redhat.openshift_virtualization/pull/242)

# Bugfixes

-   fix: pass user-configured `strict` option to `_set_composite_vars`
    in redhat inventory plugin
    [\#235](https://github.com/redhat/redhat.openshift_virtualization/pull/235)

## v2.2.4

# Release Summary

This is a service release with updated versions and dependencies.

## v2.2.3

# Release Summary

This release ensures compatibility with
kubernets.openshift\_virtualization &gt;=5.2.0,&lt;7.0.0. changes.

# Minor Changes

-   Bump dependency on kubernetes.openshift\_virtualization and
    collection version
    [\#192](https://github.com/redhat/redhat.openshift_virtualization/pull/192)

## v2.2.2

# Release Summary

This is a maintenance release to trigger a rebuild. No functional
changes.

## v2.2.1

# Release Summary

This release brings some new features and enables compatibility with
ansible-openshift\_virtualization-2.19. The inventory now tries to
lookup winrm services for Windows hosts if enabled. The
unset\_ansible\_port option was added to the inventory. It allows to
control if the value of ansible\_port should be unset if no non-default
value was found. The hidden\_fields argument was added to redhat\_vm and
[redhat](){vm,vmi}\_info which allows to hide and ignore certain fields
in the returned definition of a VM or VMI. If no namespaces were
configured the inventory now tries to use OCP Projects if available. It
is now possible to switch between running and run\_strategy with
redhat\_vm. This is a maintenance release with no functional changes
compared to version 2.2.0. Only the changelog was fixed.

# Minor Changes

-   chore: Bump supported python and ansible-openshift\_virtualization
    versions
    [\#176](https://github.com/redhat/redhat.openshift_virtualization/pull/176)
-   feat(inventory): Add unset\_ansible\_port option
    [\#173](https://github.com/redhat/redhat.openshift_virtualization/pull/173)
-   feat(inventory): Lookup winrm services for Windows hosts
    [\#171](https://github.com/redhat/redhat.openshift_virtualization/pull/171)
-   feat(inventory): Use OCP projects if available
    [\#179](https://github.com/redhat/redhat.openshift_virtualization/pull/179)
-   feat(modules): Add hidden\_fields argument
    [\#178](https://github.com/redhat/redhat.openshift_virtualization/pull/178)
-   fix(redhat\_vm): Allow switching between running and run\_strategy
    [\#180](https://github.com/redhat/redhat.openshift_virtualization/pull/180)
-   fix: Ensure compatibility with ansible-openshift\_virtualization
    &gt;= 2.19
    [\#175](https://github.com/redhat/redhat.openshift_virtualization/pull/175)

## v2.2.0

# Release Summary

This release brings some new features and enables compatibility with
ansible-openshift\_virtualization-2.19.

## v2.1.0

# Release Summary

The redhat\_vmi\_info module was added to this collection.

# Minor Changes

-   Run integration tests in random namespaces
    [\#130](https://github.com/redhat/redhat.openshift_virtualization/pull/130)
-   feat: Add redhat\_vmi\_info module
    [\#129](https://github.com/redhat/redhat.openshift_virtualization/pull/129)

## v2.0.0

# Release Summary

The deprecation of the 'connections' parameter is continued by dropping
support for multiple connections. Inventory configurations with a single
connection remain working for now. This backwards compatibility will be
dropped in version 3.0.0 of the collection. Inventory source caching is
now working and allows to reduce the load on the control plane of a
cluster from which an inventory is built.

# Minor Changes

-   Several small cleanups
    [\#122](https://github.com/redhat/redhat.openshift_virtualization/pull/122)
-   feat(redhat\_vm): Add support for RunStrategy
    [\#124](https://github.com/redhat/redhat.openshift_virtualization/pull/124)

# Breaking Changes / Porting Guide

-   chore: Bump version to 2.0.0
    [\#125](https://github.com/redhat/redhat.openshift_virtualization/pull/125)
-   cleanup(inventory): Drop support for multiple connections
    [\#117](https://github.com/redhat/redhat.openshift_virtualization/pull/117)

# Bugfixes

-   fix(inventory): Fix inventory source caching
    [\#119](https://github.com/redhat/redhat.openshift_virtualization/pull/119)

## v1.5.0

# Release Summary

Support for stopped VMs, deprecation of the 'connections' parameter and
many cleanups.

# Major Changes

-   chore: Update supported ansible-openshift\_virtualization versions
    to &gt;=2.15
    [\#105](https://github.com/redhat/redhat.openshift_virtualization/pull/105)
-   feat,test(inventory): Support listing stopped VMs and major rework
    of unit tests
    [\#114](https://github.com/redhat/redhat.openshift_virtualization/pull/114)

# Minor Changes

-   Bump e2e software versions
    [\#109](https://github.com/redhat/redhat.openshift_virtualization/pull/109)
-   Make redhat\_vm tests more robust
    [\#103](https://github.com/redhat/redhat.openshift_virtualization/pull/103)
-   Several minor improvements
    [\#115](https://github.com/redhat/redhat.openshift_virtualization/pull/115)
-   chore: Ensure compatibility with
    kubernetes.openshift\_virtualization &gt;=3.1.0,&lt;6.0.0
    [\#111](https://github.com/redhat/redhat.openshift_virtualization/pull/111)
-   redhat\_vm integration tests: changed ssh key type to RSA for FIPS
    mode
    [\#108](https://github.com/redhat/redhat.openshift_virtualization/pull/108)

# Bugfixes

-   fix(tests,redhat\_vm): Fix assertion in verify.yml
    [\#106](https://github.com/redhat/redhat.openshift_virtualization/pull/106)

## v1.4.0

# Release Summary

Compatibility with kubernetes.openshift\_virtualization
&gt;=3.1.0,&lt;4.1.0 and some minor enhancements.

# Minor Changes

-   Provide links for docsite and improve docs by adding markup
    [\#95](https://github.com/redhat/redhat.openshift_virtualization/pull/95)
-   cleanup: Cleanup YAML passed to k8s module
    [\#88](https://github.com/redhat/redhat.openshift_virtualization/pull/88)
-   docs: Use proper type for connections parameter
    [\#90](https://github.com/redhat/redhat.openshift_virtualization/pull/90)
-   feat(redhat\_vm\_info): Set wait\_condition based on running
    [\#91](https://github.com/redhat/redhat.openshift_virtualization/pull/91)

# Bugfixes

-   fix(redhat\_vm): Set wait\_condition based on running
    [\#89](https://github.com/redhat/redhat.openshift_virtualization/pull/89)
-   fix: Ensure compatibility with kubernetes.openshift\_virtualization
    &gt;=3.10,&lt;4.1.0
    [\#100](https://github.com/redhat/redhat.openshift_virtualization/pull/100)

## v1.3.2

# Release Summary

No functional changes, hotfix release to retrigger the downstream build
and to keep in sync with Ansible Automation Hub.

## v1.3.1

# Release Summary

No functional changes, only updates to the shipped documentation.

## v1.3.0

# Minor Changes

-   feat: Add append\_base\_domain option to connections
    [\#72](https://github.com/redhat/redhat.openshift_virtualization/pull/72)
-   feat: Give secondary interfaces a higher priority over services
    [\#76](https://github.com/redhat/redhat.openshift_virtualization/pull/76)

# Bugfixes

-   feat: Set ansible\_connection to winrm for Windows hosts
    [\#75](https://github.com/redhat/redhat.openshift_virtualization/pull/75)
-   fix: Explicity set ansible\_port
    [\#70](https://github.com/redhat/redhat.openshift_virtualization/pull/70)
-   fix: Return early to avoid adding empty groups.
    [\#73](https://github.com/redhat/redhat.openshift_virtualization/pull/73)

## v1.2.3

# Release Summary

No functional changes, hotfix release to retrigger the downstream build
and to keep in sync with Ansible Automation Hub.

## v1.2.2

# Release Summary

No functional changes, only cleanup of files included in the release
tarball and vendoring of documentation fragments.

## v1.2.1

# Release Summary

Mostly code cleanups and dependency updates to ensure compatibility with
KubeVirt &gt;= 1.1.0

## v1.2.0

# Release Summary

Not released due to issues in the release process

## v1.1.0

# Minor Changes

-   Add kubevirt\_vm\_info module to describe existing VirtualMachines
-   inventory: Allow to control creation of additional groups
-   inventory: Drop creation of the namespace\_vmis\_group as it is
    redundant

## v1.0.0

# Release Summary

Initial release
