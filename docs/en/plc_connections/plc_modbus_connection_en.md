# Modbus (TCP/RTU) Configuration Guide

## Overview
**Modbus** is a de‑facto standard in industrial automation. In **Faceplate**, a universal driver is implemented that supports three operating modes, allowing polling of both modern controllers and legacy equipment/sensors via gateways.

Supported modes (`Type`):
1. **tcp:** Classic Modbus TCP (Ethernet).
2. **rtu-serial:** Modbus RTU via a physical COM port (RS‑485/232).
3. **rtu-tcp:** Modbus RTU encapsulated into a TCP packet (Modbus‑over‑TCP). Used with transparent gateways (Moxa, HF, etc.).

Configuration consists of two stages:
1. **Connection (`plc_modbus_connection`):** Transport setup.
2. **Binding (`plc_modbus_binding`):** Register addressing.

---

## STEP 1. Connection setup (Connection)

At this stage you select the physical transport.

### 1.1 Select transport type
First, choose the connection type in the **Type** field.

![Modbus transport type](images/modbus_type.png)

### 1.2 Base settings (common for all types)

| Parameter | Description / Recommendations |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Polling interval (default `1000`). <br>*Tip:* for Serial use >100–200 ms. TCP can be faster. |
| **Shutdown timeout** | Socket shutdown timeout (`60000`). |
| **Support for group requests** | **Yes** — enable grouped register reads (optimization). The driver reads consecutive addresses using a single request. |
| **Max. package length** | PDU length limit. If a gateway has a small buffer, reduce this value (default 250). |

---

### 1.3 Physical layer setup

#### Option A: `tcp` mode (Ethernet)
Used to communicate with PLCs or I/O modules that have Ethernet and support Modbus TCP.

![Modbus TCP settings](images/tcp.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | Device IP address (e.g., `192.168.1.10`). |
| **Port** | Standard Modbus TCP port is **502**. |
| **Timeout** | Server response timeout (ms). |
| **Attempts** | Number of retries before a communication error is reported. |

#### Option B: `rtu-serial` mode (RS‑485/232)
Used for direct connection of a daisy chain of devices to the server COM port.

![Modbus RTU Serial settings](images/rtu_serial.png)

| Field | Description |
| :--- | :--- |
| **Port** | Port path (Linux: `/dev/ttyUSB0`, Windows: `COM1`). |
| **Baud rate** | Speed. Must strictly match on all devices on the line (9600, 19200, etc.). |
| **Parity** | Parity (`no`, `even`, `odd`). |
| **Stop bits / Data bits** | Usually `1` and `8`. |
| **Line Delay Ratio** | Line delay coefficient. Increase if the line is long/noisy. |

> **Note:** `rtu-tcp` is configured similarly to TCP (requires IP and Port), but the internal frame format is RTU (with CRC checksum).

---

## STEP 2. Variable setup (Binding)

Here you bind a specific Modbus register to a system tag.

![Modbus binding setup](images/bindings.png)

### 2.1 Addressing

| Field | Description |
| :--- | :--- |
| **Slave address** | Device address (Unit ID). In TCP usually `1` (or `255`), in Serial — from `1` to `247`. |
| **Memory area** | Modbus memory type:<br>• **HR** (Holding Registers) — 4xxxx, read/write.<br>• **IR** (Input Registers) — 3xxxx, read only.<br>• **CS** (Coils) — 0xxxx, bits read/write.<br>• **IS** (Discrete Inputs) — 1xxxx, bits read only. |
| **Address** | Register address offset. <br>⚠️ *Attention:* In some maps indexing starts at 1, while drivers typically use 0. If data is shifted, try +/- 1. |
| **Read / Write** | Modbus function codes. Usually auto‑selected based on Memory Area (e.g., Read `03`, Write `10` or `06`). |

### 2.2 Data handling

| Field | Description |
| :--- | :--- |
| **The size** | Data size (Word = 16‑bit, DWord = 32‑bit, etc.). |
| **Format** | Interpretation: `signed-integer`, `unsigned`, `float`. |
| **Byte order** | **Byte order / endianness.** Critical setting.<br>• `21` — Big Endian (default).<br>• `12` — Little Endian.<br>• `2143` / `3412` — swap variants for 32‑bit values. Use experimentally if numbers are wrong. |
| **Check CRC** | Force checksum verification (usually `Yes`). |

---

<!-- ## Additional notes

1. **Address shift:** The most common Modbus issue. If you expect value at register `100` but see `0`, try `99` or `101`.
2. **Byte order (Endianness):** If instead of `25.0` you see a huge number or `0.0004`, change **Byte order**.
3. **Timeouts:** For RTU Serial always keep a safe margin (min 100–200 ms) because RS‑485 is half‑duplex.
4. **IP vs Slave Address:** For `rtu-tcp` gateways, ensure **Slave Address** is the RS‑485 device address behind the gateway, not the gateway IP. -->
