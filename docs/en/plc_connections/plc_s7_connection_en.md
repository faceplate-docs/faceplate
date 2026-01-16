#  S7 PLC Protocol (ISO‑on‑TCP) Configuration Guide

## Overview
The **S7** driver is intended for native data exchange with Siemens **Simatic S7** PLCs.

Supported series:
- **S7‑300 / S7‑400** (classic architecture)
- **S7‑1200 / S7‑1500** (modern series; require access configuration — see Troubleshooting)
- **Siemens Logo!** (starting from 0BA7/0BA8)

Communication is based on **ISO‑on‑TCP** (RFC 1006) using the standard port **102**.

Configuration consists of two stages:
1. **Connection (`plc_s7_connection`):** Network access to the CPU.
2. **Binding (`plc_s7_binding`):** Specific memory cell addressing.

---

## STEP 1. Connection setup (Connection)

Here you configure connection parameters to the communication processor or the Ethernet port on the CPU.

### 1.1 Diagnostic panel (Runtime)
*Top part of the window. Used for state monitoring.*

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — driver stopped.<br>**RUN** (Green) — connection established (Handshake successful). |
| **Error** | Error text. <br>*Common:* `Connection refused` (no network / wrong port), `Iso packet error` (wrong Rack/Slot). |
| **Actual connection** | Current active channel (when redundancy is used). |

### 1.2 Configuration settings (Settings)

![S7 connection setup](images/s7_conn.png)

#### Main and timing settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique connection name. |
| **Period (ms)** | Polling interval. Default `1000`. S7comm is quite fast; for critical signals you can set `100–200` ms. |
| **Master connection** | Reference to the main connection (for redundancy). |
| **Support for group requests** | **Yes** — the driver will combine requests to adjacent bytes into one PDU (optimization). |
| **Max. package length** | PDU size. Typically `240` or `480` bytes for older series, `960` for newer series. |

#### Controller settings (S7 / TCP)

| Field | Description / Notes |
| :--- | :--- |
| **Data type** | Controller family. Affects packet build logic. Choose `300` (S7‑300/400/VIPA) or `1200`/`1500` if available. |
| **IP/Hostname** | PLC IP address/hostname. |
| **Port** | **102** (standard Siemens ISO‑on‑TCP port). |
| **Rack** | **Rack number.**<br>• For S7‑300/400/1500: usually `0`. |
| **Slot** | **CPU slot number.** This is critical:<br>• **S7‑300:** always `2`.<br>• **S7‑400:** depends on Hardware config (often `2` or `3`).<br>• **S7‑1200 / S7‑1500:** usually `1` (or `0` for older 1200 firmware). |

---

## STEP 2. Variable setup (Binding)

S7 memory has a strict structure. To access a variable you must know its area, type, and offset.

![S7 binding setup](images/s7_bind.png)

### 2.1 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name. |
| **Tag** | Faceplate system tag. |
| **Access** | **R** (Read), **W** (Write). |

### 2.2 Memory addressing (S7 Address)

For an address like `DB1.DBX10.2` (bit 2 at byte 10 in DB1), the settings look like:

| Field | How to fill |
| :--- | :--- |
| **Memory area** | Memory area:<br>• **DB** — Data Block (main area).<br>• **I** — Inputs.<br>• **Q** — Outputs.<br>• **M** — Flags/Merkers. |
| **Type** | Variable data type:<br>• `bit` (BOOL)<br>• `byte`, `word`, `dword`<br>• `int`, `real` (float) |
| **DB** | **Data Block number.** Only set if `Memory area` = **DB** (e.g., `1`). |
| **Byte** | **Byte offset.** Starting byte of the variable. |
| **Bit** | **Bit offset** from `0` to `7`. Only used when `Type` = `bit`. For other types it must be `0`. |
| **Format** | Data interpretation (e.g., `integer` for signed values or `float` for real values). |

---
<!-- 
## Additional notes (S7‑1200 / S7‑1500 access issues)

If you see `Permission denied` or no data:

1. **Optimized Block Access:**
   - Drivers of this type (S7comm) typically cannot work with “optimized blocks” (symbolic addressing).
   - *Fix:* In TIA Portal open DB properties and **disable** “Optimized block access”. Recompile and download to PLC.
2. **PUT/GET Access:**
   - In CPU settings (TIA Portal) under *Protection & Security -> Connection mechanisms*, enable:  
     **"Permit access with PUT/GET communication from remote partner"**.
3. **Rack/Slot:**
   - S7‑300: Rack=`0`, Slot=`2`.
   - S7‑1200: Rack=`0`, Slot=`1`. -->
