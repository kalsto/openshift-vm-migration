The point of this vars folder is to make it easier to make changes.

The checks_* files are for adding pre/post checks to the migration workflow.
Talk about the waarning levels
Talk about the messages
Talk about where the checks are run and how to change that


The all.yml file contains the list of variables that we require in order to run a migration.
The all_vault.yml file contains the vaulted variables that all.yml is expecting. It will also include variables that are required throughout all plays (such as the local user information)

The <cluster short name> (example, m-ty, or m-ny) contain _cluster specific configuration_ which will override the variables in the all_vault.yml where appropriate.
    

For each new cluster, you'll need to do the following:
Copy seed_vault.yml to be your new cluster name
Fill in the details
If the vlan list is different from the expected (in the all.yml var file), then provide a list of expected vlan's
