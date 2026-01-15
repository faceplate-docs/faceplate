# 📘 DCON (ICP DAS) Configuration in Faceplate

## General Description
**DCON** is an ASCII-based industrial protocol developed by ICP DAS. It is widely used for polling I/O modules (I-7000, M-7000 series) and converters.

The DCON driver in the **Faceplate** system is multi-transport. It allows for communication to be established in two ways:
1.  **TCP (Ethernet):** Operation via network gateways (e.g., Moxa NPort, tDS-700) or with modules possessing a built-in Ethernet interface.
2.  **Serial (COM):** Direct connection to the server via an RS-485 port or USB converter.

The configuration process consists of two stages:
1.  **Connection:** Configuration of the physical transport layer.
2.  **Binding:** Addressing of the logical device and channel.

---

## STEP 1. Connection Configuration (`plc_dcon_connection`)

At this stage, the parameters for the data exchange channel ("pipe") are defined. The set of available fields changes dynamically depending on the selected **Type**.

### 1.1 Runtime Panel (Diagnostics)
*Used for real-time process monitoring.*

![DCON Diagnostics](images/dcon_connection.png)

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — Driver is stopped.<br>**RUN** (Green) — Polling is active. |
| **Error** | Text of the last error (e.g., `Port busy` or `Timeout`). |
| **Node / PID** | Cluster node and OS Process ID (useful for debugging COM port locks). |
| **Actual connection** | Indicates the active channel (Master or Backup) when redundancy is used. |

### 1.2 General Settings
*These parameters are relevant for any connection type.*

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Polling frequency. *Recommendation:* Set to >500 ms for Serial/RS-485 to avoid collisions. |
| **Type** | **Transport Mode Selector:**<br>• `tcp` — Network connection.<br>• `serial` — Direct connection via COM port. |
| **Master connection** | Reference to the main connection (used only when configuring a backup channel). |

---

### 1.3 Transport Configuration (Depending on Type)

#### Option A: `serial` Mode (Direct Connection)
Used if the daisy chain of modules is physically wired to the server.

![Serial Configuration](images/dcon_serial.png)

| Field | Description |
| :--- | :--- |
| **Port** | System path to the port.<br>• Linux: `/dev/ttyS0`, `/dev/ttyUSB0`<br>• Windows: `COM1`, `COM3` |
| **Baud rate** | Transmission speed (DCON Standard: `9600`). Must match the module settings. |
| **Parity** | Parity check (Usually `no`). |
| **Stop bits** | (Usually `1`). |
| **Data bits** | (Usually `8`). |

#### Option B: `tcp` Mode (Network Gateway)
Used if the modules are located remotely behind an Ethernet-to-RS485 converter.

![TCP Configuration](image_25dde7.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | IP address of the gateway or module. |
| **Port** | TCP port of the gateway (often `502`, `4001`, or `1024`). |
| **Timeout** | Network response wait time. |

> **Action:** Click **Save**, then double-click the connection object to create bindings.

---

## STEP 2. Variable Configuration (`plc_dcon_binding`)

Configuration of specific data points. One Binding object = One module channel.

![Binding Configuration](images/dcon_bindings.png)

### 2.1 Addressing Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name. |
| **Tag** | System tag for storing the value. |
| **Access** | **R** (Read), **W** (Write). |
| **Address** | **NetID (Network Address).** Set via DIP switches on the module housing (0-255). |

### 2.2 Module Configuration (Module Settings)
*Describes the physical capabilities of the hardware.*
* **DI / DO / AI / AO:** Specify the number of channels of the corresponding type on the module.
    * *Example:* For I-7017 (8 AI), set `AI: 8`, and the rest to `0`.

### 2.3 Channel Configuration (Channel Settings)
*Selects the specific "pin".*
* **Type:** Data type (e.g., Analog Input).
* **Channel:** Channel number (zero-based indexing).
* **Format:** Data format (`HEX` — hexadecimal, `Dec` — decimal). Important for parsing the response.

---

## 💡 Analyst's Troubleshooting Checklist

1.  **Port Access (Linux/Serial):** If a permission error occurs with `Type: serial`, ensure the user running the Faceplate service is a member of the `dialout` (or `uucp`) group.
2.  **Baud Rate:** DCON does not support auto-negotiation. The speed in the connection settings must **strictly** match the speed of all modules on the line.
3.  **Gateway Mode (TCP):** If using an NPort or similar device, ensure it is configured in **TCP Server** mode, and the internal RS-485 parameters (baud rate, parity) match the modules.
4.  **Addressing:** Ensure the correct ID is specified in the `Address` field. If the ID is incorrect, there will be no response (as it is a request-response protocol).