# REST API Interface

Based on the IoT module, two functional blocks can be represented: Data Access API – used for integration with external analytics systems (Power BI) and historical retrieval. User API (IoT Server) – created by an engineer via iot_http_server_connection to accept arbitrary requests. A draft of the technical document is presented below. Faceplate:

# 1. General Information

The Faceplate REST API provides an interface for data exchange between the system core (Runtime/Historian) and external clients (BI systems, ERP, mobile applications, web portals). Interaction is based on the Request-Response principle.

Protocol: HTTP / HTTPS
Data format: JSON
Encoding: UTF-8

## 1.1. Base URLThe API address depends on the server configuration and security settings (HTTP/HTTPS):HTTP: http://<Server_IP>:9000/api (Default Port)HTTPS: https://<Server_IP>:9443/api (Note: The port can be changed in the Docker container configuration, see deploy as docker.md).
## 1.2. AuthenticationTo access protected API resources, you must use an authorization token or Basic Auth (depending on the security module settings).Request Header:HTTPAuthorization: Bearer <Your_Access_Token> orHTTPAuthorization: Basic <Base64_Encoded_Credentials>
# 2. History APIThis section describes the standard mechanism for retrieving aggregated data used for integration with Microsoft Power BI and other analytics platforms.2.1. Getting Historical TrendsEndpoint: /history/read (Approximate path, requires clarification in the specific project configuration)Method: POSTThe request retrieves a selection of values ​​for a list of tags for a specified time period.Request Body (Request Payload):The client sends a JSON object with filtering parameters:

```JSON
{
  "tags": [
  "StationA.Pump1.Pressure",
  "StationA.Pump1.Flow"
  ],
  "startTime": 1769281200000,
  "endTime": 1769284800000,
  "aggregation": "1m"
}
``

tags: Array of tag IDs or their names in the system.startTime
endTime: Timestamps in Unix Timestamp format (ms).
aggregation: (Optional) Aggregation period (e.g., "1m", "1h"). If not specified, raw data is returned. Server Response: The server returns an array of objects with timestamps and values.

```JSON
[
  {
    "tag": "StationA.Pump1.Pressure",
    "data": [
              [1769281200000, 24.5, 192],
              [1769281260000, 24.8, 192]
    ]
  }
]
```

Data array element structure (see powerbi_en.md):
Timestamp: Time (Unix ms).Value: Value.
Quality: Signal quality code (192 = Good).

# 3. Custom API (IoT Module)Faceplate allows you to create custom API endpoints through the IoT Connections module. This allows you to flexibly customize the logic for processing incoming requests.
## 3.1. Server Configuration: To enable data reception, you must create an iot_http_server_connection object. 
Parameter: Description: 
Example: Host: Listening Interface: 0.0.0.0 (all interfaces) Port: Listening Port: 8081 Path (Endpoint): Resource Path: /api/v1/custom_data
## 3.2. Request Processing (Scripting) The request response logic is programmed using iot_script. When a request is received, the script receives the request object and must generate a response. Example processing script (Erlang/Script): Accepts JSON, checks the "cmd" field, and writes the value to the tag. Erlang% Input data: Message (contains the request body) RequestData = json:decode(Message),

```erlang
Result = case maps:get("cmd", RequestData) of
  "set_setpoint" ->
    Val = maps:get("value", RequestData),
    faceplate:write_tag("Tag_Setpoint", Val),
    #{status => "ok", written => Val};
  _ ->
    #{status => "error", reason => "unknown command"}
  end,

Response = json:encode(Result).
```

# 4. HTTP Status Codes: Standard response codes are used when working with the API:

200 OK — The request was successful.
204 No Content — Successful, but no data was returned (often used when writing to InfluxDB/IoT).
400 Bad Request — Error in request syntax (invalid JSON, missing required fields).
401 Unauthorized — Authentication error (invalid token).
500 Internal Server Error — Internal Faceplate server error.

# 5. Integration Recommendations: Time Zones:

Faceplate processes requests using the server's time zone. It is recommended to transmit and receive time in UTC (Unix Timestamp) format to avoid drift. Batch Transfer:
- When requesting large volumes of historical data (e.g., for Power BI), avoid queries for periods longer than 30 days with raw granularity. Use aggregation (hourly/daily average).
- Security: When using iot_http_server_connection on public networks, be sure to configure SSL certificates (Key and Certificate fields in the connection settings).