# SNMP Configuration in Faceplate

## General Description
**SNMP** (Simple Network Management Protocol) is an open communication protocol defined by the Internet Engineering Task Force (IETF). The protocol is widely used for data exchange with network equipment (controllers, gateways, UPS).

The **Faceplate** environment supports protocol versions **SNMPv2** and **SNMPv3**.

The integration process consists of two stages:
1.  **Creating a connection (`plc_snmp_connection`):** Configuring network transport and redundancy logic.
2.  **Creating bindings (`plc_snmp_binding`):** Addressing specific variables (OID) inside the device.

---

## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)
> 
At this stage, a transport channel to the equipment is created.

![Connection settings window](images/snmp_connections.png)

### 1.1 Diagnostics Panel
The upper part of the window displays the driver status.
> PLC connection diagnostics → [Diagnostics](./general_ru.md#диагностика-diagnostics)


| Field | Description |
| :--- | :--- |
| **State** | **STOP** — driver is stopped.<br>**RUN** — driver is running. |
| **Node** | Cluster node. Indicates on which node the process is running. |
| **PID** | Process ID. |
| **Error** | Error text. |
| **Disabled** | |
| **Memory limit (bytes)** | Memory limit (RAM limits (MB) for the process serving the connection). Memory capacity determines the number of variables (tags) that can be processed during the connection operation. |
| **Actual connection** | Current executable communication channel. In systems with Redundancy, indicates exactly which connection (primary or backup) is currently exchanging data. |
| **Master connection** | Link to the main communication channel. Filled for redundant connections. The field indicates which connection is the priority (Master), defining the logical pair for the redundancy mechanism. |

### 1.2 General Settings (Settings)

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique name of the connection. |
| **Title** | Title (description) of this object. |
| **Period (ms)** | Base driver processing cycle. |
| **Shutdown timeout (ms)** | Waiting time for correct connection termination. |
| **Support for group requests** | **Yes** — enable the possibility of periodic General Interrogation. |
| **Max. package length** | Maximum APDU size. Standard is 250 bytes. |
| **Line Delay Ratio** | Delay coefficient for slow communication lines. |


### 1.3 Protocol Parameters (SNMP) 
| Field | Description |
| :--- | :--- |
| **Community** | **Community String.** Used as a password for accessing device data (for SNMP v1/v2c).<br>• **public** — standard value for "read-only" rights.<br>• **private** — standard value for "read-write" rights.<br>*Important: This value is case-sensitive and must match the settings in the polled device.* |
| **IP** | IP address or domain name of the device to be polled.<br>Examples: `192.168.1.10` (network device) or `127.0.0.1` (local agent). |
| **Port** | SNMP agent network port.<br>Standard port for requests: **161**. |
| **Agent** | Agent identifier or additional driver parameter. Often defaults to `0` or `1`. |


---

## 2. Variable Configuration (Binding)

Inside the connection, `plc_snmp_binding` objects are created. Each object corresponds to one variable (OID) on the device.

![Binding settings window](images/snmp_bindings.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)

### 2.1 Binding Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | Variable access rights:<br>• **R** — Read (Read only).<br>• **W** — Write (Write only).<br>• **RW** — Read/Write (Read and write). |
| **Address** | **OID (Object Identifier).** Variable address in the SNMP hierarchy.<br>*Examples:* `1.3.6.1.2.1.1.1.0` (absolute) or `1.6.3.1` (relative, if supported). |


> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)

---