# OpenShift VM migration

Ansible playbooks for an existing ROSA cluster. They cover three jobs:

1. Create a PostgreSQL RDS instance in the ROSA cluster VPC, initialize the Ansible Automation Platform (AAP) databases, and store the connection details as OpenShift secrets.
2. Install AAP on that cluster, either against that RDS instance or against the operator's in-cluster database, and remove the AAP install later.
3. Move virtual machines from VMware vSphere to OpenShift Virtualization with the Migration Toolkit for Virtualization (MTV).

The RDS and AAP playbooks are the paths you can run today. The VM migration playbooks and roles are still being assembled, so this README describes that work at the layout level and does not give a launch procedure for it.

## Layout

| Path | What it does |
| --- | --- |
| `playbooks/deploy_rds.yml` | RDS in the ROSA VPC, database init Job, database secrets |
| `playbooks/deploy_aap_w_rds.yml` | AAP 2.7 operator (`stable-2.7`) using the RDS secrets |
| `playbooks/deploy_aap_local_db.yml` | AAP 2.6 operator (`stable-2.6`) with the in-cluster PostgreSQL |
| `playbooks/destroy_aap.yml` | Removes the AAP install. Leaves RDS in place |
| `playbooks/config_aap.yml` | Creates AAP credentials, a project, a vCenter inventory, and a migration job template from `vars/aap_config.yml` |
| `playbooks/migrate_vms.yml` | MTV migration playbook the job template is pointed at |
| `playbooks/prechecks.yml`, `playbooks/batch_scan.yml` | Early pre-check entry points |
| `playbooks/execute_mtv_migration.yml` | Alternate migration sketch. Not wired to the job template |
| `vars/` | Shared settings, check definitions, and Ansible Vault files |
| `roles/` | NAD checks, MTV pre-checks, notifications, and a few roles that are still empty |

## Prerequisites

On the machine that runs the playbooks:

- `oc`
- `ansible-playbook` 2.15 or newer
- AWS credentials that can describe the ROSA VPC and create RDS, subnet, and security group resources
- An OpenShift user that can create namespaces, secrets, jobs, operator subscriptions, and the AAP custom resource. The playbooks log in as `cluster-admin` unless you override `openshift_username`
- A Red Hat subscription manifest at `manifest.zip` in the repo root, if you want the deploy playbook to apply a license
- Python packages `boto3` and `botocore` for the AWS modules

Collections used by the RDS and AAP playbooks:

```bash
ansible-galaxy collection install -r requirements.yml kubernetes.core
```

`requirements.yml` installs `amazon.aws`, `ansible.controller`, `awx.awx`, `ansible.utils`, `community.general`, and `community.postgresql`. `kubernetes.core` is imported by the playbooks and is commented out in that file, so install it explicitly. The migration playbooks also import `community.vmware` and `infra.openshift_virtualization_migration`, which are not listed in `requirements.yml`.

Optional TLS files, picked up automatically when present:

- `certs/internal-ca.crt` becomes secret `aap-custom-ca-secret`
- `certs/tls.crt` and `certs/tls.key` become secret `aap-route-tls-secret`

Pass `-e custom_hostname=<fqdn>` to either AAP deploy playbook when the route should use a specific host.

## 1. Create the RDS instance

`deploy_rds.yml` looks up the ROSA VPC by a `Name` tag matching `*rosa*<cluster_identifier>*`, collects its subnets, and creates:

- subnet group `aap-rds-subnet-group`
- security group `aap-rds-sg`, allowing TCP 5432 from `0.0.0.0/0`
- a second subnet in another availability zone when the VPC has only one, because the subnet group needs two
- PostgreSQL 15 instance `aap-postgres-db` (`db.m6g.large`, 50 GB gp3, not publicly accessible, single-AZ)
- an in-cluster Job, `rds-init-job`, that creates user `aap_user` and databases `aap_gateway`, `aap_controller`, `aap_hub`, and `aap_eda`, plus the `hstore` extension on `aap_hub`
- secrets `rds-gateway-configuration`, `rds-controller-configuration`, `rds-hub-configuration`, and `rds-eda-configuration` in namespace `ansible-automation-platform`

