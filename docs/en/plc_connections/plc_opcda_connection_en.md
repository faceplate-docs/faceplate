# OPC DA (Classic) Configuration Guide

## Overview
**OPC DA (Data Access)** is the classic industrial data exchange standard based on Microsoft **DCOM** technology. In **Faceplate**, this driver allows connecting to external OPC servers (e.g., Kepware, Matrikon, Lectus) and reading data from them.

> **Important:** Because OPC DA relies on DCOM, successful connection often requires configuring Windows and DCOM permissions on both sides (Client and Server).

Configuration consists of two stages:
1. **Connection (`plc_opcda_connection`):** OPC server connection setup.
2. **Binding (`plc_opcda_binding`):** Subscription to specific tags.

---

## STEP 1. Connection setup (Connection)

Here you specify where the OPC server is located and how it is identified.

### 1.1 Diagnostic panel (Runtime)
*Top part of the window. Shows connection status.*

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — driver stopped.<br>**RUN** (Green) — connection established. |
| **Error** | Error text. Common: `Access Denied` (DCOM permissions) or `Server not found`. |
| **Actual connection** | Current active channel (when redundancy is used). |

### 1.2 Configuration settings (Settings)

![OPC DA Connection setup](images/opcda_conn.png)

#### Main parameters

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Data update period (OPC Group Update Rate). |
| **Shutdown timeout** | Time to wait for a graceful server disconnect. |
| **Master connection** | Reference to the main connection (for redundancy). |
| **Support for group requests** | **Yes** — use OPC Group mechanism for batch reads (recommended). |

#### Connection parameters (TCP / DCOM)
Unlike many other drivers, the network fields point to the host where the OPC Server is installed.

| Field | Description |
| :--- | :--- |
| **IP/Hostname/Localhost** | Network address of the computer running OPC Server.<br>*Example:* `192.168.1.5` or `localhost` (if on the same machine). |
| **Port** | **8100** (or another port if tunneling is used). <br>*Note:* Classic OPC DA does not use a fixed TCP port (it works via DCOM/RPC, TCP 135), but this field may be used for OPC tunnels or internal proxies in this driver. |
| **ServerID** | **OPC Server ProgID.** This is the most important field — it uniquely identifies the server COM component in the Windows registry.<br>*Examples:* `Kepware.KEPServerEX.V6`, `Matrikon.OPC.Simulation.1`, `ICONICS.SimulatorOPCDA.2`. |

---

## STEP 2. Variable setup (Binding)

In OPC DA, addressing is done by the tag name (Item ID).

![OPC DA Binding setup](images/)

### 2.1 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name in the project tree. |
| **Title** | Human-readable description. |
| **Tag** | Internal Faceplate system tag where the value is mapped. |
| **Access** | **R** — Read, **W** — Write, **RW** — Read/Write. |
| **Transformation** | *Optional.* Mathematical processing of the raw value. |

### 2.2 Addressing (OPC Tag)

| Field | How to fill |
| :--- | :--- |
| **OPC tag** | **Item ID.** Full path to the tag in the OPC server address space.<br>*Examples:*<br>• `Channel1.Device1.Tag1`<br>• `Simulation.Ramp`<br>• `Bucket Brigade.Int4` |

---
<!-- 
## Additional notes

1. **ProgID (ServerID):** Ensure there are no typos. If the server is local, available ProgIDs can be listed using tools like *OPC Explorer* or *Matrikon OPC Explorer*.
2. **DCOM hell:** If `IP` is remote and the state is `Error`, 99% of the time it is a Windows permissions issue.
   - Create a user on both machines with the same username/password.
   - Run Faceplate services under that user.
   - Configure DCOM (`dcomcnfg`) on the server and allow remote access.
3. **Tag syntax:** Item ID may be case-sensitive depending on the server. Copy the exact tag path from an OPC client to avoid typos.
4. **Quality:** If the connection is OK (`State: RUN`) but the tag value is “bad” or `0`, check the tag quality on the OPC server. The OPC server may not see the PLC. -->
