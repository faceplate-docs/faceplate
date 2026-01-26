# PLC Connections

## Module Purpose

The **PLC Connections** module is designed for configuring and managing connections between **Faceplate Runtime** and external automation devices/systems:

- **PLC/RTU/IED** (controllers, terminals, protection relays)
- **Meters and measuring devices** (electricity meters, heat meters, etc.)
- **OPC servers**
- Other sources of process data via industrial protocols

Via PLC connections, the system receives and/or sends:

- **Tags/signals** (AI/DI/DO/AO)
- **Events and alarms**
- **Service communication statuses**
- **Control commands** (if permitted by configuration)

---

## How PLC Connections Are Used

PLC connections are used for:

1. **Telemetry collection** Reading sensor values, states, and measurements.

2. **Sending commands** Discrete control, setpoints, acknowledgments, etc.

3. **Integration with third-party systems** OPC DA/UA, gateways, SCADA systems, RTU concentrators.

4. **Availability monitoring** Communication channel diagnostics, connection statuses, exchange statistics.

---

# Client and Server Connections

## Client Connection

A **Client connection** means that **Faceplate initiates the connection** to the remote side:

- Faceplate connects via IP/port (or COM port) itself
- Performs exchange according to the protocol
- Receives/transmits data

**Examples:**
- IEC-104 Client → connection to a protection relay (IED)/RTU server
- Modbus Client → device polling via TCP/RTU
- OPC UA Client → reading data from an OPC UA server

---

## Server Connection

A **Server connection** means that **Faceplate listens for incoming connections** (accepts the connection as a server):

- An external device/system connects to Faceplate
- Faceplate services incoming requests/sessions
- Provides data or accepts commands

**Examples:**
- IEC-104 Server → upper-level SCADA connects to Faceplate
- OPC UA Server → clients read values from Faceplate

---

# Supported PLC Connection Types

Listed below are the types available in the **/plc** folder.

## Client Connections (Supported)

- **plc_iec101_client_connection** → [IEC-101 Client](./plc_iec101_client_connection_ru.md)
- **plc_iec104_client_connection** → [IEC-104 Client](./plc_iec104_client_connection_ru.md)
- **plc_opcua_client_connection** → [OPC UA Client](./plc_opcua_client_connection_ru.md)

---

## Server Connections (Supported)

- **plc_iec101_server_connection** → [IEC-101 Server](./plc_iec101_server_connection_ru.md)
- **plc_iec104_server_connection** → [IEC-104 Server](./plc_iec104_server_connection_ru.md)
- **plc_opcua_server_connection** → [OPC UA Server](./plc_opcua_server_connection_ru.md)

---

## Other Connections (General Types)

- **plc_ethernet_ip_connection** → [EtherNet/IP](./plc_ethernet_ip_connection_ru.md)
- **plc_mbus_connection** → [M-Bus](./plc_mbus_connection_ru.md)
- **plc_modbus_connection** → [Modbus](./plc_modbus_connection_ru.md)
- **plc_opcda_connection** → [OPC DA](./plc_opcda_connection_ru.md)
- **plc_s7_connection** → [Siemens S7](./plc_s7_connection_ru.md)
- **plc_snmp_connection** → [SNMP](./plc_snmp_connection_ru.md)

---

# Creating a PLC Connection

*Step 1.* In the project tree, navigate to the directory where the PLC connection will be located.
*Step 2.* Click the **"Create"** button.
*Step 3.* In the object tree, open the **plc** section.
*Step 4.* Ensure the list of available connection types is displayed.
![PLC folder1](images/create_plc_connection_1.gif)
*Step 5.* Select the required connection type.
*Step 6.* Click the **"OK"** button.
*Step 7.* The connection configuration window will open.
![PLC folder2](images/create_plc_connection_2.gif)