# Faceplate

## Integration with Microsoft Power BI

[Introduction](#introduction)

[Configuring REST API Server in Faceplate](#configuring-rest-api-server-in-faceplate)

[Creating an HTTP Server Object](#creating-an-http-server-object)

[Processing Modes](#processing-modes)

[Request Processing (Request)](#request-processing-request)

[Request Response (Response)](#request-response-response)

[Testing Faceplate REST API Server](#testing-faceplate-rest-api-server)

[Configuring Power BI Desktop](#configuring-power-bi-desktop)

[Power Query Script Example](#power-query-script-example)

[Useful Tips](#useful-tips)

[External Sources](#external-sources)

# **Introduction** {#introduction}

Integration of Faceplate/EMS with Power BI transforms raw SCADA technological data into management analytics. The foundation is based on the "request-response" principle: Power BI acts as a client that retrieves data from the industrial database through an HTTP gateway.

![Integration sheme](./images/img_1.png)

### Solution Architecture

1. **Source (Faceplate/EMS):** Stores tag archives (pressure, temperature, energy consumption). The Faceplate server provides an API interface (REST) that accepts external requests.
2. **Transport (HTTP API):** Data exchange layer. Power BI sends an HTTP request containing parameter IDs and time interval, and the server returns data (typically in JSON format).
3. **Processing (Power Query):** Inside Power BI Desktop, JSON response parsing occurs, data type conversion, and "expanding" lists into flat tables.

Key Advantages

* **Server-side Aggregation:** Instead of transferring millions of raw data rows, you can request already averaged values (minute-by-minute, hourly), which critically accelerates report performance.
* **Single Window:** Ability to combine SCADA data with ERP data (e.g., 1C or SAP) for calculating cost price or specific resource consumption.
* **Automation:** A once-configured data model will refresh with a single button click or on schedule in Power BI Service.

---

# **Configuring REST API Server in Faceplate** {#configuring-rest-api-server-in-faceplate}

## Creating an HTTP Server Object {#creating-an-http-server-object}

For Faceplate to "hear" Power BI, you need to create an object based on the system template `iot_http_server_connection`.

Main connection settings:

1. **Endpoint:** `/api/data` - URL address where the API will be accessible
2. **Method:** `POST` - Request type for passing parameters in the body
3. **State:** `RUN` - Server status must be "ON"

## Processing Modes {#processing-modes}

### **Request Processing (Request)** {#request-processing-request}

You will need to configure request processing through JSON processing mode with the following schema:

```json
{      
    "from": $from,      
    "to": $to,      
    "archive": $archives,      
    "step": $step      
}
```

`$from`, `$to`, `$archives`, `$step` - variables for passing values to Faceplate variables.

Power BI will form and send a JSON object in the request body. Here's what should be inside:

* **from / to:** Dates in format `YYYY-MM-DDTHH:mm:ss.SSS+TZ` (e.g., `2026-01-16T00:00:00.000+5`).
* **archive:** Array of full paths to archives (e.g., `/root/FP/PROJECT/block-A/pump-1/flow/archives/out_value`).
* **step:** Aggregation step in seconds. For daily analysis use `3600` (1 hour), for monthly — `86400` (1 day).

### **Request Response (Response)** {#request-response-response}

For response processing, you will need to configure response logic in the Response field. To do this, you must select script processing (Warning! The example uses Erlang code). The script accepts JSON with time boundaries and archive list, parses dates, and returns a ready dataset.

Code fragment:

```erlang
archive_handler:get_json(#{
    "from" => fp_util:parse_dt(From),
    "to" => fp_util:parse_dt(To), 
    "archive" => Archive, 
    "step" => Step 
})
```

The `fp_util:parse_dt()` function is a function of the Faceplate built-in module **fp_util**, it is necessary for correct conversion of the date string from ISO 8601 to the system's internal format.

The `archive_handler:get_json()` function is a handler for retrieving data from archive and converting to JSON.

## Testing Faceplate REST API Server {#testing-faceplate-rest-api-server}

After completing server-side configuration, the prepared API can be tested via **cURL** command.

Request example:

```bash
curl --location 'http://192.168.20.200:7080/api/data' \
    --header 'Content-Type: application/json' \
    --data '{
        "from": "2026-01-28T00:00:00.000+5",
        "to": "2026-01-29T00:00:00.000+5",
        "archive": [
            "/root/FP/PROJECT/block-A/pump-1/flow/archives/out_value",
            "/root/FP/PROJECT/block-A/pump-1/pressure/archives/out_value"
        ],
        "step": 3600
    }'
```

# **Configuring Power BI Desktop** {#configuring-power-bi-desktop}

To retrieve data, you need to use **Power Query**.

1. Create a **Blank Query** (**Get Data** → **Blank Query**).
2. Open **Advanced Editor** (**Advanced Editor**).
3. Paste the Power Query script (M-language) from the example below.

## Power Query Script Example {#power-query-script-example}

Script for retrieving data from a single archive. Ideal for monitoring a single parameter (e.g., flow rate of one pump).

Script body (M-script):

```powerquery
let     
    // === REQUEST PARAMETERS ===     
    DateFrom = "2026-01-28T00:00:00.000+5",     
    DateTo = "2026-01-29T23:59:59.000+5",     
    ArchivePath = "/root/FP/PROJECT/block-A/pump-1/flow/archives/out_value",     
    StepSeconds = 3600,     
    ApiUrl = "http://192.168.20.200:7080/api/data",     
         
    // === REQUEST FORMATION ===     
    body = Text.ToBinary("{     
        ""from"": """ & DateFrom & """,     
        ""to"": """ & DateTo & """,     
        ""archive"": [""" & ArchivePath & """],     
        ""step"": " & Number.ToText(StepSeconds) & "     
    }"),     
         
    // === SENDING REQUEST ===     
    response = Web.Contents(ApiUrl, [     
        Headers = [#"Content-Type"="application/json"],     
        Content = body     
    ]),     
         
    // === RESPONSE PROCESSING ===     
    json = Json.Document(response),     
    archiveData = Record.Field(json, ArchivePath),     
         
    // === CONVERTING TO TABLE ===     
    toTable = Table.FromList(archiveData, Splitter.SplitByNothing()),     
         
    addTimestamp = Table.AddColumn(toTable, "Timestamp", each      
        if [Column1] is list and List.Count([Column1]) > 0 then [Column1]{0} else null     
    ),     
         
    addValue = Table.AddColumn(addTimestamp, "Value", each      
        if [Column1] is list and List.Count([Column1]) > 1 then [Column1]{1} else null     
    ),     
         
    removeColumn = Table.RemoveColumns(addValue, {"Column1"}),     
         
    // === FILTERING NULL VALUES ===     
    filtered = Table.SelectRows(removeColumn, each [Value] <> null),     
         
    // === CONVERTING TIMESTAMP TO DATETIME ===     
    addDateTime = Table.AddColumn(filtered, "DateTime", each      
        #datetime(1970,1,1,0,0,0) + #duration(0,0,0,[Timestamp]/1000),     
        type datetime     
    ),     
         
    // === SETTING DATA TYPES ===     
    setTypes = Table.TransformColumnTypes(addDateTime, {     
        {"Timestamp", Int64.Type},     
        {"Value", type number}     
    }),     
         
    // === REORDERING COLUMNS ===     
    reordered = Table.ReorderColumns(setTypes, {"DateTime", "Timestamp", "Value"})     
in     
    reordered
```

**Result:**

| DateTime | Timestamp | Value |
|:---------|:----------|:------|
| 28.01.2026 01:00:00 | 1769281200000 | 0.332 |
| 28.01.2026 02:00:00 | 1769284800000 | 0.954 |

# **Useful Tips** {#useful-tips}

* **Time Zones**: Remember that Faceplate uses the server's time zone when processing requests.

* **Date Format**: Power BI is very sensitive to format. Always use two-digit values for hours (write 00, not 0).

* **Null Values**: If there is no data for a certain period, the API will return null. The provided scripts already include filtering of such rows so they don't corrupt your charts.

* **Faceplate Array Element Structure:** Each array element is an array of 3 elements: `[timestamp, value, quality]`. In the example, the **quality** metric was deliberately omitted.

# **External Sources** {#external-sources}


[PowerBI Desktop](https://www.microsoft.com/ru-ru/power-platform/products/power-bi/desktop?market=ru) is a free Windows application designed for deep data analysis and creating professional interactive reports. It serves as the primary development tool in the Microsoft Power BI ecosystem.

### written by Marlen Meimanov
