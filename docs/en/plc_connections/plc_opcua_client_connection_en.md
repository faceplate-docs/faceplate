# OPC UA Client Configuration Guide

## Overview
**OPC UA (Unified Architecture)** is a modern cross‑platform industrial communication standard (IEC 62541). Unlike classic OPC DA, it does not depend on Windows/DCOM, supports encryption, and works with complex data structures.

The **OPC UA Client** driver in **Faceplate** can connect to OPC UA servers (Siemens S7‑1500, Kepware, Prosys, B&R, etc.) using the binary `opc.tcp` protocol.

Configuration consists of two stages:
1. **Connection (`plc_opcua_client_connection`):** Endpoint, security, and authentication setup.
2. **Binding (`plc_opcua_client_binding`):** Subscribing to specific nodes.

---

## STEP 1. Connection setup (Connection)

Here you establish a secure channel to the server.

### 1.1 Diagnostic panel (Runtime)
*Top part of the window used to monitor the session.*

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — client stopped.<br>**RUN** (Green) — session is activated. |
| **Error** | Error text. <br>*Common:* `BadCertificateUntrusted` (certificate not trusted by server), `BadTimeout`. |
| **Actual connection** | Current active channel (when redundancy is used). |

### 1.2 Configuration settings (Settings)

![OPC UA connection setup](images/opcua_client.png)

#### Base settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Publishing Interval. The rate at which the client requests subscription updates from the server. |
| **Support for group requests** | **Yes** — enable grouping nodes into subscriptions (recommended). |
| **Master connection** | Reference to the main connection (for redundancy). |

#### Connection & Security (critical section)

| Field | Description / Notes |
| :--- | :--- |
| **URL** | **Endpoint URL.** Server address.<br>*Format:* `opc.tcp://<IP-address>:<Port>`<br>*Example:* `opc.tcp://192.168.0.10:4840` |
| **MaxNodesPerBrowse** | Maximum number of nodes returned when browsing the address space. Default: `1000`. |
| **Timeout** | Server response timeout (ms). |
| **Secure connection** | **Encryption mode.**<br>• **No:** `None` (no security), suitable for tests.<br>• **Yes:** `Sign` or `SignAndEncrypt` (requires certificates). |
| **Certificate / Key** | Paths to the client public certificate (`.der`) and private key (`.pem`). |
| **Generate a certificate** | Button to auto‑generate a self‑signed client certificate. |
| **Login / Password** | **User authentication.**<br>• Empty — **Anonymous** token.<br>• Filled — **User/Password** token. |

---

## STEP 2. Variable setup (Binding)

In OPC UA, addressing is done via **NodeId**.

![OPC UA client binding setup](images/opcua_client_bindings.png)

### 2.1 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name in the project tree. |
| **Tag** | Faceplate system tag where the value will be mapped. |
| **Access** | **R** — Read (Subscription / Monitored Item).<br>**W** — Write (Write Attribute). |
| **Transformation** | *Optional.* Value transformation (e.g., scaling). |

### 2.2 Node addressing (OPC UA Node)

| Field | How to fill |
| :--- | :--- |
| **OPC tag** | **NodeId (node address).** A unique variable address on the server. Includes namespace index (ns) and identifier type (s, i, g, b).<br>*Examples:*<br>• `ns=2;s=Machine1.Sensor.Temp` (string ID)<br>• `ns=3;i=1005` (numeric ID)<br>• `i=2258` (standard node, ns=0) |
| **Type** | OPC UA data type (Int32, Float, Boolean, String, etc.). Usually auto-detected, but can be set explicitly. |

---

<!-- ## Additional notes

OPC UA is the most secure protocol, and security is the most common source of first‑run issues.

1. **Certificate trust:**
   - Even with `Secure connection: No` (None), some servers still require the client certificate to be trusted.
   - *Symptom:* `BadSecurityChecksFailed` or `BadCertificateUntrusted`.
   - *Fix:* Open the OPC server configuration (PLC or SCADA side), locate **Rejected Certificates**, find the Faceplate certificate and move it to **Trusted**.
2. **Endpoint URL:**
   - Many servers expose multiple endpoints (different security policies). Ensure your URL matches what the server is listening on.
3. **Clock synchronization:**
   - Certificates have validity periods. If server and client clocks differ by more than a few minutes, the connection can be rejected.
4. **NodeId syntax:**
   - NodeIds are case‑ and whitespace‑sensitive. `ns=2;s=MyTag` and `ns=2;s=Mytag` are different nodes. Prefer selecting tags using Browse to avoid typos. -->
