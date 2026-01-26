# OPC UA Client Configuration Guide

## General Description
**OPC UA (Unified Architecture)** is a modern cross-platform industrial communication standard (IEC 62541). Unlike classic OPC DA, it does not depend on Windows/DCOM, and it supports encryption and complex data structures.

The **OPC UA Client** driver in the **Faceplate** system allows connecting to servers (Siemens S7-1500 PLC, Kepware, Prosys, B&R, etc.) via the binary protocol `opc.tcp`.

The configuration process consists of two stages:
1.  **Connection (`plc_opcua_client_connection`):** Configuring the Endpoint, security, and authentication.
2.  **Binding (`plc_opcua_client_binding`):** Subscribing to specific Nodes.

---

## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)
Here we create a secure communication channel with the server.

![OPC UA connection settings](images/opcua_client.png)

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


### 1.3 Protocol Parameters (OPC UA client)
The most important part of OPC UA configuration.

| Field | Description and Analytics |
| :--- | :--- |
| **URL** | **Endpoint URL.** Server address.<br>*Format:* `opc.tcp://<IP-address>:<Port>`<br>*Example:* `opc.tcp://192.168.0.10:4840` |
| **MaxNodesPerBrowse** | Limit on the number of nodes when browsing the address tree (Browse). Standard: `1000`. |
| **Timeout** | Time to wait for a response from the server (ms). |
| **Secure connection** | **Encryption mode.**<br>• **No (Off):** Mode `None` (no security). Suitable for tests.<br>• **Yes (On):** Use `Sign` or `SignAndEncrypt`. Requires certificates. |
| **Certificate / Key** | Paths to the client's public certificate (`.der`) and private key (`.pem`) files. |
| **Generate a certificate** | Button for automatic generation of a self-signed client certificate. |
| **Login / Password** | **User Authentication.**<br>• If empty — **Anonymous** is used.<br>• If filled — **User/Password** token is used. |

---

## 2. Variable Configuration (Binding)

In OPC UA, addressing is performed via **NodeId** (Node Identifier).

![OPC UA binding settings](images/opcua_client_bindings.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)
> 
### 2.1 Binding Parameters
| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | **R** (Read), **W** (Write), **RW** (Read/Write). |

### 2.2 Node Addressing (OPC UA Node)



| Field | Instruction |
| :--- | :--- |
| **OPC tag** | **NodeId (Node Address).**<br>Unique address of the variable on the server. Consists of a namespace index (ns) and an identifier (s, i, g, b).<br>*Examples:*<br>• `ns=2;s=Machine1.Sensor.Temp` (String ID)<br>• `ns=3;i=1005` (Numeric ID)<br>• `i=2258` (Standard node, ns=0) |
| **Type** | OPC UA data type (Int32, Float, Boolean, String, etc.). Usually detected automatically, but can be set rigidly. |

> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)

---