
# 📘 Modbus (TCP/RTU) Configuration Guide

## General Description
**Modbus** is the *de facto* standard for industrial automation. The **Faceplate** system implements a universal driver that supports three modes of operation, allowing for the polling of modern controllers as well as legacy equipment or sensors via gateways.

Supported Modes (`Type`):
1.  **tcp:** Classic Modbus TCP (Ethernet).
2.  **rtu-serial:** Modbus RTU via a physical COM port (RS-485/232).
3.  **rtu-tcp:** Modbus RTU encapsulated in a TCP packet (Modbus-over-TCP). Used for working with transparent gateways (Moxa, HF, etc.).

The configuration process consists of two stages:
1.  **Connection (`plc_modbus_connection`):** Transport configuration.
2.  **Binding (`plc_modbus_binding`):** Register addressing.

---

## STEP 1. Connection Configuration

At this stage, we define the physical communication layer.

### 1.1 Transport Type Selection
First, define the connection type in the **Type** field.

![Modbus Type Selection](images/modbus_type.png)

### 1.2 Basic Settings (Common for all types)

| Parameter | Description and Recommendations |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Polling period (default `1000`). <br>*Tip:* For Serial, set to >100-200 ms. For TCP, faster rates are possible. |
| **Shutdown timeout** | Socket closure wait time (`60000`). |
| **Support for group requests** | **Yes** — enable group register reading (optimization). The driver will read consecutive addresses in a single request. |
| **Max. package length** | PDU length limit. If the gateway has a small buffer, decrease this value (standard is 250). |

---

### 1.3 Physical Layer Configuration

#### Option A: `tcp` Mode (Ethernet)
Used for communication with PLCs or I/O modules that have an Ethernet port and support the Modbus TCP stack.

![Modbus TCP Settings](images/tcp.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | Device IP address (e.g., `192.168.1.10`). |
| **Port** | Standard Modbus TCP port — **502**. |
| **Timeout** | Server response wait time (in ms). |
| **Attempts** | Number of retries before a communication error is flagged. |

#### Option B: `rtu-serial` Mode (RS-485/232)
Used for direct connection of a daisy-chain of devices to the server's COM port.

![Modbus RTU Serial Settings](images/rtu_serial.png)

| Field | Description |
| :--- | :--- |
| **Port** | Path to the port (Linux: `/dev/ttyUSB0`, Windows: `COM1`). |
| **Baud rate** | Speed. Must strictly match on all devices in the line (9600, 19200, etc.). |
| **Parity** | Parity (`no`, `even`, `odd`). |
| **Stop bits / Data bits** | Usually `1` and `8`. |
| **Line Delay Ratio** | Line delay coefficient. Increase if the line is long and "noisy". |

> **Note:** The **rtu-tcp** mode is configured similarly to the TCP mode (requires IP and Port), but the internal packet structure follows RTU standards (including CRC checksum).

---

## STEP 2. Variable Configuration (Binding)

Here we bind a specific Modbus register to a system tag.

![Modbus Binding Settings](images/bindings.png)

### 2.1 Addressing

| Field | Description |
| :--- | :--- |
| **Slave address** | Device address (Unit ID). In TCP this is usually `1` (or `255`), in Serial — from `1` to `247`. |
| **Memory area** | Modbus memory type:<br>• **HR** (Holding Registers) — 4xxxx, Read/Write.<br>• **IR** (Input Registers) — 3xxxx, Read Only.<br>• **CS** (Coils) — 0xxxx, Bits Read/Write.<br>• **IS** (Discrete Inputs) — 1xxxx, Bits Read Only. |
| **Address** | Register address offset. <br>*Attention:* In some address maps, numbering starts at 1, whereas the driver typically uses 0-based indexing. If data is "shifted", try +/- 1. |
| **Read / Write** | Modbus function codes. Usually set automatically when the Memory Area is selected (e.g., Read `03`, Write `10` or `06`). |

### 2.2 Data Handling

| Field | Description |
| :--- | :--- |
| **The size** | Data size (Word = 16 bits, DWord = 32 bits, etc.). |
| **Format** | Data interpretation: `signed-integer`, `unsigned`, `float`. |
| **Byte order** | **Endianness.** A critically important setting.<br>• `21` — Big Endian (Standard).<br>• `12` — Little Endian.<br>• `2143` / `3412` — Various Swap options for 32-bit numbers. Determined experimentally if the number is displayed incorrectly. |
| **Check CRC** | Forced checksum validation (usually `Yes`). |

---

## 💡 System Analyst's Checklist

1.  **Address Shift:** The most common Modbus issue. If you expect a value in register `100` but see `0`, try address `99` or `101`.
2.  **Byte Order (Endianness):** If instead of a temperature of `25.0` you see a huge number or `0.0004`, change the **Byte order** setting.
3.  **Timeouts:** For RTU Serial, always set timeouts with a margin (minimum 100-200 ms), as RS-485 is a half-duplex interface.
4.  **IP Addressing:** When using `rtu-tcp` (gateways), ensure the **Slave Address** matches the device address ON THE RS-485 BUS behind the gateway, not the IP address of the gateway itself.