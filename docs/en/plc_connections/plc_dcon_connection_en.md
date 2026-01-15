# DCON (ICP DAS) Configuration in Faceplate

## Overview
**DCON** is an industrial ASCII-based protocol developed by **ICP DAS**. It is used to poll I/O modules (I-7000, M-7000 series) and various converters.

The **DCON driver** in **Faceplate** is **multi-transport**, meaning communication can be organized in two ways:
1. **TCP (Ethernet):** Operation via network gateways (e.g., Moxa NPort, tDS-700) or modules with built-in Ethernet.
2. **Serial (COM):** Direct connection to the server via an RS-485 port or a USB converter.

Configuration consists of two stages:
1. **Connection:** Physical transport setup.
2. **Binding:** Logical device and channel addressing.

---

## STEP 1. Connection setup (`plc_dcon_connection`)

At this stage you configure the “pipe” used for data exchange. The set of fields depends on the selected **Type**.

### 1.1 Diagnostic panel (Runtime)
*Used for real-time process state monitoring.*

![DCON Diagnostics](images/dcon_connection.png)

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — driver is stopped.<br>**RUN** (Green) — polling is running. |
| **Error** | Last error text (e.g., `Port busy` or `Timeout`). |
| **Node / PID** | Cluster node and OS process ID (useful for debugging COM port locks). |
| **Actual connection** | In redundancy mode shows the active channel (Master or Backup). |

### 1.2 General settings (Settings)
*These parameters apply to any transport type.*

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Polling interval. *Recommendation:* for Serial/RS-485 use >500 ms to avoid collisions. |
| **Type** | **Transport mode switch:**<br>• `tcp` — Network connection.<br>• `serial` — Direct COM port connection. |
| **Master connection** | Reference to the main connection (used only when configuring a backup channel). |

---

### 1.3 Transport setup (depends on Type)

#### Option A: `serial` mode (Direct connection)
Used when the module chain is physically connected to the server.

![Serial settings](images/dcon_serial.png)

| Field | Description |
| :--- | :--- |
| **Port** | System port path.<br>• Linux: `/dev/ttyS0`, `/dev/ttyUSB0`<br>• Windows: `COM1`, `COM3` |
| **Baud rate** | Communication speed (DCON default: `9600`). Must match the module settings. |
| **Parity** | Parity (usually `no`). |
| **Stop bits** | Stop bits (usually `1`). |
| **Data bits** | Data bits (usually `8`). |

#### Option B: `tcp` mode (Network gateway)
Used when modules are located remotely behind an Ethernet-to-RS485 converter.

![TCP settings](image_25dde7.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | Gateway or module IP address/hostname. |
| **Port** | TCP port of the gateway (commonly `502`, `4001`, or `1024`). |
| **Timeout** | Network response timeout. |

> **Action:** Click **Save**, then open the connection (Double Click) to create bindings.

---

## STEP 2. Variable setup (`plc_dcon_binding`)

Configure specific data points. One **Binding object = one module channel**.

![Binding setup](images/dcon_bindings.png)

### 2.1 Addressing parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name. |
| **Tag** | System tag used to store the value. |
| **Access** | **R** (Read), **W** (Write). |
| **Address** | **NetID (network address).** Set via DIP switches on the module (0–255). |

### 2.2 Module settings
*Describes physical capabilities of the hardware.*
- **DI / DO / AI / AO:** Specify the number of channels of each type on the module.  
  *Example:* For I-7017 (8 AI) set `AI: 8`, all others to `0`.

### 2.3 Channel settings
*Selects a specific “pin”.*
- **Type:** Data type (e.g., Analog Input).
- **Channel:** Channel number (indexing starts at 0).
- **Format:** Data format (`HEX` — hexadecimal, `Dec` — decimal). Important for response parsing.

---

<!-- ## Additional notes

1. **Port access (Linux/Serial):** If `Type: serial` fails due to permissions, ensure the user running Faceplate services is in the `dialout` (or `uucp`) group.
2. **Baud rate:** DCON does not support auto-negotiation. The connection baud rate must **exactly** match all modules on the line.
3. **Gateway mode (TCP):** If using NPort or similar, ensure it is configured as a **TCP Server** and RS-485 parameters (speed, parity) match the modules.
4. **Addressing:** Make sure the `Address` field contains the correct ID. With a wrong ID there will be no response (request-response protocol). -->
