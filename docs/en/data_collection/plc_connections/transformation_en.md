# PLC binding transformations

[Connection catalogue](./index.md) · [Binding setup](./bindings_en.md)

Faceplate v4.0.7. **Трансформация** processes values between a driver and a project field. An empty chain adds no processing; field-type conversion still applies.

## Direction and order

Reading applies operations from top to bottom: external value → direct chain → field type → field. Writing applies field → outgoing type conversion → reverse operations in reverse order → driver. Server publication W also uses the reverse chain.

| Operation | Parameters | Reading R/RW | Writing or publication W/RW |
|---|---|---|---|
| Scaling | Factor 1, shift 0; shift is labelled Cмена | y = x × Factor + shift | x = (y − shift) / Factor; Factor must be nonzero |
| Default Value | Value 0 | Preserves numbers; replaces nonnumeric/missing input with Value | Passes the value through |
| Limit Control | Lower Limit 0, Upper Limit 0 | Inclusive bounds; outside gives a missing value | Clamps a number to the bound |
| Damper | Tlag 1 ms | Smooths; the first number passes through | Passes the value through |
| Integration | None | Accumulates input × actual interval in ms; first result is missing | Unsupported |
| Derivative | None | Change / actual interval in ms; first result is missing | Unsupported |
| Скрипт | Erlang, context, state | Executes a user function | Unsupported |

Before saving Limit Control, set **Upper Limit > Lower Limit**; initial 0/0 is incomplete. Damper requires a positive Tlag. Integration and Derivative use processing time in milliseconds: output units are input units × ms and input units / ms. Reinitialization recreates state; this is not a persistent historical total.

## Configure a scale and verify both sides

1. Add **Scaling** to an R binding targeting a float field. Enter Factor **0.1**, shift **0**, then press Tab.
2. Save, reopen independently and confirm **0.100000 / 0.000000**. If 1 remained, edit the saved element and repeat verification.
3. External 1000 should produce field **100.0**; 1001 should produce **100.1**.
4. Where writing is supported, set the W/RW field to **120.0**. The reverse scale gives **1200**; verify by independent reading.

Limit Control bounds apply at its position in the chain. Scaling 0.1 before Limit Control 0…150 checks the engineering value. Default Value after rejected input may produce a number again.

## Write an Erlang script

Select **Доступ = R** and add **Скрипт**. The function receives Input, Context and State and returns **{Output, State}**. Context is a map keyed by **variable** names; each variable is linked through **tag** and **field**. Initial state is undefined.

For scaling with an additional offset, enter variable **Offset** and link a prepared numeric offset tag and its field. Insert:

    fun(Input, Context, State) ->
        Offset = maps:get("Offset", Context, 0),
        case is_number(Input) andalso is_number(Offset) of
            true -> {Input * 0.1 + Offset, State};
            false -> {none, State}
        end
    end.

Select **Compile**, save and reopen the binding. Input 1000 and Offset 2 should produce **102.0**; Input none should produce **none**. Compile checks syntax; verify output, context links and new input data separately.

To normalize incoming Boolean to numeric 0/1 before bool-field conversion, a separate R chain can use:

    fun(true, _Context, State) -> {1, State};
       (false, _Context, State) -> {0, State};
       (_, _Context, State) -> {none, State}
    end.

Test both source states. This function expects true/false; numeric 0/1 is another representation. Script has no reverse transformation and cannot be used with W/RW. This PLC transformation executes Erlang.

## Missing data and errors

Default Value may conceal missing communication with a plausible number; it substitutes a nonnumeric result and is not a general exception handler. Direct-processing errors may produce a missing result while transport works. Reverse-processing failure does not guarantee write suppression: check the external result.

Every operation in W/RW must support reverse processing. Use R for Script, Integration or Derivative. A valid chain does not add unsupported driver writes or automatically repair String/Boolean incompatibilities.
