# M-Bus (Meter-Bus) Driver Configuration Guide

## General Description
**M-Bus (Meter-Bus)** is a specialized European standard (EN 13757) for remote data reading from utility meters: heat meters, water meters, gas meters, and electricity meters.

In the **Faceplate** system, the M-Bus driver is hybrid and supports two physical layers:
1.  **Serial (COM):** Direct connection to the server via a Master level converter (M-Bus <-> RS-232/485).
2.  **TCP (Ethernet):** Connection via remote gateways (Ethernet-to-MBus) or transparent converters.

The configuration architecture consists of two steps:
1.  **Connection (`plc_mbus_connection`):** Configuring the transport to the bus.
2.  **Binding (`plc_mbus_binding`):** Configuring the polling of a specific variable within the device.

---

## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)

At this stage, we configure the master device that polls the bus.

### 1.1 Diagnostics Panel
The upper part of the window displays the driver status.
> PLC connection diagnostics → [Diagnostics](./general_ru.md#диагностика-diagnostics)


| Field | Description |
| :--- | :--- |
| **State** | **STOP** — driver is stopped.<br>**RUN** — driver is running. |
| **Node** | Cluster node. Indicates on which node the process is running. |
| **PID** | Process ID. |
| **Error** | Error text. |
| **Disabled** | |
| **Memory limit (bytes)** | Memory limit (RAM limits (MB) for the process serving the connection). Memory capacity determines the number of variables (tags) that can be processed during the connection operation. |
| **Actual connection** | Current active communication channel. In systems with Redundancy, indicates exactly which connection (primary or backup) is currently exchanging data. |
| **Master connection** | Link to the main communication channel. Filled for redundant connections. The field indicates which connection is the priority (Master), defining the logical pair for the redundancy mechanism. |

### 1.2 General Settings (Settings)

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique name of the connection. |
| **Title** | Title (description) of this object. |
| **Period (ms)** | Base driver processing cycle. |
| **Shutdown timeout (ms)** | Waiting time for correct connection termination. |
| **Support for group requests** | **Yes** — enable the possibility of periodic General Interrogation. |
| **Max. package length** | Maximum APDU size. Standard is 250 bytes. |
| **Line Delay Ratio** | Delay coefficient for slow communication lines. |


### 1.3 Protocol Parameters (MBUS)

#### 1.3.1 `serial` Mode (Direct connection)
Used if the M-Bus hardware converter is connected directly to the server's COM port.

![Serial M-Bus settings](images/mbus2.png)

| Field | Description |
| :--- | :--- |
| **Port** | System port name (Linux: `/dev/ttyUSB0`, Win: `COM1`). |
| **Baud rate** | Exchange speed. <br>*Standard:* Usually **2400** (less often 9600). Must match the device settings. |
| **Parity** | Parity. <br>*Standard:* Usually **Even**. The screenshot shows `no`, but most heat meters require `Even`. |
| **Data / Stop bits** | Usually 8 data bits and 1 stop bit. |
| **Timeout** | Response waiting time. For M-Bus, it is better to set it with a margin (3000-5000 ms). |
| **attempts** | Number of request attempts. Determines the maximum number of retries to send a request to the device in the absence of a response. |

#### 1.3.2 `tcp` Mode (Network Gateway)
Used if the M-Bus is located remotely and connected via an Ethernet converter.

![TCP M-Bus settings](images/mbus1.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | Gateway IP address. |
| **Port** | TCP port (often `502`, `1001`, or `8000` — see gateway documentation). |
| **Timeout** | Consider network delays + the slowness of the bus itself. |
| **attempts** | Number of request attempts. Determines the maximum number of retries to send a request to the device in the absence of a response. |

---

## 2. Variable Configuration (Binding)

The peculiarity of M-Bus is that the device provides **all** information in one large packet. The Binding task is to "extract" the necessary value from this packet.

![M-Bus variable settings](images/mbus4.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)

### 2.1 Binding Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | **R** — Read Only.<br>**W** — Write (Rarely used in M-Bus).<br>**RW** — Read/Write. |
| **Address** | **Primary Address.** A number from 1 to 250. Unique meter address on the bus. |
| **Telegram** | Telegram number. For most simple devices = `0`. (Used if data does not fit into one packet). |
| **Index** | **Data index in the packet.** The most complex parameter. <br>This is the ordinal number of the variable in the M-Bus response structure. <br>*Example:* If the meter sends the sequence: [Time, Energy, Flow, Temperature], then to get Energy Index = `1` (or `0`, depends on driver implementation, start with 0). |


> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)
---