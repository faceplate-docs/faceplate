# OPC UA Server Configuration Guide

## Overview
The **OPC UA Server** driver allows **Faceplate** to act as an OPC UA server. In other words, Faceplate publishes its internal tags to external networks, enabling third‑party clients (SCADA, MES, ERP, UaExpert) to connect and read/write data via the `opc.tcp` protocol.

Configuration consists of two stages:
1. **Connection (`plc_opcua_server_connection`):** Network endpoint/interface and server parameters.
2. **Binding (`plc_opcua_server_binding`):** Publishing specific tags into the server address space.

---

## STEP 1. Connection setup (Connection)

This stage defines on which port and interface the server will accept incoming connections.

![OPC UA Server connection setup](images/opcua_server_conn.png)

### 1.1 Diagnostic panel (Runtime)
The top part of the window shows the current server process state.

| Field | Description |
| :--- | :--- |
| **State** | Driver state. **STOP** — server stopped, port closed. **RUN** — server running and accepting connections. |
| **Node** | Cluster node name where the process is running. |
| **PID** | OS process ID. |
| **Disabled** | Switch to globally disable the server instance. |
| **Error** | Last error text (e.g., port is used by another application). |
| **Memory limit (bytes)** | RAM limit allocated to the server process. |

### 1.2 Configuration settings (Settings)

#### Main settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique system connection name. |
| **Title** | User-friendly connection description. |
| **Actual connection** | Informational field showing the active connection (relevant for redundancy). |
| **Master connection** | Reference to the main connection. Used only when setting up a backup server. |
| **Period (ms)** | Internal server processing loop. |
| **Shutdown timeout (ms)** | Time to wait for graceful shutdown of client sessions before forced stop. |

#### Protocol optimization

| Parameter | Description |
| :--- | :--- |
| **Support for group requests** | **Yes** — allow clients to use grouped subscriptions (Monitored Items). Recommended for performance. |
| **Max. package length** | Maximum data packet size (bytes). |
| **Line Delay Ratio** | Line delay coefficient (used for timeout calculations on slow networks). |

#### Network settings (TCP tab)

| Field | Description |
| :--- | :--- |
| **IP/Hostname/Localhost** | Interface IP to listen on.<br>• `127.0.0.1` — local access only.<br>• `0.0.0.0` — accessible for all external clients. |
| **Port** | TCP port for incoming connections. Default: **4841**. |
| **Timeout** | Network operation timeout (ms). |

> Note: **Users**, **Encryption** (Certificates), and **Limits** tabs are used to configure security policies.

---

## STEP 2. Variable publishing (Binding)

This stage defines the server **Address Space**. Each binding object creates a node visible to external clients.

![OPC UA Server bindings](images/opcua_server_bindings.png)

### 2.1 Runtime control

| Field | Description |
| :--- | :--- |
| **State** | Current state of the binding. |
| **Off** | Switch to temporarily hide the node from address space without deleting settings. |

### 2.2 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | System name of the binding object. |
| **Title** | Variable description. |
| **Tag** | **Source tag.** Faceplate internal tag whose value will be published. |
| **Transformation** | Optional data transformation (scaling, inversion) before sending to clients. |
| **Access** | Access level for external clients:<br>• **R** — Read-only (client can read, cannot modify).<br>• **RW** — Read/Write (client can control the tag). |
| **OPC tag** | **Node name (NodeId).** Name under which the variable is visible in the OPC UA server tree.<br>Example: `Sensor1` or `Area1.Temp`. |
| **Type** | OPC UA node data type (Double, Int32, Boolean, etc.). If not set, inherited from the source tag. |

---

<!-- ## Additional notes

1. **Firewall:** Ensure the TCP port (default 4841) is open for incoming connections on the server firewall.
2. **Endpoint URL:** Clients connect using `opc.tcp://<Server_IP>:4841`.
3. **Unique node names:** The **OPC tag** value must be unique within a single server instance.
4. **IP address:** For access from other machines, set IP to `0.0.0.0` or a specific NIC IP — not `127.0.0.1`. -->
