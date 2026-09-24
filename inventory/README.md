# In this directory, you need to create a vaulted variable file with the following values. They MUST follow this format, as they fill the variables required for the mtv process to be successful
# You can update the all.yaml variable file for Universal Variables, as they are discovered. These will be overridden if the same variables exist in the distinct variables.
# Create a variable file under inventory/group_vars that is named the same as the friendly name, and in the inventory.yaml, add a group with the appropriate host to it


# Universal variables - contained in the 'all.yaml' and the tt_all_vault.yaml files
vsphere_user:
vsphere_pass: 
vsphere_datastore: 
vsphere_storage_class: 
vddk_image_location: 
vsphere_port_group: 
cicd_vm_repo: 
github_deploy_pat: # or token, or something to push code to the {{ tt_cicd_vm_repo }}
mtv_namespace: # Not that secret, but for simplicity, put it in the vault
mtv_dest_namespace: 


# Distinct to each cluster
vcenter_host: 
openshift_host: 
openshift_username: 
openshift_password: 
openshift_token: 

