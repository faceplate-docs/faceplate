# PLC connections: catalogue and configuration route

Faceplate v4.0.7 · Revision 3 November 2026 · For integrators.

## Start configuration

1. Select the driver using the device interface and Faceplate role in the table.
2. [Prepare a tag and field](./bindings.md#prepare-a-tag-and-field), then open the protocol guide.
3. Save the connection and complete binding disabled. Verify address, representation, direction, tag and field.
4. Configure a [transformation](./transformation.md) when scaling or processing is required.
5. Once the external participant is ready, [verify a new value and recovery](./diagnostics.md).

The detailed [Modbus TCP training example](./general.md) is an additional first-exchange route. For another protocol use its own guide; the links above cover shared tasks.

## Choose a connection

“Write” means an actual driver operation. Common R/W/RW and grouping controls may remain visible without the corresponding implementation.

| Guide | Role and transport | Data and directions | Grouped PLC operations |
|---|---|---|---|
| [Modbus](./plc_modbus_connection.md) | Client; TCP, RTU-TCP, serial | Numeric/discrete registers; R/W/RW by area | Reading; byte limit |
| [S7](./old_plc_s7_connection.md) | Client; TCP | I/Q/M/DB; bit/byte/word/dword; R/W/RW by address | Reading; byte limit |
| [EtherNet/IP](./plc_ethernet_ip_connection.md) | Client; TCP | Scalar variables on supported CPUs; R/W/RW | Reading/writing; read limit counts variables |
| [DCON](./plc_dcon_connection.md) | Polling; TCP, serial | DI/AI: R; DO/AO: R/W/RW | None |
| [OPC DA](./plc_opcda_connection.md) | Client through TCP proxy | ItemID; R/W/RW with a compatible proxy | None |
| [OPC UA client](./old_plc_opcua_client_connection.md) | Client; opc.tcp | Scalar BrowseName path; R/W/RW with type restrictions | Reading/writing; read limit counts nodes |
| [OPC UA server](./old_plc_opcua_server_connection.md) | Server; opc.tcp | W: publication; R: reception; RW: both, with type restrictions | Local reading/writing; node count |
| [SNMP](./plc_snmp_connection.md) | v2c manager; IPv4/UDP | Numeric OID reading; SET needs build verification | None; does not enable GETBULK |
| [M-Bus](./plc_mbus_connection.md) | Polling; TCP, serial | Numeric telegram block; read only | None |
| [Mercury 230](./plc_mercury230_connection.md) | Polling; TCP, serial | Cumulative energy by tariff; energy reading only | None |
| [IEC 62056](./plc_iec62056_connection.md) | Polling; TCP, serial | Numeric address/password/OBIS parameter; read only | None |
| [IEC101 client](./plc_iec101_client_connection.md) | Client; serial | IOA attributes and commands; R/W/RW | None; Group request is separate |
| [IEC101 server](./plc_iec101_server_connection.md) | Server; serial | Publication W, reception R, both RW | None; Group broadcast is separate |
| [IEC104 client](./plc_iec104_client_connection.md) | Client; TCP | IOA attributes and commands; R/W/RW | None; Group request is separate |
| [IEC104 server](./plc_iec104_server_connection.md) | Server; TCP | Publication W, reception R, both RW | None; Group broadcast is separate |

For OPC UA, verify Boolean/String handling, both certificate and key, and the actual security mode. For S7, check Slot/timeout availability in your editor. Confirm SNMP SET on the actual build first. Protocol guides contain details and applicable checks.

IEC 62056 implements an IEC 62056-21-style exchange with numeric responses; DLMS/COSEM and writes are unavailable. M-Bus and Mercury do not assign units or coefficients automatically.

## Shared guides

- [Bindings and fields](./bindings.md): type, direction, saving, channel map, import/export and alternative channels.
- [Transformations](./transformation.md): seven operations, reverse chain, units and Erlang.
- [Diagnostics](./diagnostics.md): execution, channel, signal, independent write confirmation and recovery.
- [IEC types and attributes](./iec_reference.md): shared IEC101/IEC104 catalogue, quality, time and command mapping.

## Interpret verification information

Saving and independently reopening verifies configuration. Exchange requires a new result at the receiving side. Equipment examples and control numbers in added explanations are configuration recipes unless an executed test is explicitly stated.

Earlier forms and screenshots for most guides were checked in the available Studio 4.0.6.subs while the documentation targets v4.0.7. This does not establish binary/source identity. Dates and individual test boundaries remain in the verification records; a text revision does not imply another hardware test.
