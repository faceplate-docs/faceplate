# 📘 M-Bus (Meter-Bus) Driver Configuration Guide

## General Description
**M-Bus (Meter-Bus)** is a specialized European standard (EN 13757) for remote reading of utility meters: heat meters, water meters, gas meters, and electricity meters.

In the **Faceplate** system, the M-Bus driver is hybrid and supports two physical layers:
1.  **Serial (COM):** Direct connection to the server via a Master Level Converter (M-Bus <-> RS-232/485).
2.  **TCP (Ethernet):** Connection via remote gateways (Ethernet-to-MBus) or transparent converters.

The configuration architecture consists of two steps:
1.  **Connection (`plc_mbus_connection`):** Configuring the transport to the bus.
2.  **Binding (`plc_mbus_binding`):** Configuring the polling of a specific variable within a device.

---

## STEP 1. Connection Configuration

At this stage, we configure the Master device that polls the bus.

### 1.1 Diagnostics and Control (Runtime)
*Panel for real-time driver status monitoring.*

![M-Bus Diagnostics](images/mbus3.png)

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — Polling is stopped.<br>**RUN** (Green) — Driver is running. |
| **Error** | Text of the last error (e.g., `Timeout` or `Checksum error`). |
| **Actual connection** | Indicates which channel is active (Master or Backup) when redundancy is used. |

### 1.2 General Settings

| Parameter | System Analyst Recommendations |
| :--- | :--- |
| **Name** | Unique connection name in the system. |
| **Period (ms)** | Bus polling period. <br>⚠️ **Important:** M-Bus is a slow protocol (usually 2400 baud). Do not set the period to less than **60000 ms** (1 minute), especially if devices are battery-powered, to avoid premature battery depletion. |
| **Type** | Mode selector: `serial` or `tcp`. |

---

### 1.3 Physical Layer Configuration (Depending on Type)

#### Option A: `serial` Mode (Direct Connection)
Used if the M-Bus hardware converter is connected directly to the server's COM port.

![Serial M-Bus Settings](images/mbus2.png)

| Field | Description |
| :--- | :--- |
| **Port** | System port name (Linux: `/dev/ttyUSB0`, Win: `COM1`). |
| **Baud rate** | Exchange speed. <br>*Standard:* Usually **2400** (rarely 9600). Must match the device settings. |
| **Parity** | Parity. <br>*Standard:* Usually **Even**. The screenshot shows `no`, but most heat meters require `Even`. |
| **Data / Stop bits** | Usually 8 data bits and 1 stop bit. |
| **Timeout** | Response wait time. For M-Bus, it is better to set this with a margin (3000-5000 ms). |

#### Option B: `tcp` Mode (Network Gateway)
Used if the M-Bus loop is remote and connected via an Ethernet converter.

![TCP M-Bus Settings](images/mbus1.png)

| Field | Description |
| :--- | :--- |
| **IP/Hostname** | Gateway IP address. |
| **Port** | TCP port (often `502`, `1001`, or `8000` — check gateway documentation). |
| **Timeout** | Account for network latency plus the slowness of the bus itself. |

> **Action:** After configuration, click **Save**, then double-click the created connection to add bindings.

---

## STEP 2. Variable Configuration (Binding)

The peculiarity of M-Bus is that the device returns **all** information in one large packet. The Binding task is to "extract" the necessary value from this packet.

![M-Bus Variable Settings](images/mbus4.png)

### 2.1 Binding Parameters

| Field | Description |
| :--- | :--- |
| **Name** | Name of the binding object. |
| **Tag** | The system tag where the value will be written. |
| **Access** | **R** — Read Only (M-Bus is primarily a readout protocol).<br>**W** — Write (Rarely used in M-Bus). |
| **Address** | **Primary Address.** An integer from 1 to 250. The unique address of the meter on the bus. |
| **Telegram** | Telegram number. For most simple devices = `0`. (Used if data does not fit into a single packet). |
| **Index** | **Data Index in the packet.** The most complex parameter. <br>This is the ordinal number of the variable in the M-Bus response structure. <br>*Example:* If the meter sends a sequence: [Time, Energy, Flow, Temperature], then to get Energy, Index = `1` (or `0`, depending on driver implementation; start with 0). |

---

## 💡 Troubleshooting Tips

1.  **Physical Layer (90% of issues):**
    * Standard settings for most meters (Danfoss, Kamstrup, Techem): **2400 baud, 8E1 (Even Parity)**.
    * Ensure the settings in the `Serial` section match this standard. The screenshots show `9600 8N1` — this often works for Modbus but rarely for M-Bus.
2.  **Finding the Index:**
    * The driver does not see variable names from the packet ("Energy", "Volume"); it only sees a data stream.
    * *Tip:* Use a third-party utility (e.g., M-Bus Sheet or gateway manufacturer software) to read the entire packet, see the position of the desired parameter, and enter that number in the `Index` field.
3.  **Address Collisions:**
    * A common problem in M-Bus is two devices with the factory address `0` or `1` on the same bus. Connect devices one by one and change their addresses before assembling the full loop.