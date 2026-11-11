# IEC 62056 in Faceplate: configure reading and bindings

[Catalogue](./index.md) · [Bindings](./bindings.md) · [Transformations](./transformation.md) · [Diagnostics](./diagnostics.md)

Faceplate v4.0.7 · Revision 3 November 2026. This guide is based on the researched implementation; the configuration below is not claimed as verified through UI or device exchange.

## Capabilities and prerequisites

Faceplate initiates an IEC 62056-21-style exchange: device identification, programming mode, password, R1 request and exit. Transport is TCP to a compatible gateway or serial on the execution node. DLMS/COSEM, server operation and parameter writes are unavailable. Select **R** for reading; visible W/RW options do not add writes.

Obtain transport, address/port or serial settings, literal device address, password, numeric parameter OBIS, response format, units and multiplier. Devices/OBIS are not discovered automatically. Each parameter has a separate session; more bindings extend the complete cycle.

Use the [shared procedure](./bindings.md#prepare-a-tag-and-field) to prepare folder **IEC62056_Training**, tag **MeterValue**, float field **value**, initial 0.0. The parameters below are illustrative; no compatible source at 127.0.0.1:14000 is assumed installed.

## Create a connection and complete binding

| Object | Example fields |
|---|---|
| Connection TrainingIEC62056 | Тип tcp; IP/Hostname/Localhost 127.0.0.1; Порт 14000; Период 1000 ms; timeout 1000 ms; attempts 3 |
| Shared settings | Shutdown timeout 60000 ms; Главное соединение empty; Отключено enabled |
| Binding Parameter1 | address 1; password 1; OBIS 1.8.0; Доступ R; Отключить enabled |
| Destination | /IEC62056_Training/MeterValue; field value; empty Трансформация |

1. Open the training folder in **Меню → Общий вид**, select **Создать**, then the IEC 62056 connection in **plc**.
2. Name it TrainingIEC62056 and enable **Отключено** before saving. Enter transport and numbers from the table; finish input with Tab.
3. Explicitly set timeout **1000**: the form's initial 10000 exceeds its own 6000 limit. Do not treat the initial value as verified configuration.
4. Select **save**, close and independently reopen using **Редактировать**. Check settings and disabling.
5. Double-click the connection and create Parameter1. Enable **Отключить** and enter address, password and OBIS.
6. Select MeterValue beside **тег**, separately select **value**, R and an empty transformation.
7. Save and independently reopen the binding. Check the complete destination and literal meter credentials.

Device address and OBIS are sent literally; example 1.8.0 does not establish that every meter provides this parameter. Replace the password with the actual value. One connection may contain different address/password combinations where the line supports them.

## Configure serial

Select **Тип serial** and set an existing node port, baud rate, parity, stop bits and data bits from the meter settings. Initial form fields are /dev/tty0, 9600, none, 1, 8; these are not universal line settings.

The driver does not change port speed after identification. A meter changing speed after ACK needs a compatible mode or gateway and separate verification. Save disabled configuration and reopen it before operational startup.

## Verify the number and units

The driver accepts a numeric response body between STX and ETX; units after * are discarded. Numeric part 230.1 produces 230.1. Date/time strings, decimal commas, echo or an OBIS prefix before the parenthesis may not match the expected format.

An empty transformation passes the number without assigning units. If the map requires factor 0.1, set Scaling 0.1/0: raw 1000 should produce 100.0. Choose the multiplier from the map, not the OBIS name.

For operational startup, replace illustrative settings, enable the intended connection/binding and project execution conditions. Match a new meter response to the correct field. Overall RUN/OK does not exclude an individual OBIS error.

## Parameters and duration

| Field | Initial display / condition |
|---|---|
| Тип | tcp or serial; one transport is active |
| TCP port | Form 1024; model 4000; explicitly enter the actual port |
| timeout | Form 10000 with range 1–6000 ms; explicitly 1000 in the example |
| attempts | 3; form range 1–500; attempts for an individual transaction |
| Period | 1000 ms; whole cycle, not a promised per-reading frequency |
| Grouped PLC requests | Unsupported; shared grouping, packet and ratio settings do not combine these requests |
| Ограничение памяти (байт) | System value 1024; actual unit MiB despite the label |

A session includes several requests, response-completion waiting and service pauses. Its duration may substantially exceed the period. Start with one parameter, measure the complete cycle, then expand the map. Increasing period does not fix a password or response format.

## Change, redundancy and recovery

Change the channel through **Редактировать → save**, then reopen independently. **Отключено** applies to the whole connection; **Отключить** applies to one parameter. A retained old number or Default Value does not confirm communication.

An [alternative channel](./bindings.md#configure-an-alternative-channel) uses the main connection's bindings. A successfully opened gateway with an incorrect password/OBIS does not guarantee switching.

## Diagnostics

| Message/symptom | Check and correct | Confirm |
|---|---|---|
| econnrefused/timeout or serial error | Address/port from execution node, port path and line settings | Correct channel opens and a new response arrives |
| invalid_identification | Response beginning, echo and identification format | Correct device identification succeeds |
| invalid_authentification_request | Programming-mode support and P0 response | Device accepts the mode |
| invalid_password | Password, address, complete response and wait | New access session succeeds; the message does not always mean only a bad password |
| invalid_obis | OBIS, access and R1 response | New parameter response arrives |
| no_block_start/no_block_end | STX/ETX, echo, prefix and frame completeness | Numeric body is decoded |
| invalid_value | Numeric format, decimal point and unit after * | Expected number reaches the field |
| RUN with empty/old field | Binding error, tag/field, transformation and freshness | A new known value appears in the selected field |

Open [shared diagnostics](./diagnostics.md#collect-a-log). Start/Stop control logging. After correction, obtain new B instead of old A; for constant readings confirm a new successful request/response. Working transport, a cleared error and an old number do not replace this check.
