# 📘 EtherNet/IP Driver Configuration (Rockwell Automation)

## General Description
**EtherNet/IP** (Industrial Protocol) is an industrial standard utilizing the Common Industrial Protocol (CIP) over standard Ethernet.
In the **Faceplate** system, this driver is used for native integration with **Allen-Bradley (Rockwell Automation)** controllers and compatible devices.

### 🏭 Supported Equipment
According to the driver configuration, the following controller families are supported:
* **ControlLogix / CompactLogix** (Tag-based addressing, CIP)
* **Micro800** (Micro820/850/870 Series)
* **MicroLogix** (PCCC addressing)
* **SLC 500** (Legacy, PCCC)
* **PLC-5** (Legacy, PCCC)
* **LogixPCCC** (Specific mode for Logix via PCCC)

---

## STEP 1. Connection Configuration (`plc_ethernet_ip_connection`)

This step establishes the communication session with the controller.

![EtherNet/IP Connection Settings](images/eip_connection.png)

### 1.1 General Settings

| Parameter | Description |
| :--- | :--- |
| **Name** | Unique system name for the connection (e.g., `cip_line1_main`). |
| **Period (ms)** | Polling period. <br>*Recommendation:* Typically 100-500 ms for EtherNet/IP. CIP is a fast protocol, but avoid overloading EN2T modules. |
| **Shutdown timeout** | Timeout for graceful TCP session termination (CIP Forward Close). |
| **Master connection** | Used for Redundancy configuration. Reference to the main channel. |
| **Support for group requests** | **Yes** — enable optimization (Multi-Request packets). The driver will pack multiple read requests into a single Ethernet frame. |

### 1.2 Controller Settings

This is a critically important section defining the addressing method.

![Controller Types](images/plc_type.png)

| Field | Description and Analysis |
| :--- | :--- |
| **Controller Type** | Select the PLC family:<br>• **ControlLogix:** Uses symbolic tag names. The most modern mode.<br>• **MicroLogix / SLC / PLC5:** Use data file addressing (N7:0, F8:1). |
| **IP** | IP address of the communication module or processor. |
| **Routing** | *Optional.* CIP Path to access the processor if it is not located in the same slot where Ethernet connects, or resides in a different chassis.<br>*Format:* Usually specified as a sequence of pairs `Port,Address`.<br>*Example:* `1,0` (Backplane, Slot 0). Leave empty for CompactLogix (chassis-less). |

---

## STEP 2. Tag Configuration (`plc_ethernet_ip_binding`)

In the EtherNet/IP protocol (especially for ControlLogix), data is accessed by **Tag Name**, not by memory address.

![Tag Binding Settings](images/eip_