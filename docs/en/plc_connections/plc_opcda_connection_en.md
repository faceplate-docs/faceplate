# 📘 OPC DA (Classic) Configuration Guide

## General Description
**OPC DA (Data Access)** is a classic standard for data exchange in industrial automation, based on Microsoft DCOM technology. In the **Faceplate** system, this driver enables connections to any external OPC Servers (e.g., Kepware, Matrikon, Lectus) to read and write data.

> **Important:** Since OPC DA relies on DCOM, establishing a successful connection often requires configuring Windows user permissions and DCOM security settings on both sides (Client and Server).

The configuration process consists of two stages:
1.  **Connection (`plc_opcda_connection`):** Configuring the connection to the OPC Server.
2.  **Binding (`plc_opcda_binding`):** Subscribing to specific tags (Items).

---

## STEP 1. Connection Configuration

At this stage, we specify the location and the name of the OPC Server.

### 1.1 Diagnostics Panel (Runtime)
*The upper part of the window. Displays the connection status.*

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — Driver is stopped.<br>**RUN** (Green) — Connection to the server is established. |
| **Error** | Error text. Common errors: `Access Denied` (DCOM issues) or `Server not found`. |
| **Actual connection** | The currently active channel (when using redundancy). |

### 1.2 Configuration Parameters (Settings)

![OPC DA Connection Settings](images/opcda_conn.png)

#### General Settings
| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Data update interval (OPC Group Update Rate). |
| **Shutdown timeout** | Time allowed for graceful disconnection from the server. |
| **Master connection** | Reference to the main connection (for redundancy configuration). |
| **Support for group requests** | **Yes** — use the OPC Group mechanism for batch reading (recommended). |

#### Connection Parameters (TCP / DCOM)
Unlike other drivers, network settings here point to the host where the OPC Server is running.

| Field | Description |
| :--- | :--- |
| **IP/Hostname/Localhost** | Network address of the computer hosting the OPC Server.<br>*Example:* `192.168.1.5` or `localhost` (if the server is on the same machine). |
| **Port** | **8100** (or another port if tunneling is used). <br>*Note:* In classic OPC DA, the TCP port is not strictly defined (it operates via DCOM/RPC on port 135), but in this driver, this field may be used for specific OPC tunnels or internal proxies. |
| **ServerID** | **OPC Server ProgID.** This is the most critical field.<br>It uniquely identifies the server software component in the Windows Registry.<br>*Examples:* `Kepware.KEPServerEX.V6`, `Matrikon.OPC.Simulation.1`, `ICONICS.SimulatorOPCDA.2`. |

---

## STEP 2. Variable Configuration (Binding)

In OPC DA, addressing is done via the Tag Name (Item ID).

![OPC DA Binding Settings](images/opcda_bindings.png)

### 2.1 Binding Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding in the project tree. |
| **Title** | Human-readable description. |
| **Tag** | Internal Faceplate system tag where the value will be mapped. |
| **Access** | **R** — Read, **W** — Write, **RW** — Read/Write. |
| **Transformation** | *Optional.* Mathematical processing of the raw value. |

### 2.2 Addressing (OPC Tag)

| Field | Instruction |
| :--- | :--- |
| **OPC tag** | **Item ID.**<br>The full path to the tag in the OPC Server namespace.<br>*Examples:*<br>• `Channel1.Device1.Tag1`<br>• `Simulation.Ramp`<br>• `Bucket Brigade.Int4` |

---

## 💡 System Analyst's Checklist (Troubleshooting)

1.  **ProgID (ServerID):** Ensure the server name is entered correctly. If the server is installed locally, you can view the list of available ProgIDs using utilities like *OPC Explorer* or *Matrikon OPC Explorer*.
2.  **DCOM Hell:** If the `IP` is remote and the status is `Error`, 99% of the time the issue is Windows permissions.
    * Create a user with the exact same login and password on both machines.
    * Run the Faceplate services under this user.
    * Configure DCOM Config (`dcomcnfg`) on the server to allow remote access.
3.  **Tag Syntax:** Item IDs are often case-sensitive (depends on the server). Copy the tag path directly from an OPC client to avoid typos.
4.  **Quality:** If the link is valid (`State: RUN`), but the tag value is "bad" or `0`, check the tag quality on the OPC Server itself. The server might not be communicating with the underlying PLC.