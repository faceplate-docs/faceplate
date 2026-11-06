# PLC bindings: prepare fields and configure a signal map

[Connection catalogue](./index.md) · [Transformations](./transformation_en.md) · [Diagnostics](./diagnostics_en.md)

Faceplate v4.0.7. A connection defines the shared channel; a child binding links one signal to one project field. Use the actual device map for addresses and formats.

## Prepare a tag and field

1. Choose a separate training folder in **Меню → Общий вид**. Define the tag name, field, type and units.
2. Use a suitable project primitive. If none exists, prepare a primitive type with a **value** field and its Runtime flag enabled, then create an instance in the training folder. The field need not be named value.
3. Choose **float** for fractional measurements and scaling, **integer** for integers and masks, and **string** for text. Use **bool** only for two states; a 0…3 code requires integer.
4. Open the instance and check that the field is visible and available in Runtime. Initialize float to 0.0, integer to 0 or string to empty text. Initialization is not a read result.
5. For W/RW, establish the permitted command before enabling the binding. W may send it on activation without a new operator action.

Example destination: folder **PLC_Training**, tag **AnalogValue**, field **value**, type float, initial 0.0. The project owner prepares primitive types and permissions; device addresses belong in bindings.

## Create a complete binding

1. Configure the connection using its protocol article. Save it with **Отключено** enabled until preparation is complete.
2. Double-click the connection and select **Создать**. The binding must be directly inside that connection.
3. Enter a name and enable **Отключить**. Set the signal address, type and format from its map.
4. Select the project object beside **тег**, then separately select **value** in the adjacent field list. Check the full path and field type.
5. Choose direction using the table. Configure any scale using the [transformation guide](./transformation_en.md).
6. Save, close and reopen the object independently. Check address, type, direction, transformation, tag and field.
7. Once the external participant is ready, enable the intended connection and binding. Project, parent-folder and execution-node conditions must also permit execution.
8. Confirm a new value in the selected field; independently verify the external side for writes.

| Access | Client driver | Server driver |
|---|---|---|
| R | Device → Faceplate field | Server model → field; an external client supplies a value or command |
| W | Field → device; no periodic reading | Field → server model → external client |
| RW | Both directions | Both directions; initial publication depends on the driver |

Access sets direction, not permissions. A W/RW option does not add writes to M-Bus, IEC 62056 or Mercury cumulative energy. For servers, direction relative to Faceplate does not prohibit external client writes to a node.

## Verify type and scale

For a numeric training signal, use source 1000 and **Scaling: Factor 0.1, shift 0**. Expect 100.0 in a float field. Change the source to 1001: expect 100.1. An integer destination rounds fractional results.

Where writing is supported, command 120.0 with this scale corresponds to 1200 externally. Server publication uses the reverse chain: field 120.0 is published as 1200. Verify the intended direction.

## Configure an alternative channel

1. Confirm standalone operation of the main connection first.
2. Create an alternative connection of the same type with another transport configuration. Set **Главное соединение** on the alternative to the main connection.
3. Check the link and automatic disabling of the alternative's independent execution. Do not create chains of main connections.
4. The alternative's data map must match the main connection's bindings. The main connection uses its own bindings.
5. Reproduce a connection failure on a test setup, inspect **Актуальное соединение** and confirm a new value. Separately check return to the main path.

Switching is driven by connection failure, not every address error. SNMP may register an unreachable agent successfully; a TCP gateway may open a channel without a reachable meter. For servers, no connected client does not itself mean local listener failure. A retained path and automatic return to the preferred channel require independent verification.

## Expand one signal into a channel map

1. Prepare a table: name, external address, type, direction, units, transformation, tag and field.
2. Verify one complete binding as a reference. When copying, change address and destination and reopen the copy.
3. For bulk preparation, use **Экспорт .xlsx** from a supporting editor. Use the exported workbook as the column and format template; handle service identifiers according to project import rules.
4. Back up the configuration before import. First transfer 10 training signals into a separate folder with execution disabled. Select the correct import context.
5. Inspect the import report, object count, parent connections, field links, duplicate addresses and competing write sources. Reopen a sample of bindings and compare with the map.
6. Enable exchange after checking W/RW destinations. Repeat independent data verification.

An .xlsx command does not establish that an arbitrary workbook creates a valid PLC map. Check the export format and import result on the actual build.

## Change and disable

**Отключено** stops the whole connection; **Отключить** excludes one signal. Saving channel settings may recreate its process. Disabling a signal does not guarantee field clearing; a server node may remain until restart.

Before deletion or relocation, inspect **Перекрёстная ссылка** and field destinations. Confirm a new read or write after changes using the [verification procedure](./diagnostics_en.md).
