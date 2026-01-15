# Ethernet/IP (Rockwell Automation) Driver Configuration

## Overview
**EtherNet/IP** (Industrial Protocol) is an industrial standard that uses the **Common Industrial Protocol (CIP)** over standard Ethernet.
In **Faceplate**, this driver is used for native integration with **Allen‑Bradley (Rockwell Automation)** controllers and compatible devices.

### Supported equipment
According to the driver configuration, the following controller families are supported:
- **ControlLogix / CompactLogix** (Tag-based addressing, CIP)
- **Micro800** (Micro820/850/870)
- **MicroLogix** (PCCC addressing)
- **SLC 500** (Legacy, PCCC)
- **PLC‑5** (Legacy, PCCC)
- **LogixPCCC** (Specific mode for Logix via PCCC)

---

## STEP 1. Connection setup (`plc_ethernet_ip_connection`)

At this stage you create a communication session with the controller.

![Ethernet/IP connection setup](images/eip_connection.png)

### 1.1 General settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique system connection name (e.g., `cip_line1_main`). |
| **Period (ms)** | Polling interval. <br>*Recommendation:* typically 100–500 ms for EtherNet/IP. CIP is fast, but avoid overloading EN2T modules. |
| **Shutdown timeout** | Time to wait for a graceful TCP session close (CIP Forward Close). |
| **Master connection** | Used for redundancy configuration. Reference to the main channel. |
| **Support for group requests** | **Yes** — enable optimization (Multi‑Request packets). The driver will pack multiple reads into one Ethernet frame. |

### 1.2 Controller settings

This section is critical: it defines the addressing method.

![Controller types](images/plc_type.png)

| Field | Description / Notes |
| :--- | :--- |
| **Controller type** | Select PLC family:<br>• **ControlLogix:** Uses symbolic tag names (most modern mode).<br>• **MicroLogix / SLC / PLC‑5:** Uses file-based addresses (N7:0, F8:1). |
| **IP** | IP address of the communication module or CPU. |
| **Routing** | *Optional.* CIP path for reaching the CPU if Ethernet is not in the same slot, or if the CPU is in another chassis.<br>*Format:* sequence of `Port,Address` pairs.<br>*Example:* `1,0` (Backplane, Slot 0). Leave empty for CompactLogix (no chassis routing). |

---

## STEP 2. Tag binding setup (`plc_ethernet_ip_binding`)

With EtherNet/IP (especially ControlLogix), addressing is done by **tag name**, not by raw memory address.

![Tag binding setup](images/eip_bindings.png)

### 2.1 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding object name in the system tree. |
| **Tag** | Faceplate system tag where the value will be written. |
| **Access** | **R** (Read only), **W** (Write only), **RW**. |
| **Transformation** | Raw data transformation (scaling, bit inversion, etc.). |

### 2.2 Target data addressing

| Field | How to fill |
| :--- | :--- |
| **Controller tag name** | **Symbolic address in the PLC.**<br>• For **ControlLogix:** Tag name as in Studio 5000. Example: `MyTag`, `Program:MainProg.Step`.<br>• For **SLC/MicroLogix:** Element address, e.g., `N7:0`, `F8:10`, `B3:0/5`. |
| **Data type** | Expected data type (DINT, REAL, BOOL, STRING). Must match the type defined in the PLC. |

---
<!-- 
## 💡 Additional notes

1. **CIP Path (Routing):** The most common issue with ControlLogix chassis. If the Ethernet module is in slot 1 but the CPU is in slot 0, IP alone is not enough — you must set the backplane path to the CPU.
2. **Tag syntax:** ControlLogix tags can be *Controller Scoped* (global) or *Program Scoped* (local).
   - Global: `TagName`
   - Local: `Program:ProgramName.TagName`
3. **Strings:** Allen‑Bradley strings have a specific structure (length + data). Ensure `Data type` is correct so the driver can unpack the structure.
4. **Legacy PLCs (SLC/PLC‑5):** They do not benefit from `Support for group requests` as much as newer controllers. If you see communication issues, try disabling this option. -->
