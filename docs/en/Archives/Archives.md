# Archives

In Faceplate, the **Archives** module is a subsystem for storing time-stamped data.

Most often, this data comes from external sources, such as field equipment, PLCs, or integrated information systems. Also, data to be archived can be generated internally within the system, for example, as a result of intermediate calculations by script modules, forecasting modules, etc. A simple example of an archive is the archiving of temperature sensor readings read from a PLC via the Modbus protocol.

## Purpose

Archives can be effectively used by engineers and operators to analyze, control, and monitor production processes. Users can analyze archived data in the form of graphs and reports.

Faceplate has a developed system for displaying archived data in the form of graphs. For the end-user, it is enough to simply select the archived points, and they will be displayed as graphs for the specified period. The user can scroll through them, set a new period, request aggregates, or export the data, for example, to Excel or XML.

(You can read more about working with trends in the Trends section).

Parallel to the advanced graphical interfaces, Faceplate provides an API for working with archived data. The provided API can be used for:

* Writing archives
* Deleting individual archives for a specified period
* Retrieving values for individual archives for a requested period
* Retrieving values for individual archives at specified moments in time
* Retrieving aggregated values for individual archives for specified periods

The "Archives" editor allows you to work with archived parameters, configure archiving settings, and edit or delete previously created ones. Most often, values are archived with a cycle specified in the archive settings.

### Archive in Faceplate

Creating new archives or editing the settings of existing ones is performed using the form:

![first](/images/1.png)
![PLC folder1](images/1.png)
![common](images/1.png)

**The following table describes the fields:**

| Element | Description |
| :--- | :--- |
| **Folder** | This field indicates the location of the archive. |
| **Pattern** | Object pattern. |
| **Name** | In this field, you need to write the name of the archive. It is usually recommended to give names related to the content of the archive (e.g., "Well Pressure"). During operation, the archive name will be reflected in the Trends window. The operator should understand from the archive name which graph they are working with. The name must be unique within the context of the folder containing the archive. |
| **Title** | A short text description of the archived value. |
| **State** | Current state of the archiving process: `RUN` or `STOP`. |
| **Node** | Indicates on which server the archiving process is running (relevant in a multi-server architecture). |
| **PID** | Unique process identifier. |
| **Disabled** | This switch allows you to determine the archive state (enabled/disabled), i.e., whether data is being written to the archive or not. This setting allows you to disable parameter archiving in runtime mode. |
| **Error** | In case of any errors related to the archive, the "Error" column will be populated. |
| **Memory limit (bytes)** | Memory limit in bytes. If the process requires more memory than the set limit, for example due to a memory leak in a user script, the system will automatically restart the process. |
| **ID** | System identifier of the archive, filled in automatically (service information). |
| **Source** | Data for storage in the archive can be obtained from 2 types of sources:<br>1. **tag** - the value of a tag field acts as the archived parameter.<br>2. **script** - allows you to define a script that can be used for additional processing of the archived value or forming the archive value from several input parameters. For example, the average value of several measurement points can be stored in the archive.<br><br>Also, data can be written to the archive via the corresponding API. |
| **Period (ms)** | In this field, you need to set the cycle (frequency) of recording the selected data values to the archive. The minimum value is 10 ms, the maximum value is 3600000 ms.<br>**ATTENTION!** Changing this parameter can significantly affect the hardware requirements of the Faceplate server. Reducing this parameter leads to an increase in the load on the storage system, as well as the amount of disk space required to store archives. |
| **Minimum step** | This field allows you to set the minimum difference in value between the previous and current parameter values. This means that the system will write a new value to the archive only if it differs from the previous one by an amount greater than or equal to the minimum step value.<br>For example, if interference is observed in the measurement channel, in some cases it is acceptable to set the minimum change step equal to the average amplitude of the interference. This will allow the archive to reflect only the stable trend of parameter changes, disregarding short-term insignificant deviations. Setting this parameter can rid the data of noise and reduce load. |

The **Runtime** tab indicates the current state of the archive.

![](/images/2.png)

**The following table describes the fields:**

| Element | Description |
| :--- | :--- |
| **Quality** | Quality code of the archived parameter (if used). |
| **Ts** | Custom timestamp. For example, if the archived parameter has a timestamp defined by the source, the value will be written with it. |
| **Value** | The last recorded value. |

---

## Typical Example of Working with an Archive

In this example, we consider the case of receiving data from an OPC server, subsequently archiving each received value in Faceplate archives, and displaying them in trends.

### Getting Started

