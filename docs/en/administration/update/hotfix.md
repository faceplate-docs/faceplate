# Hotfix

For the integration engineer. The version number and update types are described in [«FACEPLATE version and update»](update.md).

# Contents

- [Introduction](#introduction)
- [Main part](#main-part)
    - [Hotfix types](#hotfix-types)
    - [Installing a frontend hotfix](#installing-a-frontend-hotfix)
    - [Installing a backend hotfix](#installing-a-backend-hotfix)
    - [Application project hotfix](#application-project-hotfix)
- [Conclusion](#conclusion)

# Introduction

A hotfix is an urgent bug fix without a new release. The version number does not change: **About** and the `faceplate version` line in `console.log` show the previous number.

A bug can be in the FACEPLATE program itself or in the application project. The program is the same in all installations of one version, the user does not change it. The part of the program that runs in the browser is called the frontend, the part that runs on the server is called the backend. The application project is everything the user creates and changes in Studio and Runtime for their site, for example mnemonic diagrams and scripts.

So there are three hotfix types:

- a frontend hotfix and a backend hotfix are files plus a description of which folders of the [installation directory](../start_stop/start_stop.md#glossary) they go into;
- an application project hotfix is a description of what to change in Studio or Runtime.

You need access to Studio (`http://<server>:9000/fp/studio`) and Runtime (`http://<server>:9000/fp/runtime`) under an account allowed to make the required changes. A frontend or backend hotfix also needs access to the server file system (for example, over SSH) to put the files into the installation directory, and to the node console.

# Main part

## Hotfix types

Frontend and backend hotfixes differ in how the node gets the new files. An application project hotfix does not touch files on the server. No hotfix requires stopping the node.

| | Frontend hotfix | Backend hotfix | Application project hotfix |
|---|---|---|---|
| What it fixes | The part of the program in the browser. For example, the Runtime menu does not open or a Studio window layout is broken | The part of the program on the server. For example, replication does not pass data to another FACEPLATE instance | The application project. For example, the script of a button on a mnemonic diagram writes the value to the wrong tag |
| How it is installed | Hotfix files are put into the installation directory | Hotfix files are put into the installation directory and loaded with commands in the node console | The application project is changed in Studio or Runtime following the hotfix description |
| How the node gets the fix | The node takes the interface files from the installation directory each time a page is opened | The node loads the new files on commands in the console, without a restart | The change is saved in the project |
| When the fix takes effect | When the user reloads the Studio or Runtime page and logs in again | Right after the commands in the node console | Depends on what is changed |
| Cluster | Files are replaced on every node | Files are replaced and commands are run on every node | The application project is shared by all nodes: the change is made once |

## Installing a frontend hotfix

1. Make a backup copy. One option for the project is an export file, see [«Project import and export», section «Export»](../../project_objects/import_export/import_export.md#export).
2. Unpack the hotfix archives into the module folder `lib/<module-name>-<version>` of the installation directory: into `priv` and/or into `priv/UI`, as stated in the hotfix description. Do not stop the node.
3. Reload the Studio page, log in and check the fix.
4. Ask Studio and Runtime users to reload the page: until then the browser works with the previous files.

In a cluster steps 1–2 are done on every node: each node serves its own files to the browser.

To undo the hotfix, restore the files from the backup copy and reload the page.

## Installing a backend hotfix

1. Make a backup copy. One option for the project is an export file, see [«Project import and export», section «Export»](../../project_objects/import_export/import_export.md#export).
2. Put the hotfix files into the folders from its description. The program files of a module are in the `lib/<module-name>-<version>/ebin` folder of the installation directory.
3. In the console of the running node (see [«Starting and stopping a node», section «Node console»](../start_stop/start_stop.md#node-console)), run for each module of the hotfix:

    ```erlang
    code:load_file(<module-name>).
    code:purge(<module-name>).
    <module-name>:on_init().
    ```

4. Check that the bug is fixed.

In a cluster steps 1–3 are done on every node. Nodes are not stopped, Runtime and Studio keep working.

To undo the hotfix, restore the files from the backup copy and run step 3 again.

## Application project hotfix

An application project hotfix is installed in Studio or Runtime following the hotfix description. No access to server files is needed, the node is not restarted. When the change takes effect depends on what is changed.

1. Save the project to an export file, see [«Project import and export», section «Export»](../../project_objects/import_export/import_export.md#export).
2. Note the previous values of what you change.
3. Make the changes from the hotfix description and check the fix.

To undo the hotfix, set the noted values back.

# Conclusion

A hotfix does not change the version number and does not require stopping the node. Frontend and backend hotfixes are installed by replacing files in the installation directory after making a backup copy: frontend takes effect after a page reload, backend after the commands in the node console. An application project hotfix is installed in Studio or Runtime.
