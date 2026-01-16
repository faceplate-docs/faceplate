# IEC 60870-5-101 Server Configuration Guide

## General Description
The **IEC 101 Server** driver allows the **Faceplate** system to operate as a Controlled Station (Slave) via serial interfaces (RS-232/485). In this mode, the system awaits requests from an external Controlling Station (Master), transmits data, and executes telecontrol commands.

The configuration process consists of two stages:
1.  **Connection (`plc_iec101_server_connection`):** Configuring the COM port, physical layer, and addressing parameters.
2.  **Binding (`plc_iec101_server_binding`):** Defining the address map (IOA) and control parameters.

---

## STEP 1. Connection Configuration

At this stage, port parameters and protocol logic are defined. These must strictly match the Master settings.

![IEC 101 Server Connection Settings](images/plc_iec101_server_conn.png)

### 1.1 Diagnostics Panel (Runtime)
| Field | Description |
| :--- | :--- |
| **State** | **STOP** — server is stopped.<br>**RUN** — server is running, port is open. |
| **Error** | Error text (e.g., unable to open COM port). |
| **Actual connection** | Currently active channel (for redundancy). |

### 1.2 General Settings (Settings)
| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Internal event processing cycle. |
| **Shutdown timeout (ms)** | Wait time during driver shutdown. |
| **Support for group requests** | **Yes** — respond to General Interrogation commands. |
| **Max. package length** | Maximum packet size (usually 250). |
| **Line Delay Ratio** | Response delay coefficient (for slow lines). |

### 1.3 Protocol and Addressing Parameters
| Field | Description |
| :--- | :--- |
| **Common Address of ASDU** | **Station Address (CA).** The logical address of this device. |
| **Common Address Size** | Size of the ASDU address field (1 or 2 bytes). |
| **Originator Address Size** | Size of the originator address field (1 byte or 0). |
| **Information Object Address Size** | Size of the IOA field (2 or 3 bytes). |
| **Link Address** | **Link Layer Address.** Used in Unbalanced mode for bus addressing. |
| **Link Address Size** | Size of the link address field (1 or 2 bytes). |
| **Balanced** | **Transmission Mode:**<br>• **Off (Unbalanced):** Master-Slave. Normal mode for RS-485.<br>• **On (Balanced):** Point-to-Point. Peer-to-Peer mode (usually RS-232). |

### 1.4 Serial Port Settings (SERIAL)
| Field | Description |
| :--- | :--- |
| **Port** | Port name (e.g., `/dev/ttyUSB0` or `COM1`). |
| **Baud rate** | Transmission speed (9600, 19200, etc.). |
| **Parity** | Parity checking. The de-facto standard for IEC 101 is **Even**. |
| **Stop bits** | Stop bits. |
| **Data bits** | Data bits (usually 8). |
| **Timeout** | Byte wait timeout on the line. |
| **Attempts** | Number of retries (relevant for balanced mode). |

**Group broadcast:** Configuration for periodic spontaneous transmission of specific group data without a Master request.
**Accept updates via information objects:** Allow changing internal tags when writing to the IOA (gateway mode).

---

## STEP 2. Variable Configuration (Binding)

Defining the list of signals to transmit to the Master.

![IEC 101 Server Binding Settings](images/plc_iec101_server_binding.png)

### 2.1 Binding Parameters
| Field | Description |
| :--- | :--- |
| **Name** | Binding name. |
| **Tag** | Internal Faceplate tag. |
| **Access** | **R** (Monitoring), **RW** (Monitoring + Control). |
| **Address** | **IOA (Information Object Address).** Object address. |
| **Type** | **ASDU Type.** Data format for transmission (e.g., `M_SP_NA_1`). |
| **Parameter** | Tag attribute (`Value`, `Quality`, `Timestamp`). |

### 2.2 Remote Control Parameters
Fields active when `Access = RW`.

| Field | Description |
| :--- | :--- |
| **Remote control type** | Command type expected from the Master (e.g., `C_SC_NA_1`). |
| **Remote control address** | IOA for the control command. |
| **Group** | Interrogation group (usually 20). |