Launch an OPC UA server with tags that will simulate temperature and pressure sensor values. For this example, **KEPServerEX 6** was used.

![](/images/3.png)

The `Temperature` tag is configured so that values change along a sine wave from 0 to 150, and `Pressure` receives random values from 0 to 10. Both tags have the `Float` variable type.

For simplicity in this example, the OPC UA server is configured to allow anonymous connections.

![](/images/4.png)

In Faceplate, create an OPC UA client connection to this server. To do this, in the **General View**, click the "Create" button. In the menu that opens, select `plc_opcua_client_connection` and click "Ok".

![](/images/5.png)

The OPC UA client connection configuration form will open. In this form:
1.  Set the **Name**.
2.  Disable **Secure connection**.
3.  In the **URL** field, specify the connection string to the server.

To do this, you can use the function to search for available servers. Clicking the search button opens a form where you need to specify the address (IP or Domain Name) of the server and the port on which the OPC UA server process is running.

Next, click search, after which a list of points available for connection will be displayed below.

![](/images/6.png)

Select one of them (in our example, we used `opc.tcp://`) and click "Ok".
(You can read more about configuring OPC UA connections in the OPC UA Client section).

![](/images/7.png)

After clicking "save", the OPC UA server connection object will appear in the project structure.
Next, we need to enter this object (double-click on the object) and create bindings to the server tags.

Enter the connection object and click the "Create" button - a form opens for configuring binding parameters to an OPC UA server tag.

![](/images/8.png)

Set "Pressure" as the binding name. To select an OPC UA tag, click on the search button.
A window opens containing the entire tag tree of the OPC UA server. Select the required tag and click "Ok".

![](/images/9.png)

By clicking on the search icon in the **Type** section, Faceplate will automatically detect the data type of the selected tag.

![](/images/10.png)

Repeat the actions for the "Temperature" tag.

![](/images/11.png)

The result will be the following structure:

![](/images/12.png)

Now let's create 2 **ARCHIVE** objects that will write the received values to the archive.

Go back to the root folder and click the "Create" button; the object creation window will open.
Here, in the "system" folder, select "ARCHIVE" and click "Ok".

![](/images/13.png)

Next, the editing menu for the created archive will open. Fill in the required **Name** field and the **tag** field.
In the "tag" section, using the search, select the binding to "Pressure".

![](/images/14.png)

In the field selection, choose the field - "value".

![](/images/15.png)

Let's create a second archive that will receive values from "Pressure" and "Temperature" and record a system load index to the archive.
This functionality will be implemented using the **"script"** source, with a binding to the "value" fields of the two tags "Pressure" and "Temperature". We will choose **Erlang** as the programming language.

![](/images/16.png)

To compile the script, click the "Compile" button.
If the compilation is successful without errors, "ok" will appear next to the compilation button; otherwise, a list of errors will be displayed, for example:

![](/images/17.png)

**General principle of operation:**
The archiving system reads values from the tag fields to which the declared variables are bound with a specified cyclicity, calls the script passing a map with the variable values as input, and the value obtained at the script output is saved to the database with the current server timestamp.

To check the operation of the archives, let's launch the runtime. To do this, click the "Start Runtime" button in the top panel.
After that, go to the runtime page; to do this, open "Runtime" in the side menu.

![](/images/18.png)

Next, enter the runtime page, open **Trends** from the side menu, and add series with our archives.

![](/images/19.png)

To do this, in the "Trend Selection" window, go to the **Archive** section. Here you need to set the group name and series name.

![](/images/20.png)

After naming the series, you can specify the path to the archive (settings button - gear icon).

![](/images/21.png)

Clicking the search button allows us to select any previously created archive.

![](/images/22.png)

After selection, the path is saved, and the series is ready for display.

![](/images/23.png)

By default, the trend updates automatically with a cycle of once per second. You can stop the update by clicking the pause button.
To select the depth of data display, click the trend depth setting button (by default, it is "minute X 10").
In the dialog that opens, select a new value.

![](/images/24.png)

![](/images/25.png)

To view data for a past period, stop the trend update and click on the button displaying the current period (in our case, it is "05:20:00 => 05:25:00"). In the dialog that opens, select the period of interest:

![](/images/26.png)

![](/images/27.png)

To export data to Excel, click the button:

![](/images/28.png)

on the toolbar. In the opened form:
1.  Select the Excel format (`.xlsx`).
2.  Adjust the period and step if necessary.
3.  Select the data aggregation function for the step, for example, `avg`.
4.  Click OK.

![](/images/29.png)
