# Verify and diagnose PLC exchange

[Connection catalogue](./index.md) · [Bindings](./bindings_en.md)

Faceplate v4.0.7. Check configuration, execution permission, channel and individual signal in sequence.

For the **Diagnostics** window and its log controls, see [Diagnostics of Runtime objects](../../administration/diagnostics/diagnostics.md).

## Verification map

| Level | Where to inspect | Sufficient result |
|---|---|---|
| Configuration | Reopened connection and binding | Addresses, types, access, transformation, tag and field are saved |
| Execution | Отключено/Отключить, folder, Runtime, Узел/PID | Intended execution is permitted and a process exists |
| Channel | Ошибка, Актуальное соединение, external participant | Correct path is reachable and an addressed operation succeeds |
| Signal | Binding state/error/value and tag field | A new known value reaches the correct field |
| Write | Response and independent external reading | New command is received after reverse processing |
| Equipment | Feedback signal or device check | Expected physical result is confirmed |

RUN, OK, PID and an old number alone do not confirm new data. IEC cycles may read an old cache; TS may belong to an earlier message. A server's local model can remain without an external client.

## Collect a log

1. Select the saved connection in **Общий вид → Редактировать** and select **Диагностика**.
2. Choose **Log level**: info, warning, error or debug. **Log limit** defaults to 1000, range 1–100000.
3. Select **Start**, reproduce the action and inspect **Logs** and **Процессы**.
4. Use **Копировать** to retain messages; record time, connection path and binding. **Очистить** clears the displayed output.
5. Select **Stop** and close the window. Start/Stop control log collection; **Отключено** controls exchange.

The window is available in STOP. Empty Logs/Процессы establish neither health nor absence of a process. A complete network frame or a message for every successful request is not guaranteed.

## Find the cause

| Symptom | Check | Action and confirmation |
|---|---|---|
| STOP/no process | Flags, parents, node, dependencies | Remove the execution blocker, then verify process and new value |
| timeout/closed/connection failure | Address from execution node, port, transport, serial settings | Restore the path and confirm a fresh addressed operation |
| One signal fails | Address/type/attribute, permissions, tag and field | Correct the signal and receive a new control value |
| Incorrect value | Width, signedness, byte order, scale, field type | Compare known input with the calculation |
| A number remains after failure | Default Value, old cache/field, binding error | Correct the cause and confirm new reception |
| Write without result | Access, driver support, command, reverse chain | Independently read the external side and verify feedback |
| List shows ОШИБКА but text says no errors | Flag, PID, tooltip, Ошибка | Assess actual execution and signal; row colour does not identify the cause |

## Verify recovery

1. Record successful value A externally and in the field.
2. On your test setup, introduce one failure: unavailable source or incorrect address. Record the binding error and inspect a control signal separately where available.
3. Correct the cause and establish a new source value B different from A.
4. Confirm B independently, then wait for the expected transformed B in the same Faceplate field.
5. For writes, issue a new permitted command and verify it independently. W may resend its current value on activation; check it beforehand.

If the reading remains constant, use an independently observed new request/response for that signal. Rereading a cache, clearing an error and retained A do not establish recovery.
