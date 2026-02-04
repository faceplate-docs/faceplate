# IEC 60870-5-104 Client Configuration Guide

## General Description
The **IEC 104 Client** driver is designed for data exchange with telecontrol equipment (RTU, substation controllers, protection relay terminals) via the **IEC 60870-5-104** protocol over TCP/IP networks.

The configuration process consists of two stages:
1.  **Connection (`plc_iec104_client_connection`):** Configuring the network connection, ASDU parameters, and protocol timings.
2.  **Binding (`plc_iec104_client_binding`):** Addressing specific information objects (IOA) and configuring telecontrol commands.

---

## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)

At this stage, physical connection parameters and specific IEC 104 protocol settings are defined.

![IEC 104 connection settings](images/plc_iec104_client_conn.png)

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
| **Actual connection** | Current active communication channel. In systems with Redundancy, indicates exactly which connection (primary or backup) is currently exchanging data. |
| **Master connection** | Link to the main communication channel. Filled for redundant connections. The field indicates which connection is the priority (Master), defining the logical pair for the redundancy mechanism. |

### 1.2 General Settings (Settings)

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique name of the connection. |
| **Title** | Title (description) of this object. |
| **Period (ms)** | Base driver processing cycle. |
| **Shutdown timeout (ms)** | Waiting time for correct disconnection. |
| **Support for group requests** | **Yes** — enable the possibility of periodic General Interrogation. |
| **Max. package length** | Maximum APDU size. Standard is 250 bytes. |
| **Line Delay Ratio** | Delay coefficient for slow communication lines. |

### 1.3 Protocol Parameters (IEC 60870-5-104 client)

These parameters must strictly match the settings in the slave device (RTU).

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | IP address of the slave device (Slave/Server). |
| **Port** | TCP port. |
| **Common Address of ASDU** | Station Common Address (CA). Unique identifier of the device on the bus. |
| **Common Address Size** | Size of the ASDU address field (usually **2** bytes). |
| **Originator Address Size** | Size of the originator address field (usually **1** byte, sometimes 0). |
| **Information Object Address Size** | Size of the object address field (IOA). Standard: **3** bytes. |
| **To** | TCP connection establishment timeout (t0). |
| **T1 (ms)** | Timeout for confirmation of sent APDU (t1). |
| **T2 (ms)** | Timeout for APDU reception confirmation (t2) in case of no data traffic. |
| **T3 (ms)** | Channel test timeout (t3). If the channel is idle for this time, a `TESTFR` frame is sent. |
| **W** | Transmit window size (w). Number of unacknowledged APDUs that can be received before sending a confirmation. |

### Group Request Configuration
The **Group Requests** table is used to organize data polling. It allows splitting polled signals into logical groups (e.g., to separate by data update frequency). Group 20 (General Interrogation) is typically used.

**Managing the Group List:**
1.  **Adding a group:** Use the interface controls to create a new row.
2.  **Deleting a group:** Click the button with the trash bin icon (Delete) to the right of the corresponding row.
3.  **Order:** Use the **↑** and **↓** arrows to change the group polling priority.

**Group Parameters:**
| Field | Description |
| :--- | :--- |
| **Group number** | Unique number (ID) of the polling group. Used for internal identification and standard compliance. |
| **Update frequency (ms)** | Group polling period in milliseconds. Determines how often the driver will request data updates for tags included in this group. |
| **Timeout (ms)** | Waiting time for a response from the device for this group of requests. |

---

## 2. Variable Configuration (Binding)

Configuring the binding of a specific telesignaling (TS) or telemetry (TM) signal.

![IEC 104 binding settings](images/plc_iec104_client_bindings.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)

### 2.1 Binding Parameters
| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | Access mode:<br>• **R** — Read only (Monitoring).<br>• **W** — Write only.<br>• **RW** — Read and Write (Telecontrol). |
| **Address** | **IOA (Information Object Address).** Information object address (Full Address). A number (e.g., `100`). [See address calculation section below](./plc_iec104_client_connection_ru.md#22-расчет-ioa-если-задан-октетами). |
| **Type** | **ASDU Type (TypeID).** Data type expected from the device.<br>Examples:<br>• `1: M_SP_NA_1` (Single Point)<br>• `30: M_SP_TB_1` (Single Point with CP56 timestamp)<br>• `13: M_ME_NC_1` (Measured float)<br>• `36: M_ME_TF_1` (Measured float with timestamp). More details at (https://support.kaspersky.com/kics-for-networks/3.0/206199)|
| **Parameter** | Value attribute: `Value`, `Quality` (DIQ/SIQ/QDS), `Timestamp` (TS). |

> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)


### 2.2 IOA Calculation (If defined by octets)
If the address in the memory map is defined by bytes (e.g., `10.2.0`), use the formula to convert it to a decimal number:
$$Address = Octet_1 + (Octet_2 \times 256) + (Octet_3 \times 256^2)$$

### 2.3 Remote Control and Write Parameters (When Access = RW / W)
![IEC 104 Read-Write binding settings](images/plc_iec104_clinet_rw.png)
These fields appear only if **RW** or **W** mode is selected.
*Note:* For telecontrol (TU) commands, using `Access: RW` is mandatory.

| Field | Description |
| :--- | :--- |
| **Remote control type** | **Command Type (Command TypeID).**<br>ASDU type for sending the command.<br>Examples:<br>• `45: C_SC_NA_1` (Single Command)<br>• `46: C_DC_NA_1` (Double Command)<br>• `50: C_SE_NC_1` (Set Point Float) |
| **Remote control address** | **Command IOA.**<br>Object address for writing. Often matches the read address (`Address`), but sometimes they are separated (e.g., reading switch status via IOA 100, but controlling it via IOA 2100). |

---