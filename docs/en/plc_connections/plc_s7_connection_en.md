# S7 (ISO-on-TCP) Configuration Guide

## General Description
The **S7** driver is designed for native data exchange with **Simatic S7** family programmable logic controllers (PLC) from Siemens.

Supported series:
* **S7-300 / S7-400** (Classic architecture).
* **S7-1200 / S7-1500** (Modern series, require access configuration, see Troubleshooting section).
* **Siemens Logo!** (starting from versions 0BA7/0BA8).

Data exchange occurs via the **ISO-on-TCP** protocol (RFC 1006) through standard port **102**.

The configuration process consists of two stages:
1.  **Connection (`plc_s7_connection`):** Configuring network access to the CPU.
2.  **Binding (`plc_s7_binding`):** Addressing a specific memory cell.

---


## 1. Connection Configuration (Connection)
> Create PLC connection → [Steps to create a PLC connection](./general_ru.md#создание-plc-соединения)
At this stage, we configure connection parameters to the communication processor or Ethernet port on the CPU.

![S7 connection settings](images/s7_conn.png)

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

### 1.3 Protocol Parameters (S7)

![S7 data type settings](images/s7_data_type.png)



| Field | Description and Analytics |
| :--- | :--- |
| **Data type** | Controller type (family). <br>Affects packet formation algorithms. Select `300` (S7-300/400), `1200` (S7-1200)/`1500`(S7-1500), or LOGO.|
| **IP/Hostname** | Controller IP address. |
| **Port** | **102** (Standard Siemens ISO-on-TCP port). |
| **Rack** | **Rack number (chassis).** <br>• For S7-300/400/1500: Usually `0`. |
| **Slot** | **CPU Slot number.** (Field might be below Rack).<br>⚠️ **This is a critical parameter:**<br>• **S7-300:** Always `2`.<br>• **S7-400:** Depends on Hardware configuration (often `2` or `3`).<br>• **S7-1200 / S7-1500:** Usually `1` (or `0` for old firmware 1200). |

---

## 2. Variable Configuration (Binding)

In S7, memory has a rigid structure. To access a variable, you need to know its area, type, and offset (address).

![S7 binding settings](images/s7_bind.png)
> Create PLC binding → [Steps to create a PLC binding](./general_ru.md#создание-plc-привязки)

### 2.1 Binding Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding. |
| **Title** | Title (description) for this object. |
| **Tag** | Faceplate system tag. The incoming value will be written to the selected field of the selected object. See [Binding to a tag](./general_ru.md#привязка-к-тегу-на-примере-архива) |
| **State** | **STOP** — binding is stopped.<br>**RUN** — binding is running. |
| **Transformation** | Value transformation. See [Transformation](./transformation_ru.md). |
| **Access** | **R** (Read), **W** (Write), **RW** (Read/Write). |

### 2.2 Memory Addressing (S7 Address)

For addressing like `DB1.DBX10.2` (Bit 2 in byte 10 of data block 1), the settings will look like this:



| Field | Instruction |
| :--- | :--- |
| **Memory area** | Memory area:<br>• **DB** — Data Block (Data blocks, main area).<br>• **I** (Inputs) — Inputs.<br>• **Q** (Outputs) — Outputs.<br>• **M** (Flags/Merkers) — Flag memory. |
| **Type** | Variable data type:<br>• `bit` (BOOL)<br>• `byte`, `word`, `dword`<br>• `int`, `real` (float) |
| **DB** | **Data Block Number.** Filled only if `Memory area` = **DB**. (E.g., `1`). |
| **Byte** | **Byte Offset.** The starting byte of the variable. |
| **Bit** | **Bit Offset.** From `0` to `7`. <br>Filled **only** if `Type` = `bit`. For other types, it must be `0`. |
| **Format** | Data interpretation (e.g., `integer` for signed numbers or `float` for real numbers). |

> Error in PLC binding -> [binding error](./general_ru.md#ошибка-в-привязке)
---