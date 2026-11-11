# IEC101/IEC104: types, attributes and command mapping

[Connection catalogue](./index.md)

Faceplate v4.0.7. This reference covers IEC101/IEC104 clients and servers. Direction depends on the role: a client reads the remote cache/sends commands; a server publishes a local object/receives commands.

## Select Type and Parameter

Select the information Type from the device map, then explicitly select Parameter. Create a separate binding for each attribute at the same IOA. Server bindings sharing an object must agree on Type and Group. Value does not automatically create quality or time fields.

| TypeID | Name | Parameter in the form |
|---|---|---|
| 1 | M_SP_NA_1 | Value, QDS, SIQ |
| 2 | M_SP_TA_1 | Value, QDS, SIQ, TS |
| 3 | M_DP_NA_1 | Value, QDS, DIQ |
| 4 | M_DP_TA_1 | Value, QDS, DIQ, TS |
| 5 | M_ST_NA_1 | Value, VTI, QDS |
| 6 | M_ST_TA_1 | Value, VTI, QDS, TS |
| 7 | M_BO_NA_1 | Value, QDS |
| 8 | M_BO_TA_1 | Value, QDS, TS |
| 9 | M_ME_NA_1 | Value, QDS |
| 10 | M_ME_TA_1 | Value, QDS, TS |
| 11 | M_ME_NB_1 | Value, QDS |
| 12 | M_ME_TB_1 | Value, QDS, TS |
| 13 | M_ME_NC_1 | Value, QDS |
| 14 | M_ME_TC_1 | Value, QDS, TS |
| 15 | M_IT_NA_1 | Value, BCR |
| 16 | M_IT_TA_1 | Value, BCR, TS |
| 17 | M_EP_TA_1 | Value, SEP, Duration, TS |
| 18 | M_EP_TB_1 | Value, QDP, Duration, TS |
| 19 | M_EP_TC_1 | Value, QDP, Duration, TS |
| 20 | M_PS_NA_1 | Value, QDS |
| 21 | M_ME_ND_1 | Value |
| 30 | M_SP_TB_1 | Value, QDS, SIQ, TS |
| 31 | M_DP_TB_1 | Value, QDS, DIQ, TS |
| 32 | M_ST_TB_1 | Value, VTI, QDS, TS |
| 33 | M_BO_TB_1 | Value, QDS, TS |
| 34 | M_ME_TD_1 | Value, QDS, TS |
| 35 | M_ME_TE_1 | Value, QDS, TS |
| 36 | M_ME_TF_1 | Value, QDS, TS |
| 37 | M_IT_TB_1 | Value, BCR, TS |
| 38 | M_EP_TD_1 | Value, SEP, Interval, TS |

## Interpret value, quality and time

Single Point Value is 0/1; Double Point is 0…3. Normalized measurements already range from −1…1; scaled measurements use signed16, floating point uses float32. Choose integer for masks and codes, float for fractional measurements.

QDS/SIQ/DIQ and other descriptors are packed numbers. Single Point uses QDS quality mask 254; Double Point uses 252. Bad quality does not itself block Value. BCR contains the full 40 bits; counter Value is signed32.

CP24 TS means milliseconds within an hour, without a complete date or hour. CP56 TS is Unix time in milliseconds, converted through the node's local timezone. Server transmission without an explicit CP56 timestamp may use encoding time for an old value. A timestamp is not a universal freshness indicator.

## Example: one IOA's value, quality and time

For a source with IOA 100 and Type 36: M_ME_TF_1, prepare float Measurement.value and integer Quality.value and Timestamp.value. Create three bindings: Address 100, Type 36, Parameter Value/QDS/TS respectively, each linked to its own field.

Use R for a client; use W for server publication. External measurement 21.5 should match Measurement.value=21.5 without transformation. Verify quality and time independently; three separate updates are not an atomic snapshot.

## Example: command and feedback state

For a client, base Address 101, Type 1 and Parameter Value describe feedback; Доступ RW, Remote control type 45: C_SC_NA_1 and Remote control address 200 describe the command. Numeric command 1 targets IOA 200; state is read from IOA 101.

For a server, Address 101, Type 1, Parameter Value, Доступ R, Remote control type 45 and Remote control address 200 receive a command into the selected field. This transfers from the server model; equipment needs a separate output link.

Command pairs without time/with CP56: 45/58 single, 46/59 double, 47/60 step, 48/61 normalized setpoint, 49/62 signed16, 50/63 float32, 51/64 unsigned32.

Agree direct activation and permitted values with the external participant. Separate verified Select/Execute semantics are not provided. ACTCON/ACTTERM and physical feedback are distinct checks. These are configuration examples; this reference does not claim new command tests.
