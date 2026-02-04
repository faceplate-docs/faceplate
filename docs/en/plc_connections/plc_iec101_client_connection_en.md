# IEC 60870-5-101 Client Configuration Guide

## General Description
The **IEC 101 Client** driver is designed for data exchange with telecontrol equipment (RTU) via serial communication channels (RS-232, RS-485) using the **IEC 60870-5-101** protocol. Unlike IEC 104 (TCP/IP), this protocol is oriented towards low-speed physical lines and requires precise configuration of link layer addressing.

The configuration process consists of two stages:
1.  **Connection (`plc_iec101_client_connection`):** Configuring the COM port, Link Layer parameters, and addressing.
2.  **Binding (`plc_iec101_client_binding`):** Addressing specific Information Objects (IOA).

---

## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)

At this stage, physical port parameters and specific IEC 101 protocol settings (address sizes, balance mode) are defined.

![IEC 101 Client connection settings](images/plc_iec101_client_conn.png)

### 1.1 Diagnostics Panel
> PLC connection diagnostics → [Diagnostics](./general_ru.md#диагностика-diagnostics)

| Field | Description |
| :--- | :--- |
| **State** | **STOP** — driver is stopped.<br>**RUN** — driver is running. |
| **Node** | Cluster node. Indicates on which node the process is running. |
| **PID** | Process ID. |
| **Error** | Error text (if any). |
| **Disabled** | Connection disable flag. Through this button, the user disables or enables the driver. |
| **Memory limit (bytes)** | Memory limit (RAM limits in bytes for the process serving the connection). Memory capacity determines the number of variables (tags) that can be processed. |
| **Actual connection** | Current active communication channel. In systems with Redundancy, indicates exactly which connection (primary or backup) is currently exchanging data. |
| **Master connection** | Link to the main communication channel. Filled for redundant connections. The field indicates which connection is the priority (Master), defining the logical pair for the redundancy mechanism. |

### 1.2 General Settings (Settings)
| Parameter | Description |
| :--- | :--- |
| **Name** | Unique name of the connection. |
| **Title** | Title (description) of this object. |
| **Period (ms)** | Base driver processing cycle. |
| **Shutdown timeout (ms)** | Waiting time for operations to complete when stopping the driver. |
| **Support for group requests** *| **Yes** — enable support for General Interrogation. |
| **Max. package length** *| Maximum packet size. Usually 250 bytes. |
| **Line Delay Ratio** *| Line delay coefficient. |

> *Note:* For this connection type, the parameters "Support for group requests*", "Max. package length*", and "Line Delay Ratio*" are not used. It is recommended to leave these settings at default.

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

### 1.3 Protocol Parameters (IEC 60870-5-101)
Critical settings that must strictly match the RTU configuration.

| Field | Description |
| :--- | :--- |
| **Common Address of ASDU** | **Station Address (CA).** Logical address of the device (RTU). |
| **Common Address Size** | Size of the ASDU address field. Standard: **1** or **2** bytes. |
| **Originator Address Size** | Size of the originator address field. Usually **1** byte (sometimes 0). |
| **Information Object Address Size** | Size of the object address (IOA). Usually **2** or **3** bytes. |
| **Link Address** | **Link Layer Address.** Used for addressing the physical device on the RS-485 bus (in unbalanced mode). Often matches the Common Address. |
| **Link Address Size** | Size of the link address field. Standard: **1** or **2** bytes (sometimes 0 for point-to-point mode). |
| **Balanced** | **Transmission Mode:**<br>• **Off (Unbalanced):** "Master-Slave" mode. The server polls devices sequentially (standard for RS-485).<br>• **On (Balanced):** Equal rights mode (Point-to-Point). Spontaneous transmission from both sides (more common for RS-232, fiber optics, full duplex). |

### 1.4 Port Settings (SERIAL)
| Field | Description |
| :--- | :--- |
| **Port** | Path to the COM port (Linux: `/dev/ttyS0`, Windows: `COM1`). |
| **Baud rate** | Transmission speed (e.g., `9600`). |
| **Parity** | Parity (None, Even, Odd). IEC 101 often requires `Even`. |
| **Stop bits** | Stop bits (1 or 2). |
| **Data bits** | Data bits (usually 8). |
| **Timeout** | Time to wait for a response from the device. |
| **Attempts** | Number of request attempts before issuing an error. |


---

## 2. Variable Configuration (Binding)

![IEC 101 Client binding settings](images/plc_iec101_binding.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)

### 2.1 Binding Parameters
| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | **R** (Read), **W** (Write), **RW** (Read/Write). |
| **Address** | **IOA (Information Object Address).** Object address. Numeric value. |
| **Type** | **ASDU Type.** Data format.<br>Examples: `1: M_SP_NA_1` (Single Point), `30: M_SP_TB_1` (Single Point + Time). More details at (https://support.kaspersky.com/kics-for-networks/3.0/206199) |
| **Parameter** | Value attribute: `Value`, `Quality` (DIQ/SIQ/QDS), `Timestamp` (TS). |

> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)

### 2.2 IOA Calculation (If defined by octets)
If the address in the memory map is defined by bytes (e.g., `10.2.0`), use the formula to convert it to a decimal number:
$$Address = Octet_1 + (Octet_2 \times 256) + (Octet_3 \times 256^2)$$

### 2.3 Remote Control and Write Parameters (When Access = RW / W)
![IEC 101 Read-Write binding settings](images/iec101_rw.png)
These fields appear only if **RW** or **W** mode is selected.
*Note:* For telecontrol (TU) commands, using `Access: RW` is mandatory.

| Field | Description |
| :--- | :--- |
| **Remote control type** | **Command Type (Command TypeID).**<br>ASDU type for sending the command.<br>Examples:<br>• `45: C_SC_NA_1` (Single Command)<br>• `46: C_DC_NA_1` (Double Command)<br>• `50: C_SE_NC_1` (Set Point Float) |
| **Remote control address** | **Command IOA.**<br>Object address for writing. Often matches the read address (`Address`), but sometimes they are separated (e.g., reading switch status via IOA 100, but controlling it via IOA 2100). |

---