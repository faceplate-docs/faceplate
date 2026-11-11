Faceplate

Integration with Microsoft Power BI

# Introduction

Faceplate/EMS integration with Power BI transforms raw process SCADA data into management analytics. It's based on the request-response principle: Power BI acts as a client, retrieving data from an industrial database via an HTTP gateway.

Solution Architecture

- **Source (Faceplate/EMS):** Stores tag archives (pressure, temperature, energy consumption). The Faceplate server provides an API (REST) ​​that accepts external requests.
- **Transport (HTTP API):** Data exchange layer. Power BI sends an HTTP request containing parameter IDs and a time interval, and the server returns data (usually in JSON format).
- **Processing (Power Query):** Within Power BI Desktop, parsing of the JSON response, data type conversion, and "unfolding" lists into flat tables occurs.

Key Benefits

- **Server-side aggregation:** Instead of transferring millions of rows of raw data, you can request averaged values ​​(minute or hourly), dramatically speeding up reporting.
- **Single window:** Ability to combine SCADA data with ERP data (e.g., 1C or SAP) to calculate cost or resource consumption.
- **Automation:** Once configured, the data model can be updated with the click of a button or according to a schedule in the Power BI Service.

# Configuring the REST API server in Faceplate

## Creating an HTTP server object

For Faceplate to "listen" to Power BI, you need to create an object based on the iot_http_server_connection system template.

Basic connection settings:

- Endpoint /api/data : The URL where the API will be accessible
- Method : POST : The request type for passing parameters in the body
- State : RUN : The server status must be "ENABLED"

## Processing Modes

### Request Response

You will need to configure request processing using the JSON processing mode with the following schema:

```json
{
"from": \$from,
"to": \$to,
"archive": \$archives,
"step": \$step
}
```

\$from, \$to, \$archives, \$step - variables for passing values ​​to Faceplate variables.

Power BI will generate and send a JSON object in the request body. Here's what should be inside:

- **from / to**: Dates in YYYY-MM-DDTHH:mm:ss.SSS+TZ format (e.g., 2026-01-16T00:00:00.000+5).
- **archive**: Array of full paths to archives (e.g., /root/FP/PROJECT/block-A/pump-1/flow/archives/out_value).
- **step**: Aggregation step in seconds. For daily analysis, use 3600 (1 hour), for monthly analysis, use 86400 (1 day).

### Response

To process the response, you will need to configure the response logic in the Response field. To do this, select script processing (Note: The example uses Erlang code). The script accepts JSON with time boundaries and a list of archives, parses the dates, and returns a ready-made data set.

Code snippet:

```erlang
archive_handler:get_json(#{
"from" => fp_util:parse_dt(From),
"to" => fp_util:parse_dt(To),
"archive" => Archive,
"step" => Step
})
```

The fp_util:parse_dt() function is a function of the built-in Faceplate **fp_util** module. It is required for correctly converting the ISO 8601 date string to the system's internal format.

The archive_handler:get_json() function is a handler for retrieving data from an archive and converting it to JSON.

## Testing the Faceplate Server REST API

After completing the server configuration, the prepared API can be tested using the **cURL** command.

Example request:

```bash
curl --location '<http://192.168.20.200:7080/api/data>'
\--header 'Content-Type: application/json'
\--data '{"from": "2026-01-28T00:00:00.000+5","to": "2026-01-29T00:00:00.000+5","archive": \[ "/root/FP/PROJECT/block-A/pump-1/flow/archives/out_value", "/root/FP/PROJECT/block-A/pump-1/pressure/archives/out_value"\],"step": 3600}'
```

# Setting up Power BI Desktop

To retrieve data, you need to use **Power Query**.

- Create a **Blank Query** (**Get Data** → **Blank Query**).
- Open the **Advanced Editor**.
- Paste the Power Query script (M-language) from the example below.

## Example Power Query Script

This script retrieves data from a single archive. Ideal for monitoring a single parameter (e.g., the flow rate of a single pump).

Script body (m-script):

```m
let
// === REQUEST PARAMETERS ===
DateFrom = "2026-01-28T00:00:00.000+5",
DateTo = "2026-01-29T23:59:59.000+5",
ArchivePath = "/root/FP/PROJECT/block-A/pump-1/flow/archives/out_value",
StepSeconds = 3600,
ApiUrl = "<http://192.168.20.200:7080/api/data>",
<br/>// === FORMING THE REQUEST ===
body = Text.ToBinary("{
""from"": """ & DateFrom & """,
""to"": """ & DateTo & """,
""archive"": \[""" & ArchivePath & """\],
""step"": " & Number.ToText(StepSeconds) & "
}"),
<br/>// === SENDING REQUEST ===
response = Web.Contents(ApiUrl, \[
Headers = \[#"Content-Type"="application/json"\],
Content = body
\]),
<br/>// === PROCESSING RESPONSE ===
json = Json.Document(response),
archiveData = Record.Field(json, ArchivePath),
<br/>// === CONVERT TO TABLE ===
toTable = Table.FromList(archiveData, Splitter.SplitByNothing()),
<br/>addTimestamp = Table.AddColumn(toTable, "Timestamp", each
if \[Column1\] is list and List.Count(\[Column1\]) > 0 then \[Column1\]{0} else null
),
<br/>addValue = Table.AddColumn(addTimestamp, "Value", each
if \[Column1\] is list and List.Count(\[Column1\]) > 1 then \[Column1\]{1} else null
),
<br/>removeColumn = Table.RemoveColumns(addValue, {"Column1"}),
<br/>// === FILTERING NULL VALUES ===
filtered = Table.SelectRows(removeColumn, each \[Value\] <> null),
<br/>// === CONVERTING TIMESTAMP TO DATETIME ===
addDateTime = Table.AddColumn(filtered, "DateTime", each
# datetime(1970,1,1,0,0,0) + #duration(0,0,0,\[Timestamp\]/1000),
type datetime
),
<br/>// === SETTING DATA TYPES ===
setTypes = Table.TransformColumnTypes(addDateTime, {
{"Timestamp", Int64.Type},
{"Value", type number}
}),
<br/>// === REORDERING COLUMNS ===
reordered = Table.ReorderColumns(setTypes, {"DateTime", "Timestamp", "Value"})
in
reordered

| DateTime | Timestamp | Value |
| --- | --- | --- |
| 2026-01-28 01:00:00 | 1769281200000 | 0.332 |
| --- | --- | --- |
| 2026-01-28 02:00:00 | 1769284800000 | 0.954 |
| --- | --- | --- |
```

# Helpful Tips

- **Time Zones**: Remember that Faceplate uses the server's time zone when processing requests.
- **Date Format**: Power BI is very picky about formatting. Always use two-digit values ​​for hours (write 00, not 0).
- **Null Values**: If there is no data for a given period, the API will return null. The suggested scripts already have built-in filtering for such strings so they don't ruin your charts.
- **Faceplate Array Element Structure**: Each array element is an array of 3 elements: \[timestamp, value, quality\]. In this example, the **quality** metric was deliberately omitted.

# External Sources

[PowerBI Desktop](https://www.microsoft.com/en-us/power-platform/products/power-bi/desktop?market=en) is a free Windows application designed for deep data analysis and creating professional interactive reports. It serves as the primary development tool in the Microsoft Power BI ecosystem.