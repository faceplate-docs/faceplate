# Minor update and patch

For the integration engineer. The version number, update types and log lines at node startup are described in [«FACEPLATE version and update»](update.md).

# Contents

- [Glossary](#glossary)
- [Introduction](#introduction)
- [Main part](#main-part)
    - [How the update goes](#how-the-update-goes)
    - [Update procedure](#update-procedure)
- [Conclusion](#conclusion)

# Glossary

| Term | Meaning |
|---|---|
| Node | One running FACEPLATE server. A node name looks like `fp@<server>`, see [«Cluster nodes»](../nodes/nodes.md) |
| Cluster | Nodes that work together with one project and one database |
| Installation directory | The folder on the server where FACEPLATE is installed. It contains the `bin`, `erts-<version>`, `etc`, `lib` and `releases` folders. After the first start the `logs` folder and the `DB` database appear in it, after a start in the background the `log` folder, and after the Git module is connected to a repository the `cvs` folder |

# Introduction

With a minor update and a patch, the new version starts on the previous version's database and migrates it to its own format. The project, archives and event log stay in the database and pass to the new version; there is nothing to move.

Cluster nodes are updated one at a time. While a node is being updated, the others keep working, so Runtime does not stop. A new-version node joins the previous-version nodes and works together with them until all nodes are updated. With a single node, Runtime stops for the time of the update.

You need access to the servers' files (for example, over SSH) and Studio.

# Main part

## How the update goes

1. One node is stopped; the others keep working.
2. On this node's server the installation directory is copied to a backup folder, and the new version is unpacked over the installation directory itself. The database stays where it is.
3. The node is started as usual. The first updated node migrates the cluster database to the new version; the previous-version nodes keep working with it.
4. Once the node is confirmed to work, the next one is updated the same way.

In the example the cluster has nodes `fp@server1.fp` and `fp@server2.fp`. Commands are run from the folder that contains the `faceplate` installation directory.

## Update procedure

Steps 1–3 are done once, steps 4–10 for the first node, step 11 for each next node.

### 1. Review

Read the release notes of the new version.

### 2. Connect

Check that all nodes are working: Studio, the **Servers** panel, see [«Cluster nodes»](../nodes/nodes.md).

Connect to the server of the node you are updating.

### 3. Export

Save a project export file, see [«Project import and export», section «Export»](../../project_objects/import_export/import_export.md#export). It is a spare copy of the project objects. It is needed if, after a failed update, the backup of the installation directory made in step [5](#5-save) cannot be restored.

### 4. Stop

Stop the node, see [«Starting and stopping a node», section «Stopping»](../start_stop/start_stop.md#stopping). The other nodes keep working, and Runtime runs on them.

### 5. Save

Make a backup of the installation directory together with the `DB` database and the `logs` logs, for example into the `faceplate_backup` folder. The installation directory is copied, not moved: in step [7](#7-copy) the new version is unpacked over the installation directory itself, and the copy in `faceplate_backup` stays unchanged.

### 6. Check

Check that `/etc/hosts` on the server lists all cluster nodes, see [«Storages», section «Preparing the servers»](../../data_storage/storage/storage.md#preparing-the-servers).

### 7. Copy

Copy the new version's distribution to the server and unpack it over the installation directory.

The distribution has no `DB`, `logs` or `cvs` folders, so unpacking does not touch them: the database, the logs and the Git module's connection in the installation directory are kept. There is no need to move them from `faceplate_backup`. If the distribution is unpacked into an empty folder, the node starts with an empty database and creates a new project.

### 8. Change

Unpacking puts the new version's `faceplate/releases/<version>/vm.args` file with default values. Copy into it the values from the previous file, saved in `faceplate_backup/releases/<previous version>/vm.args`:

| Parameter | Value |
|---|---|
| `-name` | The previous node name, for example `fp@server1.fp` |
| `-setcookie` | The previous cookie, the same on all cluster nodes |
| `+MIscs` | The previous value |

Parameters are described in [«Redundancy», section «Virtual machine settings (vm.args)»](../redundancy/redundancy.md#virtual-machine-settings-vmargs).

The database remembers the names of its nodes. If the name in `vm.args` differs from the previous one, the node does not start: it waits for the node with the previous name. `console.log` repeats the lines `trying to connect to 'fp@<previous name>' node` and `'fp@<previous name>' node is not available`, and Studio does not open. Stop the node, correct `-name` and start it again.

### 9. Start

Set the open files limit, see [«Starting and stopping a node», section «Open files limit»](../start_stop/start_stop.md#open-files-limit).

Start the node as usual, see [«Starting and stopping a node», section «Starting in a window»](../start_stop/start_stop.md#starting-in-a-window). The node joins the running cluster nodes.

The [server log](../logs/logs.md) of the first updated node must show the line `upgrade faceplate version from <previous> to <new>`: the node has migrated the cluster database to the new version. For the next nodes the database is already migrated, and the log shows `faceplate version <new>`.

### 10. Monitor

Check that:

- the [server log](../logs/logs.md) has no `error` or `crash` lines before Runtime starts. Only the lines `the attempt to obtain license failed` and `invalid license` are allowed: the node has no license, see [«Licensing», section «A node without a license»](../license/license.md#a-node-without-a-license);
- Studio and Runtime open at this node's address, the project tree is in place, **About** shows the new version;
- the **Servers** panel shows all cluster nodes working.

If the check fails, do not continue the update. Stop the node, put back its installation directory from `faceplate_backup` and start the node as usual: it joins the cluster in the previous version and receives from the running nodes the data written during the update. Make an archive of the logs and the database at the moment the new version started and hand it over to support.

How long to monitor depends on the project size.

### 11. Update

Update the next node the same way as the first one:

1. Stop the node — step [4](#4-stop).
2. Save its installation directory — step [5](#5-save).
3. Check the network settings — step [6](#6-check).
4. Unpack the distribution — step [7](#7-copy).
5. Copy the settings into `vm.args` — step [8](#8-change).
6. Start the node — step [9](#9-start).
7. Check the node — step [10](#10-monitor).

Repeat for each node not yet updated.

# Conclusion

Nodes are updated one at a time: a node is stopped, its installation directory is copied together with the database and logs to a backup folder, the new version is unpacked over the installation directory itself, and the previous node name, cookie and `+MIscs` are put back into `vm.args`. The node is started as usual and joins the running nodes. The first updated node migrates the cluster database, and the log shows `upgrade faceplate version from … to …`. Then the log, Studio, Runtime and the **Servers** panel are checked, and the next node is updated. While one node is being updated, Runtime runs on the others. On errors, the node gets its saved directory back and works in the cluster in the previous version.
