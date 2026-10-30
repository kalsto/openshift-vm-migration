v0.1a - this document is a WIP and should be reviewed and updated as things progress
This is is a quick overview of the process for executing a migration.

Login to your AAP instance with the appropriate process


From here, you'll see the Overview of your AAP instance. On the left is the navigation pane. Click on `Automation Execution` to expand that menu item, then click on `Templates`


Within Templates, you will see different Job Templates, including one for Execute Migration. This is the primary job template.

If you click on the Template Name, it will bring it up into a new window. You can then click on the big blue `Launch template` button in the upper right corner. There's also a `launch template` button from the Templates page, which will bypass the extra click.


First screen on the next page is the Inventory. All of the vsphere inventories should be created in AAP so that you can simply select the correct vSphere inventory for the migration you're doing

Click blue `Next` button at the bottom of the page


Next you've got the survey - Here you specify the `Migration type` - we've defaulted to cold, but that can be changed to warm if that's the preference

The Cluster Short Name is required, and it's to indicate which variable file you want to load. the name you specify here must match the variable file you've added to the repository `vars/cluster_vars` directory

The `Upload CSV` text area is where you can paste the output of your csv directly from the Chef Migration Preparation tool. Skip the header line, and dump the rest of the vm's you want to migrate into that field.

`Scheduled time` is for when you want the migration to happen. This should be sometime in the future. By default, if you do NOT specify a time here, the system assumes you want the cutover to happen immediately, and it will treat your vm accordingly
- if this is a cold migration, this is fine. If you are wanting to pre-stage the data, you should provide a time sometime in the future.
- This date can be changed after the fact, so it's advisable that if you want to run a warm migration, give it a date 2 weeks out, then come back and adjust as necessary

Then you can hit the blue `Next` button at the bottom again, and once you've reviewed the job, you can hit the blue `Finish` at the bottom of your screen.


This will start the process for running the job. If you click on the `Automation Execution > Jobs` link on the left, you will be able to see when the job kicks off. Usually it will have a `Source control` update job that runs first.
Once the Playbook runs, you can click on it to follow the progress.


Please note, the prechecks should still be validated to ensure they are meeting the expectations of TT
Most of the post-checks are stubbed out, but haven't been fully tested.
Some of the Slack notifications have been made available, however an enhancement would be to capture the message-id of the initial message sent to slack, put it into a configmap or into an artifact within the job run, and then use that to update the message thread with updates.

