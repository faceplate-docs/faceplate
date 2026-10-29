# IEC 60870-5-101 Client Configuration Guide

> See also: [PLC Connections overview](./general_en.md)

## Overview
The **IEC 101 Client** driver exchanges data with telecontrol equipment (RTU) over serial links (RS-232, RS-485) using **IEC 60870-5-101**. Unlike IEC 104 (TCP/IP), this protocol targets low-speed physical lines and requires precise link-layer addressing.

Configuration is done in two stages:
1. **Connection (`plc_iec101_client_connection`):** COM port, link layer parameters, and addressing.
2. **Binding (`plc_iec101_client_binding`):** Address specific information objects (IOA).

---

## 1. Connection setup (Connection)
> Create a PLC connection -> [Create a PLC connection](./general_en.md#create-a-plc-connection)

This step defines physical port parameters and IEC 101 protocol settings (address sizes, balanced/unbalanced mode).

<img src="images/plc_iec101_client_conn.png" alt="IEC 101 Client connection setup" width="600">

> Diagnostics and common settings are described in [Common connection settings](./general_en.md#common-connection-settings).
>
> For this connection type, **Support for group requests**, **Max. package length**, and **Line Delay Ratio** are not used. Keep defaults.

### 1.1 Group request setup
Group Requests are used to organize polling. They allow splitting polled signals into logical groups (for example, by update rate). Group 20 (General Interrogation) is typically used.

**Group list management:**
1. **Add a group:** Use the UI controls to add a new row.
2. **Delete a group:** Click the trash icon (Delete) on the row.
3. **Order:** Use **up** and **down** arrows to change poll priority.

**Group parameters:**
| Field | Description |
| :--- | :--- |
| **Group number** | Group ID used internally and aligned with the standard. |
| **Update frequency (ms)** | Polling period for tags in the group. |
| **Timeout (ms)** | Response timeout for this group. |

### 1.2 Protocol parameters (IEC 60870-5-101)
Critical settings that must match the RTU configuration.

| Field | Description |
| :--- | :--- |
| **Common Address of ASDU** | **Station address (CA).** Logical device address (RTU). |
| **Common Address Size** | ASDU address size. Standard: **1** or **2** bytes. |
| **Originator Address Size** | Originator address size. Usually **1** byte (sometimes 0). |
| **Information Object Address Size** | IOA size. Usually **2** or **3** bytes. |
| **Link Address** | **Link-layer address.** Used to address the physical device on RS-485 (unbalanced mode). Often matches the Common Address. |
| **Link Address Size** | Link address size. Standard: **1** or **2** bytes (sometimes 0 for point-to-point). |
| **Balanced** | **Transmission mode:**<br>- **Off (Unbalanced):** Master-Slave. The server polls devices sequentially (standard for RS-485).<br>- **On (Balanced):** Peer-to-peer (point-to-point). Spontaneous transfer both ways (common for RS-232, fiber, full duplex). |

### 1.3 Serial port settings (SERIAL)
| Field | Description |
| :--- | :--- |
| **Port** | COM port path (Linux: `/dev/ttyS0`, Windows: `COM1`). |
| **Baud rate** | Baud rate (for example, `9600`). |
| **Parity** | Parity (None, Even, Odd). IEC 101 often requires `Even`. |
| **Stop bits** | Stop bits (1 or 2). |
| **Data bits** | Data bits (usually 8). |
| **Timeout** | Response timeout. |
| **Attempts** | Number of retries before error. |

---

## 2. Binding setup (Binding)

<img src="images/plc_iec101_binding.png" alt="IEC 101 Client binding setup" width="600">

> Create a PLC binding -> [Create a PLC binding](./general_en.md#create-a-plc-binding)

> Common binding fields are described in [Common PLC binding fields](./general_en.md#common-plc-binding-fields).

### 2.1 Binding-specific parameters
| Field | Description |
| :--- | :--- |
| **Address** | **IOA (Information Object Address).** Numeric address. |
| **Type** | **ASDU type.** Data format.<br>Examples: `1: M_SP_NA_1` (Single Point), `30: M_SP_TB_1` (Single Point + Time). See (https://support.kaspersky.com/kics-for-networks/3.0/206199) |
| **Parameter** | Value attribute: `Value`, `Quality` (DIQ/SIQ/QDS), `Timestamp`. |

> Binding error -> [Binding errors](./general_en.md#binding-errors)

### 2.2 IOA calculation (if specified by octets)
If the address is given in bytes (for example, `10.2.0`), use the formula:
$$Address = Octet_1 + (Octet_2 \times 256) + (Octet_3 \times 256^2)$$

### 2.3 Remote control and write parameters (Access = RW / W)
<img src="images/iec101_rw.png" alt="IEC 101 read-write binding setup" width="600">
These fields appear only if **RW** or **W** is selected.
*Note:* For remote control commands (TU), `Access: RW` is required.

| Field | Description |
| :--- | :--- |
| **Remote control type** | **Command TypeID.** ASDU type used to send commands.<br>Examples:<br>- `45: C_SC_NA_1` (Single Command)<br>- `46: C_DC_NA_1` (Double Command)<br>- `50: C_SE_NC_1` (Setpoint float) |
| **Remote control address** | **Command IOA.** Address used for writing. Often matches `Address`, but can differ (for example, read status at IOA 100 and control at IOA 2100). |

---