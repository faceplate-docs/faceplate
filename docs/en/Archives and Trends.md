# User Guide: Archives and Trends in Faceplate

## 1. General Information on Archives
In the **Faceplate** editor, the "Archives" subsystem is a tool for storing data coming from external sources (PLC connections, IoT connections, script results, etc.).

Created archives are used by engineers and operators to analyze, control, and monitor production processes based on historical data presented in the form of graphs and reports.

### Archive Characteristics
* **Data Storage:** Saves data for a specified time to analyze historical trends.
* **Compression:** Uses compression methods to save disk space and optimize performance.
* **Search and Access:** Users can search for and access historical data.
* **Security:** Ensures data integrity and protection against unauthorized changes.
* **Cyclicity:** Parameter values are archived cyclically at user-defined time intervals, regardless of the variable's rate of change.
* **Deployment:** Archives can be deployed locally or remotely.

---

## 2. Creating and Configuring Archives

The "Archives" editor allows you to work with archived parameters, configure them, and edit or delete previously created ones. The main panel of the editor displays the archive database with statuses and sources.

Creating new archives or editing existing settings is done using the configuration form.

### Configuration Parameters

| Parameter | Description |
| :--- | :--- |
| **Name** | A unique archive name within the project. Usually related to the content (e.g., "Pressure"). Displayed in the Trends window. |
| **Folder** | The location of the archive within the project structure. |
| **Disabled** | A switch determining whether data is written to the archive in runtime mode. |
| **Depth (days)** | The length of the stored history. Minimum value is 1 day. Changing this parameter affects disk space requirements. |
| **Period (ms)** | Recording frequency. Decreasing the period leads to increased CPU load and required disk space. |
| **Minimum step** | The system writes a new value to the archive only if it differs from the previous one by an amount greater than or equal to this step. Allows ignoring "noise" and reducing load. |
| **Source** | Selection of data source: `tag` (tag value), `script` (script result), or `iot`. |
| **Data type** | • `simple` — basic type for constantly changing parameters.<br>• `categorized` — for object state codes.<br>• `counter` — the difference between previous and current values. |

---

## 3. Using Scripts

A source of type `script` allows defining a script for additional processing of the archived value or forming a value based on multiple input parameters.

### Principle of Operation
1.  The archiving system reads values from the tag fields to which variables are bound.
2.  The script is called with a map of variable values passed as input.
3.  The value returned from the script is saved to the archive database.

### Configuration
In the editor, you select the programming language (**Erlang** or **JavaScript**), enter variables, and select the source of values for them. A compilation function is used to check the correctness of the script. If there are no errors, a confirmation message is displayed.

---

## 4. Configuration Export and Import

The database of archived parameters can be exported to an `.xlsx` format file and imported back. This allows transferring settings between projects (e.g., from a test server to a production one) or using spreadsheet editors for mass changes.

### Export
Exporting generates a file where each row corresponds to one archived parameter.

**Main configuration file fields:**
* Storage location and archive name.
* Archiving period and storage depth.
* Status (enabled/disabled).
* Source type and reference to the tag or script.
* Minimum step and data type.

### Import
When importing a file, the system loads data into the database. In case of data inconsistency (e.g., a specified tag is missing), an error message is displayed indicating the row number and the reason.

---

## 5. Working with Trends (Runtime)

In Runtime mode, the "Trends" tab is used to view graphs of parameters stored in the archive.

### Trend Selection
The selection window consists of two tabs:
1.  **Groups:** Displays previously saved sets of trends for quick access.
2.  **Archives:** Allows searching for parameters and creating new graphs.

### Series Configuration
A series is a separate line on the graph. For each series, you can configure:
* Line color and thickness.
* Visibility and name.
* Path to the data archive.
* Presence of point markers.
* Minimum and maximum display range.

### Display Control
After plotting the graph, the user can:
* Set a precise display period (start/end date and time).
* Select a preset time interval.
* Analyze parameter behavior over various time segments.
* The graph automatically rebuilds when the period changes.

---

## 6. Aggregates

The "Aggregates" module allows creating aggregated functions to perform calculations directly within trends.

### Available Functions
The system implements the following analytics functions:
* **Basic:** Average, Minimum, Maximum.
* **Integral:** Total Integral, Integral of Positive Values, Integral of Negative Values.
* **Statistical:** Standard Deviation, Mean Absolute Deviation.
* **Share/Ratio:** Share of Positive Values, Share of Negative Values, Share of Zeros.
* **Extremes:** Minimum/Maximum Positive and Negative values.

---

## 7. "Trends" Element (Widget)

For mnemonic scheme developers, a **Trends** element is provided, allowing the embedding of a graph into the operator interface.

### Element Properties
The developer can configure the appearance and operator access rights via properties:

* **Grid:** Enable display and configure grid step for time and value axes.
* **Legend:** Configure legend display mode (on mouseover, always, follow cursor, or hidden), as well as fonts and colors.
* **Value:** Binding to a specific archive or group of archives, configuring update frequency.
* **Scale:** Configure time step, period factor, as well as upper and lower scale limits.
* **Toolbar:** Control the visibility of the toolbar in runtime mode. You can selectively block functions for the operator:
    * Trend selection.
    * Setting the time period.
    * Scale configuration.
    * Appearance changes.
    * Data export (printing, saving to CSV/XML).