```bash
ansible-playbook playbooks/deploy_rds.yml \
  -e "aws_access_key=<AWS_ACCESS_KEY>" \
  -e "aws_secret_key=<AWS_SECRET_KEY>" \
  -e "aws_region=us-east-2" \
  -e "cluster_identifier=<ROSA_CLUSTER_ID>" \
  -e "openshift_host=https://api.<cluster>.<domain>:443" \
  -e "openshift_password=<OPENSHIFT_PASSWORD>" \
  -e "db_master_password=<RDS_MASTER_PASSWORD>" \
  -e "db_app_password=<AAP_APP_PASSWORD>"
```

There is no playbook that deletes the RDS instance, subnet group, security group, or extra subnet.

## 2. Install AAP

Both deploy playbooks create namespace `ansible-automation-platform`, an `OperatorGroup`, a subscription to `ansible-automation-platform-operator` from `redhat-operators`, and an `AnsibleAutomationPlatform` resource named `aap`. Controller runs with 2 replicas. Hub is enabled with `ReadWriteOnce` storage and pod affinity so its pods stay on one node. EDA, Lightspeed, and metrics are disabled. The playbook waits for the admin secret and the route, then polls `/api/controller/v2/ping/`. If `manifest.zip` is present it posts that manifest to the controller config API.

The external-database install uses channel `stable-2.7` and the RDS secrets. Run it after `deploy_rds.yml`:

```bash
ansible-playbook playbooks/deploy_aap_w_rds.yml \
  -e "openshift_host=https://api.<cluster>.<domain>:443" \
  -e "openshift_password=<OPENSHIFT_PASSWORD>"
```

The in-cluster database install uses channel `stable-2.6` and does not set a database secret, so the operator creates its own PostgreSQL:

```bash
ansible-playbook playbooks/deploy_aap_local_db.yml \
  -e "openshift_host=https://api.<cluster>.<domain>:443" \
  -e "openshift_password=<OPENSHIFT_PASSWORD>"
```

Watch the rollout with:

```bash
oc get pods -n ansible-automation-platform -w
```

When the playbook finishes it prints the route, the `admin` username, and the generated admin password. You can read those later with:

```bash
oc get route aap -n ansible-automation-platform -o jsonpath='{"https://"}{.spec.host}{"\n"}'
oc get secret aap-admin-password -n ansible-automation-platform -o jsonpath='{.data.password}' | base64 -d; echo
```

## 3. Remove AAP

`destroy_aap.yml` deletes the `AnsibleAutomationPlatform` resource, the operator subscription, the operator group, and the namespace. It does not wait on finalizers, and it does not touch RDS.

```bash
ansible-playbook playbooks/destroy_aap.yml \
  -e "openshift_host=https://api.<cluster>.<domain>:443" \
  -e "openshift_password=<OPENSHIFT_PASSWORD>"
```

## 4. Seed AAP objects

`playbooks/config_aap.yml` logs in to the cluster, reads the AAP admin secret and route, and uses `ansible.controller` to apply `vars/aap_config.yml`. That file defines an Automation Hub credential, a Galaxy credential, vCenter credentials, an OpenShift bearer-token credential, a Git project (`scm_branch: main`), a VMware inventory source, and job template `01 - Execute OpenShift VM Migration` (`playbooks/migrate_vms.yml`).

Connection values come from `vars/vault.yml`. Decrypt that vault with the local vault password file before running the playbook.

## VM migration

The intended run is an AAP job using `playbooks/migrate_vms.yml`, limited to specific VM names from a vCenter inventory. That playbook selects a target OpenShift cluster, checks Changed Block Tracking when the migration is warm, powers source VMs off when it is cold, ensures the target namespace and MTV `NetworkMap` / `StorageMap` resources, includes `infra.openshift_virtualization_migration.mtv_management` and `mtv_migrate`, and on failure powers the source VMs back on and deletes the target `VirtualMachine` and matching PVCs.

It is not ready to treat as a documented procedure. The playbook still has open TODOs around cluster variable loading, `vars/migration_config.yml` is not included by it, and the cluster files it tries to load (`mda.yml`, `mny.yml`, `mty.yml`) are not the files under `vars/cluster_vars/`. `playbooks/execute_mtv_migration.yml` is a separate sketch with placeholder cluster values. Pre-checks live in `checks.md`, `playbooks/prechecks.yml`, `playbooks/batch_scan.yml`, and `roles/mtv_checks`, and several of those tasks are unfinished.

`roles/qemu-guest` and `roles/mtv_forkliftcontroller` have no tasks yet. `roles/ocp_nad` checks that expected NetworkAttachmentDefinitions exist. `roles/notify` can send a Slack message and is only called from `playbooks/test_notify.yml`.
