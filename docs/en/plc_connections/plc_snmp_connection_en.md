# SNMP Configuration in Faceplate

## Overview
**SNMP** (Simple Network Management Protocol) is an open communication protocol defined by the IETF. It is widely used to exchange data with network devices (controllers, gateways, UPS, etc.).

In **Faceplate**, **SNMPv2** and **SNMPv3** are supported.

Integration consists of two stages:
1. **Connection (`plc_snmp_connection`):** Network transport setup and redundancy logic.
2. **Binding (`plc_snmp_binding`):** Addressing specific variables (OIDs) within the device.

---

## STEP 1. Connection setup (Connection)

At this stage you create a transport channel to the target equipment.

![Connection setup window](images/snmp_connections.png)

### 1.1 Diagnostic panel (Runtime)
*Top part of the window. Shows the current process state.*

| Field | Description |
| :--- | :--- |
| **State** | **STOP** (Red) — driver stopped.<br>**RUN** (Green) — driver running. |
| **Error** | Last error text. `no errors` — normal operation. |
| **Actual connection** | **Active channel indicator.**<br>Shows which connection is currently used for polling.<br>• If redundancy is not configured — equals the current one.<br>• With redundancy — shows whether `Master` or backup channel is active. |

### 1.2 Configuration settings (Settings)

**Base settings:**
- **Name:** Unique system name (Latin characters, no spaces).
- **Period (ms):** Polling interval (default `1000` ms).
- **Shutdown timeout (ms):** Time to gracefully close the socket (default `60000`).

**Redundancy settings:**
- **Master connection:** Reference to the main connection.  
  *Used to configure a backup channel.* If the current connection is a backup, specify the main connection name here. The system will switch channels automatically based on availability.

**Network settings:**
- **IP/Hostname:** Target device IP address/hostname.
- **Port:** `161` (standard UDP port for SNMP agent).
- **Community:** Access password. Commonly `public` (read-only) or `private` (write).
- **Support for group requests:** `Yes` — enable `GetBulk` (batch read). Recommended for faster polling if the device supports it.

> **Action:** Click **Save**. After saving, open the object (double click) to configure tag bindings.

---

## STEP 2. Variable setup (Binding)

Inside the connection, create `plc_snmp_binding` objects. Each object corresponds to one variable (OID) on the device.

![SNMP binding setup window](images/snmp_bindings.png)

### 2.1 Binding parameters

| Field | Description |
| :--- | :--- |
| **Name** | Binding name in the project tree. |
| **Tag** | Faceplate system tag where the value will be written. |
| **Transformation** | *Optional.* On-the-fly data transformation (scaling, bit masks). |
| **Access** | Variable access rights:<br>• **R** — Read-only.<br>• **W** — Write-only.<br>• **RW** — Read/Write. |
| **Address** | **OID (Object Identifier).** Address of the variable in SNMP hierarchy.<br>*Examples:* `1.3.6.1.2.1.1.1.0` (absolute) or `1.6.3.1` (relative, if supported). |

### 2.2 Runtime control
- **State:** Current binding state (active/error).
- **Off:** Switch to temporarily disable polling for a specific tag without deleting the configuration.

---

<!-- ## Additional notes

1. **Redundancy:** When configuring a backup channel, ensure `Master connection` contains the correct name of the main channel. `Actual connection` in Runtime shows which channel currently drives polling.
2. **OID validation:** If you see `No Such Name`, verify the **Address**. Use a third‑party MIB Browser to validate OIDs before configuration.
3. **Startup sequence:**
   1. Configure Connection.
   2. Start the driver (`State: RUN`).
   3. Ensure there are no communication errors.
   4. Create Bindings. -->
