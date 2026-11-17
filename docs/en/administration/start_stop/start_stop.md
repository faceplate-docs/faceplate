# Starting and stopping a node

For the integration engineer.

# Contents

- [Glossary](#glossary)
- [Introduction](#introduction)
- [Main part](#main-part)
    - [Open files limit](#open-files-limit)
    - [Starting in a window and in the background](#starting-in-a-window-and-in-the-background)
    - [Starting in a window](#starting-in-a-window)
    - [Starting in the background](#starting-in-the-background)
    - [Checking the start](#checking-the-start)
    - [Node console](#node-console)
    - [Stopping](#stopping)
    - [Starting in a cluster](#starting-in-a-cluster)
- [Conclusion](#conclusion)

# Glossary

| Term | Meaning |
|---|---|
| Node | One running FACEPLATE server. A node name looks like `fp@<server>`, see [«Cluster nodes»](../nodes/nodes.md) |
| Installation directory | The folder on the server where FACEPLATE is installed. It contains the `bin`, `erts-<version>`, `etc`, `lib` and `releases` folders. After the first start the `logs` folder and the `DB` database appear in it, after a start in the background the `log` folder, and after the Git module is connected to a repository the `cvs` folder |
| Node console | The command line of a running node where commands are run |

# Introduction

A node is started and stopped with commands in a server terminal (for example, over SSH). Commands are run from the folder that contains the `faceplate` installation directory. The full list of commands is printed by `./faceplate/bin/faceplate` without parameters.

A node is started in a terminal window or in the background. This decides what happens to the node when the window is closed, and how its console is opened.

# Main part

## Open files limit

A node works only if its process may open at least 200,000 files. The limit is set with `ulimit -n` in the same terminal before the start:

```bash
ulimit -n <limit>
```

`<limit>` is a number from 200,000. The command acts only in this terminal, so it is repeated before every start.

With a lower limit the node process starts, but FACEPLATE does not work: Studio does not open, and the line `ulimit <current> is less than minimum 200000` appears in `logs/console.log`, `logs/error.log` and where the start messages are shown: in the terminal window (start in a window) or in `log/erlang.log.<number>` (start in the background). Stop the node (see [«Stopping»](#stopping)), set the limit and start again.

## Starting in a window and in the background

| | In a window (`console`) | In the background (`daemon`) |
|---|---|---|
| Where start messages are shown | In the terminal window | In the `log/erlang.log.<number>` file of the installation directory |
| Node console | Open in this window | Opened with `remote_console`, see [«Node console»](#node-console) |
| The terminal window or SSH session is closed | The node stops | The node keeps working |

With either way of starting, errors are written to the server logs, see [«Server logs»](../logs/logs.md).

## Starting in a window

```bash
ulimit -n <limit>
./faceplate/bin/faceplate console
```

The window is taken by the node. Do not close it or break the SSH session while the node must work.

## Starting in the background

```bash
ulimit -n <limit>
./faceplate/bin/faceplate daemon
```

The command returns the terminal at once, and the node starts in the background.

## Checking the start

The node has started when:

- the terminal window (start in a window) or `log/erlang.log.<number>` (start in the background) shows the line `----------------FACEPLATE STARTED----------------------------`;
- Studio opens: `http://<server>:9000/fp/studio`.

The `./faceplate/bin/faceplate ping` command answers `pong` if the node process works, and `Node is not running!` if not. `pong` does not yet mean FACEPLATE works: with a low open files limit the node also answers `pong`.

## Node console

A node started in a window has its console open in that window. To a node started in the background the console is connected from another terminal:

```bash
./faceplate/bin/faceplate remote_console
```

Each command is typed in full, with the dot at the end, and Enter is pressed.

To leave `remote_console` without stopping the node, press Ctrl+G, type `q` and press Enter. The `q().` command stops the node itself.

## Stopping

```bash
./faceplate/bin/faceplate stop
```

The command works for a node started both in a window and in the background. If the node is started in a window, run it in another terminal. The command ends when the node is stopped; after that `ping` answers `Node is not running!`.

## Starting in a cluster

Cluster nodes are started and stopped with the same commands as a single node. A variable at the start is needed in two cases: a node is attached to a cluster for the first time, or the cluster is started after all nodes were stopped. The [open files limit](#open-files-limit) is set before these commands too. For what to configure on the servers so that nodes join into a cluster, see [«Storages», section «Preparing the servers»](../../data_storage/storage/storage.md#preparing-the-servers).

### Attaching a node to a cluster

A node with an empty `DB` folder in the installation directory is attached: a new installation or a node whose `DB` folder was deleted. It is started for the first time with the `ATTACH_TO` variable set to the name of a running cluster node:

```bash
ulimit -n <limit>
env ATTACH_TO=fp@<server> ./faceplate/bin/faceplate console
```

`fp@<server>` is the name of a node that already works in the cluster. To start the node in the background, write `daemon` instead of `console`. The node joins the cluster and works with its database. The variable is needed only at the first start: after that the node is started as usual, see [«Starting in a window»](#starting-in-a-window) and [«Starting in the background»](#starting-in-the-background). For the **Servers** panel, see [«Cluster nodes»](../nodes/nodes.md).

If the node already has its own database, `ATTACH_TO` has no effect: the node starts as a separate cluster with its own database, and there is no error message. So after the start check that the node is shown on the **Servers** panel of the other nodes.

### Starting after a full cluster stop

If all cluster nodes are stopped, at startup they wait for each other: any of them may hold data the others lack. Meanwhile `logs/console.log` repeats the lines `trying to connect to 'fp@<node>' node` and `There were active nodes ['fp@<node>'], when the node went down`.

To get the cluster running, the node stopped last is started first, with the `FORCE_START` variable. It allows the node to open the database without waiting for the others:

```bash
ulimit -n <limit>
env FORCE_START=true ./faceplate/bin/faceplate console
```

To start in the background, write `daemon` instead of `console`. After that the other nodes are started as usual, see [«Starting in a window»](#starting-in-a-window) and [«Starting in the background»](#starting-in-the-background).

`FORCE_START` is set for one node and only for this start. A node with this variable treats its data as the most recent, and changes that reached only the other nodes are lost. The most recent data is on the node stopped last, so that node gets the variable.

# Conclusion

Before the start the open files limit is set to at least 200,000. A node is started in a window (`console`) or in the background (`daemon`): in a window the node works while the terminal is open, in the background regardless of it. The start is confirmed by the `FACEPLATE STARTED` line and an open Studio. The console of a running node is opened with `remote_console`, the node is stopped with `stop`. A node is attached to a cluster for the first time by starting it with `ATTACH_TO`, and after all nodes were stopped the node stopped last is started first with `FORCE_START`.
