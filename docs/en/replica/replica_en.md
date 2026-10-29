# Replication in Faceplate: Configure Data Exchange and Verify Delivery

A guide for integrators configuring data transfer between a site and a control center. The settings and behavior described here are based on the examined Faceplate 4.0.7 implementation.

Russian UI labels are retained with English explanations so you can match them to the interface shown in the screenshots.

**Contents**

- [What replication does](#what-replication-does)
- [Prerequisites](#prerequisites)
- [Configure data exchange](#configure-data-exchange)
- [Manage the replication channel](#manage-the-replication-channel)
- [Transfer pump station data to the control center](#transfer-pump-station-data-to-the-control-center)
- [Parameter and state reference](#parameter-and-state-reference)
- [Troubleshooting](#troubleshooting)
- [Replication limitations](#replication-limitations)

## What replication does

Replication transfers object data from one site to another Faceplate instance or cluster. For example, a control center receives pump station pressure, its history, and messages indicating that a threshold has been exceeded.

To set up data exchange, create a pair of **Replica** objects with the same **GUID**. One object runs at the site; the other runs at the control center. Each object's parent folder defines the scope of data exchange, including its subfolders.

| Data | Direction | What to verify |
|---|---|---|
| Current object fields | Site → center | The value in the corresponding object at the center |
| Changes to current fields at the center | Center → site | The changed value at the site |
| Archive history | Site → center | Stored points within the selected interval |
| Messages belonging to the folder's message group | Site → center | Records with the expected source, text, and time |

Tags and archives must already exist on the receiving side. Replication matches them by their paths relative to the exchange folder. For example, the **Process/Pressure** object at the site must have a corresponding **Process/Pressure** object at the center. The enclosing parent folders may have different names: matching uses the relative path.

The object type determines which current fields are included. The entire project configuration is not transferred. Prepare archives and message templates before configuring replication; check transferred records in trends and the message log.

The overall workflow is: prepare corresponding objects on both sides → create the pair → align the identifier, nodes, and addresses → save the settings → verify each data flow on the receiving side.

## Prerequisites

This example requires two accessible Faceplate instances or clusters with the replication module. The user must have permission to modify the example folders, create objects, and view values, archives, and messages. The exchange folders must be enabled and have execution nodes assigned.

Provide connectivity in both directions: the center receives site data, while the return address is needed for initial retrieval of current data and for changes sent back to the site. Obtain node names from the active Faceplate configuration; the node name and HTTP address are separate settings.

### Example connection details

| Parameter | Site | Control center |
|---|---|---|
| Example node name | `site@site.example` | `center@center.example` |
| Example service base address | `http://site.example:9000` | `http://center.example:9000` |
| Exchange folder | PumpStation | PumpStation |
| Replication object to create | StationLink | StationLink |

Domains ending in **.example**, node names, and port **9000** are placeholders. They illustrate the required format and do not specify your installation's addresses or default port. Enter the actual service addresses and full node names for your system.

### Example objects

Prepare the following objects inside **PumpStation** on each side. Creating replication does not create them automatically.

| Relative path or purpose | Site | Center |
|---|---|---|
| Process/Pressure — current pressure | 2 bar | 0 bar before data exchange |
| Setpoint — example setpoint | 3 bar | 3 bar |
| PressureArchive | Archive of the Pressure value, recorded every 1 s | Corresponding archive at the same relative path |
| High pressure message | Pressure above 4 bar condition, using the exchange folder's message group | Ability to view the transferred message |

Use example values with no connection to actuators. The pressure and setpoint fields must support entering fractional numbers through the form and belong to the object's current data. If your object type uses different fields, select corresponding fields on both sides.

For the maintenance stage, prepare separate **MaintenanceA** and **MaintenanceB** folders at the site, outside **PumpStation**. Both folders must be disabled before copying. This example does not require clearing the example data or the working pair.

## Configure data exchange

### Identifier, roles, and scope

The **GUID** links the two sides of a pair. Generate it on one side and copy it to the other. Use a different identifier for another independent pair. Copying an object preserves its GUID, so the copy does not form a new independent pair unless you change this field.

**Receive Nodes** specifies the receiving nodes. If the local node is in the list, the object acts as a receiver. On the side with no matching local node, it acts as a sender on its folder's nodes. This setting does not require a separate sender/receiver switch.

For this example, enter the center's node in **Receive Nodes** for both objects. The site folder must run on the site's node, and the center folder on the center's node.

The object's location affects which data is transferred. Moving it to a different folder changes the scope of data exchange. Check the relative paths of tags and archives on both sides; matching the final object name alone is insufficient if the subfolders differ.

### Forward and return addresses

Use **URL** for the receiving service addresses at the center and **URLS back** for the service addresses at the site. The channel address ends in **/REPLICA**. Faceplate adds any additional service path components itself.

Address lists provide sequential attempts: after a successful response, the first working address is used. The list does not enable simultaneous delivery to all listed recipients. A fallback address must point to the corresponding receiving side with the required configuration.

### Period, maximum step, and timeout

**Период (мс)** (period in milliseconds) sets the data exchange processing cycle. It does not guarantee that data will be visible at the receiver after exactly this interval: connectivity, accumulated history, and processing on both sides affect delivery.

**Максимальный шаг (мс)** (maximum step in milliseconds) limits the time interval covered by one batch of history and messages. It does not limit the number of tags or records. **Таймаут (мс)** (timeout in milliseconds) sets the request wait time; the connection timeout uses one tenth of this value.

On the first run, unset history and message processing boundaries are set to the current time. Earlier history is not selected automatically. After a stop, transfer resumes from the saved boundaries. A boundary can also advance through an empty interval with no records.

## Manage the replication channel

### Edit and disable

Open the object from the replication list or through its folder in the project tree. Search by name or path; the filter string must be empty or contain at least three characters. The enabled/disabled filters help locate enabled and disabled objects.

![Replication list and filters](./images/replica-list-compact-ui-4.0.6.subs.png)

*Figure 1 — Replication list and filters. Available test instance: Faceplate Studio 4.0.6.subs.*

Saving changed settings may restart the running object. After a change, check data transfer as well as the state. Canceling an edit closes it without saving the changes.

The **Disabled** checkbox prevents the object from starting. Disabling its parent folder also affects execution. Disabling replication does not control archiving of the source objects: the site archive must keep running when you verify the accumulation of history.

### Copy, move, and delete

Copy the object only into a folder that is already disabled. After **Copy/Paste**, the copy retains the GUID and ordinary settings, while history and message processing boundaries are not copied. Before starting a new pair, assign a new shared GUID and check all addresses and roles.

To move an object, use **Paste** with the **move** operation. Check the destination folder first: moving changes the scope of data exchange. Deleting one or more objects requires confirmation. Deleting a replication object does not delete its associated tags and archives.

The common forms provide **Copy Path**, **Cross Reference**, and **Broken Dependencies** for copying the path, viewing references, and viewing broken dependencies. Verify their availability and labels in the specific form in your installation.

### Processing boundaries and memory

History and message processing boundaries are populated automatically. The numeric fields in the current parameters allow changes, but saving through the forms and the effect on active data exchange have not been verified in this example. Test editing only on a disabled example copy.

The **Memory limit (bytes)** field has a unit mismatch: the label specifies bytes, while the examined implementation treats the number as MiB. A value of **1024** corresponds to 1024 MiB. Confirm the units in your installation before changing the field; the example below does not assign a new numeric value to this limit.

## Transfer pump station data to the control center

This is the guide's single end-to-end scenario. It uses the example objects in the Prerequisites section. Replace all addresses and node names in the tables with your own. The following results are expected from the examined behavior; verify them on your pair of instances.

### Connect the site and center

Configure the center object first, then the site object. This prepares the receiving side before sending starts.

| Field | Site object | Center object |
|---|---|---|
| Имя (name) | StationLink | StationLink |
| GUID | Identifier obtained from the center | Generated pair identifier |
| URL, one list entry | `http://center.example:9000/REPLICA` | `http://center.example:9000/REPLICA` |
| URLS back, one list entry | `http://site.example:9000/REPLICA` | `http://site.example:9000/REPLICA` |
| Receive Nodes, one list entry | `center@center.example` | `center@center.example` |
| Период (мс) (period, ms) | 1000 | 1000 |
| Максимальный шаг (мс) (maximum step, ms) | 60000 | 60000 |
| Таймаут (мс) (timeout, ms) | 30000 | 30000 |
| Disabled | Cleared | Cleared |

![Empty REPLICA form before entering values](./images/replica-empty-form-ui-4.0.6.subs.png)

*Figure 2 — Step 2 — Empty REPLICA form before entering values. The screenshot shows the root folder; select PumpStation for this scenario. Available test instance: Faceplate Studio 4.0.6.subs.*

The identical addresses and nodes in the table define the pair's common directions. Each object's role depends on its local nodes, rather than a different address value in the form.

1. At the center, open the **PumpStation** folder in the project tree.
2. In **Общий вид** (General view), choose to create an object of type **Replica**.
3. Set the name to **StationLink**.
4. Generate a **GUID** using the button next to the field.
5. Complete the remaining fields using the center column in the table.
6. Save the center object.
7. At the site, open the **PumpStation** folder.
8. Create a **Replica** object named **StationLink** in this folder.
9. Complete the fields using the site column, including the center object's GUID.
10. Save the site object.
11. Open the replication list.
12. Check the state, node, and process of both objects.
13. At the site, change the current **Process/Pressure** value to **3 bar**.
14. At the center, open the corresponding **Process/Pressure** object.
15. Verify that its current value is now **3 bar**.

Running objects are expected to show **RUN** with an assigned node and process. Allow several periods for data exchange; if there is no result, use the troubleshooting section. This stage succeeds when the changed value matches at the center. It does not yet confirm that stored history and messages have been transferred.

### Verify history, messages, and write-back

1. In the site object, set **Период (мс)** (period, ms) to **2000**.
2. Set **Максимальный шаг (мс)** (maximum step, ms) to **30000**.
3. Set **Таймаут (мс)** (timeout, ms) to **10000**.
4. Save the changes.
5. Set the same three values in the center object.
6. Save the changes at the center.
7. Record the verification start time using the site's clock.
8. At the site, set **Pressure = 3 bar**.
9. After this value has been stored in the archive, change **Pressure** to **5 bar**.
10. After the next archive record, return **Pressure** to **3 bar**.
11. At the center, open a trend for **PressureArchive** covering the verification interval.
12. Find the points with values of **3, 5, and 3 bar**.
13. Compare their timestamps with the site archive records.
14. In the center's message log, find the message for pressure exceeding **4 bar**.
15. Compare its source, occurrence time, and clearance time with the site's message.
16. At the site, add a test comment to this message.
17. Verify the comment change in the center's message log.
18. At the center, change the current **Setpoint** value from **3** to **3.5 bar**.
19. At the site, verify **Setpoint = 3.5 bar**.
20. At the center, return **Setpoint** to **3 bar**.
21. At the site, verify that it has returned to **3 bar**.

With a 1 s archive recording period, hold each test value for longer than one archive interval. Compare the actual points at the source and receiver; a point missing at the source is not a replication error. Account for time zones when selecting the interval and comparing displayed times.

This stage checks four separate results: current values, stored history, messages, and changes sent back to the site. Acknowledgment transfer is not separately tested here.

### Verify recovery of data exchange

Start with a working pair for which history reception has already been confirmed. Archiving at the site must continue independently of the disabled replication channel.

1. Find **StationLink** in the list by name or path.
2. Check the enabled and disabled object filters.
3. Reset the filters.
4. Refresh the list.
5. Open **Diagnostics** of the site object and click **Start**, see [Diagnostics of Runtime objects](../diagnostics/diagnostics.md).
6. Select **Disabled** in the site object.
7. Save the change.
8. Record the time when replication was disabled.
9. Change **Pressure** at the site so that its archive contains distinguishable records.
10. Verify that these records exist in the site archive.
11. Clear **Disabled** in the site object.
12. Save the change.
13. At the center, check the records for the interval when replication was disabled; the site's messages for this time are in the **Diagnostics** window.

Processing is expected to resume from the saved boundary. Verify the specific values and timestamps at the center: a transition to RUN or an advancing boundary does not replace this check. The time needed to process the accumulated interval depends on its size and the data exchange settings.

Use the same example channel to test a list of fallback addresses. Prepare a working center address and a test address that you can deliberately make unavailable; the list order must be known.

1. In **URL**, enter the unavailable test address first and the working center address second.
2. Save the settings.
3. Change the example pressure at the site.
4. Check this value at the center and inspect the diagnostic records.
5. Restore the working address list.
6. Save the settings.

This checks whether the next address is tried after a failed attempt. The placeholder domain in this guide is not a ready-to-use fallback service; use your working receiver for the test.

### Maintain a disabled example copy

Perform this stage at the site using the operations in Manage the replication channel. Keep the working **PumpStation/StationLink** pair. The **MaintenanceA** and **MaintenanceB** folders must be disabled and outside the working pair's scope.

1. Verify that **MaintenanceA** is disabled.
2. Copy **StationLink** using **Copy**.
3. Insert one copy into **MaintenanceA** using **Paste**.
4. Open the copy's parameters.
5. Verify that its GUID matches the source object's GUID.
6. Generate a new GUID for the copy.
7. Select **Disabled** on the copy itself.
8. Save the copy.
9. Open its current parameters.
10. Enter the example value **1700000000000** milliseconds in the history processing boundary field.
11. Save the change.
12. Reopen the form.
13. Verify the saved value of **1700000000000**.
14. Check the purpose of **Memory limit (bytes)** in the reference below.
15. Copy the duplicated object's path using **Copy Path**, if the action is available in the form.
16. Open **Cross Reference** to view references.
17. Open **Broken Dependencies** to view broken dependencies.
18. Verify that **MaintenanceB** is disabled.
19. Move the copy to **MaintenanceB** using **Paste** with the **move** operation.
20. Check the copy's new path.
21. Delete the example copy and confirm deletion.
22. Refresh the list and verify that the copy is absent.
23. Verify that the working pair and the example tags and archives remain in place.

Editing the boundary on a disabled copy checks only whether the field is saved. It does not confirm that history is transferred again. If the form does not provide the required field or the change is not saved, stop this part of the check; successful saving through both forms has not been confirmed in this working version. The memory limit is not changed at this stage because of the unit mismatch.

## Parameter and state reference

The labels below correspond to the examined forms; verify their translation and location in the running interface. For a typical configuration, enter the identifier, addresses, and nodes, then check the numeric parameters and enabled state.

| Field | Purpose and requirement | Initial value or limitations |
|---|---|---|
| Имя (name) | Required object name within the folder | Entered by the user when creating the object |
| Заголовок (title) | Optional description | May be empty |
| Folder / Pattern | Folder and object type | Displayed information |
| GUID | Required pair identifier | Entered or generated using the button; identical on both sides of one pair |
| URL | List of forward addresses | Entered by the user; multiple entries are tried sequentially |
| URLS back | List of return addresses | Entered by the user; site service address |
| Receive Nodes | List of receiving nodes | Entered by the user; determines the object's role |
| Период (мс) (period, ms) | Data exchange processing cycle | Integer; default 1000; minimum 1000 |
| Максимальный шаг (мс) (maximum step, ms) | Time interval for one batch of history and messages | Integer; default 60000; minimum 1000 |
| Таймаут (мс) (timeout, ms) | Request wait time | Integer; default 30000; minimum 10 |
| Disabled | Prevents the object from starting | Must be cleared for operation |
| Memory limit (bytes) | Inherited memory limit | Value 1024; minimum 10; the bytes label conflicts with processing in MiB |

List validation does not confirm that addresses are correct or nodes exist. Successful saving of empty lists has not been tested on the instance; populate all three lists in the working example configuration.

| State or field | Set by | Interpretation |
|---|---|---|
| State | Faceplate | RUN — the process is running; STOP — stopped; successful data exchange must be checked separately |
| Node | Faceplate | Execution node; no node indicates that no node is assigned |
| PID | Faceplate | Running process; no process indicates that there is no process |
| Error | Faceplate | General text of the latest history or message error; not a complete log of all data flows |
| History processing boundary | Faceplate | Numeric timestamp of the last processed interval; set to the current time on the first run |
| Message processing boundary | Faceplate | Equivalent boundary for messages |

Boundaries are expressed in milliseconds since January 1, 1970, UTC. They describe the processed interval, not the number of received points. The general Error text may be cleared after successful processing of another data flow. Also check diagnostics for errors in current value transfer.

## Troubleshooting

First identify the missing result: a current value, history, a message, or a change sent back to the site. Check data and settings on both sides.

| Symptom or message | Where to check and possible cause | Action | Verify recovery |
|---|---|---|---|
| STOP, no node, no process | Object/folder Disabled setting, folder nodes, and Receive Nodes | Enable the required object/folder and correct the node assignment | A process appears, then the test value is transferred |
| invalid_replica_guid | Pair GUID, role, and whether the other side is running | Align the GUID and make sure the required side is running | A subsequent transfer reaches the corresponding object |
| all_endpoints_failed, no_endpoint, timeout | Address lists, connectivity, and the /REPLICA path | Correct the addresses or restore service availability | The test value and new records appear at the center |
| HTTP 400 or 404 | Service address, channel path, GUID, and role | Check connection details on both sides; read the full error text | Requests succeed and data is stored at the receiver |
| invalid archive in replica packet | Relative path and existence of the center archive | Prepare the corresponding archive | Points from a new verification interval appear in it |
| skip update for undefined item | Matching object and subfolders at the center | Prepare the corresponding object at the same relative path | A new value appears in it |
| unable to send real-time batch | Site diagnostics, forward addresses, and the center process | Restore connectivity or correct the receiving side | A new current value reaches the center |
| unable to initialize data | Center diagnostics, return addresses, and site availability | Correct the return address or restore site operation | The center receives current data; write-back is checked separately |
| unable to save changes: … | Save form; the reason follows the colon | Correct the reported cause | Reopening shows the saved fields |

If RUN is shown but the required data is missing, check the relative paths and the specific data flow. If Error is empty, check diagnostics: successful history processing may clear an error from another flow. An advancing boundary alone does not prove that data has been stored at the receiver.

Working with the **Diagnostics** window is described in [Diagnostics of Runtime objects](../diagnostics/diagnostics.md). Record the verification time, object, source value, and expected result at the receiver to distinguish a replication error from a missing source record.

## Replication limitations

- The entire project configuration is not transferred. Missing tags and archives are not created automatically; the corresponding data may be skipped.
- History and messages flow from the site to the center. Reverse data exchange is described for current fields.
- The examined form has no separate history-only or messages-only modes.
- Multiple URLs provide sequential attempts, not delivery to every address.
- History preceding the first run is not selected automatically. After a stop, resuming depends on the saved boundaries and available source data.
- Messages are selected by their parent folder's message group and their occurrence, clearance, or comment time. Acknowledgment time is not used separately for this selection.
- A successful process state or acceptance response does not guarantee that history and messages have been stored. Confirm completion using data on the receiving side.
