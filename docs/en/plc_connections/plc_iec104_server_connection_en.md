# IEC 60870-5-104 Server Configuration Guide

## General Description
The **IEC 104 Server** driver allows the **Faceplate** system to act as a Controlled Station (Slave/RTU). In this mode, the system opens a TCP port and awaits connections from external Controlling Stations (Top-level SCADA, Control Centers), transmitting internal tag data to them and accepting control commands.

The configuration process consists of two stages:
1.  **Connection (`plc_iec104_server_connection`):** Configuring the TCP port, ASDU addressing, and protocol timing parameters.
2.  **Binding (`plc_iec104_server_binding`):** Publishing specific tags to the protocol address space (IOA) and configuring command acceptance parameters.

---

## STEP 1. Connection Configuration

At this stage, the listening socket and link layer parameters are configured. These settings must match the configuration of the Client (Master) that will connect to Faceplate.

![IEC 104 Server Connection Settings](images/iec104_server.png)

### 1.1 Diagnostics Panel (Runtime)
The upper part of the window displays the server process status.

| Field | Description |
| :--- | :--- |
| **State** | **STOP** — server is stopped, port is closed.<br>**RUN** — server is running and listening for connections. |
| **Error** | Error text (e.g., `Address already in use` if port 2404 is occupied by another application). |
| **Actual connection** | Indicator of the active connection (relevant for server redundancy). |

### 1.2 General Settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name in the system. |
| **Period (ms)** | Internal driver event processing cycle. |
| **Shutdown timeout (ms)** | Time allowed for graceful closure of TCP sessions when stopping the driver. |
| **Support for group requests** | **Yes** — Allow processing of "Interrogation Commands" from the client. Recommended to be enabled. |
| **Max. package length** | Maximum APDU (Application Protocol Data Unit) size. Standard value: **250**. |
| **Line Delay Ratio** | Line delay coefficient (used for timeout calculation on slow channels). |

### 1.3 Protocol Parameters

| Field | Description |
| :--- | :--- |
| **Port** | TCP port for incoming connections. IANA Standard: **2404**. |
| **Originator Address** | The originator address the server inserts into its responses by default (usually 0). |
| **Common Address of ASDU** | **Station Address (CA).** The unique number of this device in the IEC 104 network. Must match the Client settings. |
| **Common Address Size** | Size of the ASDU address field in bytes. Standard: **2 bytes**. |
| **Originator Address Size** | Size of the originator address field. Standard: **1 byte** (sometimes 0). |
| **Information Object Address Size** | Size of the Information Object Address (IOA) field. Standard: **3 bytes**. |
| **K** | Parameter **k** (APDU transmit window). Maximum number of transmitted APDUs without acknowledgement. |
| **W** | Parameter **w** (APDU receive window). Maximum number of received APDUs before sending an acknowledgement. |
| **T1 (ms)** | Time-out for send confirmation. |
| **T2 (ms)** | Time-out for acknowledgement in case of no data message. |
| **T3 (ms)** | Time-out for send test frames. Interval for sending `TESTFR` if the channel is idle. |

**Group broadcast:**
Allows configuring periodic transmission of data for specific groups, even if the client has not explicitly requested them.
* *Group number / Update frequency / Timeout.*

**Accept updates via information objects:**
Special option. If enabled (**On**), a Client writing a value to an IOA will update the value of the linked tag within the Faceplate system. Used for gateway implementation or receiving setpoints.

---

## STEP 2. Variable Configuration (Binding)

This stage defines the list of signals the server will expose "upstream".

![IEC 104 Server Binding Settings](images/iec104_server_bindings.png)

### 2.1 General Parameters
| Field | Description |
| :--- | :--- |
| **Name** | Binding object name. |
| **Tag** | **Source Tag.** The internal Faceplate tag whose value will be translated into the protocol. |
| **Access** | Access mode for the Client:<br>• **R** — Client can only Read (Monitoring/TM).<br>• **RW** — Client can Read and send Control Commands (Telecontrol/TC). |
| **Address** | **IOA (Information Object Address).** The number under which the tag is visible on the network. (See calculation below). |
| **Type** | **ASDU Type.** Data format for transmission.<br>Examples: `M_SP_NA_1` (Single Point), `M_ME_NC_1` (Float Measurement). |
| **Parameter** | Tag attribute to transmit: `Value`, `Quality`, `Timestamp`. |

### IOA Address Calculation
If the IOA is defined by octets (bytes) in the address map, use the Little-Endian formula:
$$Address = Octet_1 + (Octet_2 \times 256) + (Octet_3 \times 65536)$$

### 2.2 Remote Control Parameters
These fields become active and mandatory if `Access` is set to **RW**. They define how the server handles incoming commands.

| Field | Description |
| :--- | :--- |
| **Remote control type** | **Command Type.**<br>The ASDU type the server expects to receive from the client to control this object.<br>Examples: `C_SC_NA_1` (Single Command), `C_SE_NC_1` (Setpoint Float). |
| **Remote control address** | **Command IOA.**<br>The address to which the client must send the control command. Often matches the monitoring address (`Address`), but can differ. |
| **Group** | The Interrogation Group number this signal belongs to (usually 20 — General Interrogation). |

---

<!-- ## System Analyst Checklist

1.  **Network Access:** Ensure TCP port **2404** is open in the inbound Firewall rules on the server running Faceplate.
2.  **Type Matching:** The ASDU type in the `Type` field determines how the server *packs* the data before sending. Ensure the receiving side (SCADA) is configured to receive exactly this data type (e.g., distinguishing Float from Normalized value).
3.  **Feedback (RW):** To implement full control (TU), you must not only configure the `Remote control address` but also ensure that changing the tag in the Faceplate system results in actual action on the equipment. -->