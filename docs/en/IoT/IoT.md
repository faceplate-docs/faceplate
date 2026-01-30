Faceplate

IoT Connections Module

# 

[**Table of Contents**	2](#heading=)

[**1\. Introduction and General Principles	3**](#1.-introduction-and-general-principles)

[1.1. Purpose of the IoT Module	3](#1.1.-purpose-of-the-iot-module)

[1.2. Unified Data Binding Mechanism	3](#1.2.-unified-data-binding-mechanism)

[1.2.1. Configuration Table Structure	3](#1.2.1.-configuration-table-structure)

[1.2.2. Data Flow Directions	3](#1.2.2.-data-flow-directions)

[1.2.3. Operating Features	4](#1.2.3.-operating-features)

[1.3. Universal Components	4](#1.3.-universal-components)

[1.3.1. Programmable Scripts (iot\_script)	5](#1.3.1.-programmable-scripts-\(iot_script\))

[1.3.2. Direct Binding (iot\_tag)	5](#1.3.2.-direct-binding-\(iot_tag\))

[1.3.3. Event Handling (iot\_eventlog)	5](#1.3.3.-event-handling-\(iot_eventlog\))

[1.3.4. Historical Data (iot\_ts)	5](#1.3.4.-historical-data-\(iot_ts\))

[1.4. Status Panel	6](#1.4.-status-panel)

[1.5 Request Triggering Mechanism (Triggers Tab)	6](#1.5-request-triggering-mechanism-\(triggers-tab\))

[1.5.1 Main Trigger Types	6](#1.5.1-main-trigger-types)

[**2\. Transport Protocols (Connection Settings)	8**](#2.-transport-protocols-\(connection-settings\))

[2.1. HTTP (HyperText Transfer Protocol)	8](#2.1.-http-\(hypertext-transfer-protocol\))

[2.1.1. Client (iot\_http\_client\_connection)	8](#2.1.1.-client-\(iot_http_client_connection\))

[2.1.2. Server (iot\_http\_server\_connection)	8](#2.1.2.-server-\(iot_http_server_connection\))

[2.2. MQTT	9](#2.2.-mqtt)

[2.2.2. Publisher (iot\_mqtt\_publisher)	9](#2.2.2.-publisher-\(iot_mqtt_publisher\))

[2.2.3. Subscriber (iot\_mqtt\_subscriber)	10](#2.2.3.-subscriber-\(iot_mqtt_subscriber\))

[2.3. WebSocket	10](#2.3.-websocket)

[2.3.1. Client (iot\_websocket\_client\_connection)	10](#2.3.1.-client-\(iot_websocket_client_connection\))

[2.3.2. Server (iot\_websocket\_server\_connection)	11](#2.3.2.-server-\(iot_websocket_server_connection\))

# 

# **1\. Introduction and General Principles** {#1.-introduction-and-general-principles}

## **1.1. Purpose of the IoT Module** {#1.1.-purpose-of-the-iot-module}

The IoT (Internet of Things) module is designed for data exchange with systems supporting HTTP, MQTT, and WEBSOCKET protocols.
![List of available IoT connections](./images/iot_1.png)
## **1.2. Unified Data Binding Mechanism** {#1.2.-unified-data-binding-mechanism}

The Bindings mechanism is a fundamental tool of the IoT module, designed to establish connections between internal tags of the Faceplate system and variables used in exchange protocols (HTTP, MQTT, WebSocket).

### **1.2.1. Configuration Table Structure** {#1.2.1.-configuration-table-structure}

A unified table with the following key columns is used for configuring the connection:

* **Variable:** Local variable name that will be used in the payload or processing scripts.  
* **Tag (System Tag):** Path to the tag in the Faceplate system object tree from which the value is read or to which the value is written.  
* **Field (Tag Attribute):** Specifies which tag parameter is used for exchange:  
  * `value` — current tag value (most frequently used parameter);  
  * `ts` — timestamp of the last update;  
  * `status` — data quality or validity status.

### **1.2.2. Data Flow Directions** {#1.2.2.-data-flow-directions}

The mechanism's operation logic depends on the component's role in the data exchange chain:

**A. Outgoing Flow (Source / Response)** In `source` type components (for example, when preparing data for sending via MQTT or in an HTTP request), the process follows this scheme:

1. The system reads the value from the specified **Tag**.  
2. The value is assigned to the local **Variable**.  
3. The variable is passed to the script or directly to the data packager to form the message (Payload).  
   The processing mode determines how the incoming request is handled:

* **Const:** Static message (for example, "OK").  
* **JSON:** Automatic JSON response formation with variable value substitution.  
* **Script:** Programmatic formation of the request body. The script body receives variables and returns a map:    
  * Response: A response received from the server.  
    * Context: A map that contains variables and other data.

  **B. Incoming Flow (Action / Request)** In `action` type components (for example, when receiving a response from the server or subscribing to a topic), the process occurs in reverse order:

1. Received external data is parsed into **Variable** variables.  
2. The mapping mechanism finds the corresponding **Tag** in the table.  
3. The value from the variable is written to the Faceplate system tag, taking into account the selected field (**Field**).  
   The processing mode determines how the outgoing request is formed:

* **Const:** Static message (for example, "OK").  
* **JSON:** Automatic JSON response formation with variable value substitution.  
* **Script:** Programmatic formation of the request body. The script body receives variables and returns a serialized string:    
  * Data: A map that contains request data.   
    * Context: A map that contains variables and other data.

### **1.2.3. Operating Features** {#1.2.3.-operating-features}

* **Synchronization:** Data binding ensures real-time value updates.  
* **Type Casting:** The system automatically attempts to cast data types (for example, converts a string number from JSON to the `float` format of a system tag) if provided by settings.  
* **Scalability:** The table allows configuring an unlimited number of connections for a single connection.

## **1.3. Universal Components** {#1.3.-universal-components}

These components are responsible for data transformation, filtering, and translation between module components and internal Faceplate subsystems.
![Data flow directions](/IoT/images/iot_0.png)

### **1.3.1. Programmable Scripts (iot\_script)** {#1.3.1.-programmable-scripts-(iot_script)}

Used for implementing complex transformation logic when standard JSON mapping is insufficient.

**iot\_script\_source (Data Generation):** Executed immediately before sending a packet. The script (JS/Erlang) receives tag values and forms the final string or binary block (Payload) from them.

**iot\_script\_action (Data Processing):** Executed immediately after receiving data from the network. The script parses "raw" data, performs calculations or condition checks, and returns a map of values to write to tags.

### **1.3.2. Direct Binding (iot\_tag)** {#1.3.2.-direct-binding-(iot_tag)}

Designed for simple "one-to-one" exchange scenarios without intermediate logic.

* **iot\_tag\_source:** Reads the current tag value and sends it to the external system in its original form. Optimal for transmitting numeric values and simple strings.  
![iot_tag_source](/IoT/images/iot_4.png)

* **iot\_tag\_action:** Receives data from the external system and writes it directly to the specified system tag without additional processing. Supports atomic value updates.

### **1.3.3. Event Handling (iot\_eventlog)** {#1.3.3.-event-handling-(iot_eventlog)}

Provides integration with the Faceplate event logging subsystem. Used for:

* **iot\_eventlog\_source:** Generating notifications about changes in system tag status (alarms, warnings, system events). Allows packaging complex structures describing the event (severity, timestamp, source, and message body) into the outgoing payload.  
* **iot\_eventlog\_action:** Analyzing incoming messages from the network and converting them into standard event system events. Supports configurable routing and filtering by message type.

### **1.3.4. Historical Data (iot\_ts)** {#1.3.4.-historical-data-(iot_ts)}

Allows interaction with the time series archiving subsystem. Used for loading and uploading historical values of system tags at specified time intervals:

* **iot\_ts\_source:** Extraction of historical tag data (min/max/avg values over a period) for transmission to external analytical or SCADA systems.  
* **iot\_ts\_action:** Reception of historical data batches from external systems and their storage in the Faceplate internal archive. Supports data interpolation and filtering to eliminate anomalies.

## **1.4. Status Panel** {#1.4.-status-panel}

Located in the upper right corner of each component interface.

**State (Status):** Reflects the current state of the connection:

* `Running` — Active and functioning connection.  
* `Error` — Connection lost or configuration error (for example, unreachable network node or authorization failure).  
* `Idle` — Awaiting the first data transmission or in passive listening mode.

**Log:** A button for viewing the operation journal of this component (useful for debugging).

**Config:** Opens the component configuration panel.

**Delete:** Removes the current component from the system (warning: non-recoverable operation).
![Status Panel](/IoT/images/iot_3.png)

## **1.5 Request Triggering Mechanism (Triggers Tab)** {#1.5-request-triggering-mechanism-(triggers-tab)}

The Triggers subsystem controls **when** and **under what conditions** the system generates and sends data packets. Triggers can operate in various modes: periodic, on condition, on change, or in response to external events.

### **1.5.1 Main Trigger Types** {#1.5.1-main-trigger-types}

**On tag change (Change Trigger):** Generates a packet when the specified system tag value changes. This may be a single tag or a group of tags, each having a change detection threshold (delta).

**Periodic Trigger:** Sends messages at fixed intervals (for example, every 5 seconds or once per minute). Often used for telemetry data.

**On condition (Condition Trigger):** Works on conditional logic — evaluates the expression (for example, `temperature > 70` or `valve_status == "open"`). If the condition is met, data sending occurs.

**On external event (Event Trigger):** Reacts to events in the Faceplate event system (alarms, operator actions, network events).

**Combined Triggers:** Supports combinations: for example, send once every 10 seconds, but only if any value has changed and the `ready` flag is set to `true`.

**Trigger Settings:** Displayed on the corresponding configuration tab. Each trigger may have:

**Min. period per send request** - Minimum interval between two consecutive messages. Even if the tag has changed 10 times in a second, the packet will be sent no more frequently than this setting.

**Required delivery** - If the flag is set, the system will store the packet in the queue until receiving confirmation from the server (HTTP 200 OK).

**Trigger** - A button in the interface for immediate sending of the current data packet.

**Last successful request** - Informational (read-only) field displaying the timestamp of the last successful response.

**Max. period per send request** - Maximum silence interval. If triggers have not been activated during this time, the message is sent forcibly. Often used as a Heartbeat.

# 

# **2\. Transport Protocols (Connection Settings)** {#2.-transport-protocols-(connection-settings)}

## **2.1. HTTP (HyperText Transfer Protocol)** {#2.1.-http-(hypertext-transfer-protocol)}

HTTP (HyperText Transfer Protocol) is a data transmission protocol on the internet based on the REST architecture. It operates on a client-server model, where the client sends requests and the server sends responses.  

Protocol usage support is provided by Components:

* **iot\_http\_client\_connection:**  This is the client part of the connection. Sending requests (GET, POST, etc.) to external web servers.   
* **iot\_http\_server\_connection:**  Server part. Receiving incoming requests. Allows external systems to exchange data with Faceplate.

### **2.1.1. Client (iot\_http\_client\_connection)** {#2.1.1.-client-(iot_http_client_connection)}

The `iot_http_client_connection` component initializes requests to remote servers. To exchange data with the broker, you need to configure:

* **URL \-**	Full resource address, including protocol, IP/domain and port ([`http://192.168.1.50:8080/api/v1/data`](http://192.168.1.50:8080/api/v1/data)`)`  
* **Method** HTTP \- Request method defining the operation type.`GET` (read), `POST` (write)  
* **Timeout (ms) \-** Time limit for waiting for a response. When exceeded, the connection goes into `Error` status.  
* **Headers \-** Request metadata. Important for specifying content type or authorization.`Content-Type = application/json`  
* **Query \-** Variables passed in the URL string after the `?` sign.`token = xyz123`, `id = 5`  
* **Key \-** Path to the private key file for mutual TLS (mTLS). `/etc/ssl/client.key`  
* **Certificate \-** Path to the client SSL certificate file for HTTPS. `/etc/ssl/client.crt`  
* **CA Certificate \-** Path to the certificate authority certificate for server verification. `/etc/ssl/certs/rootCA.pem`
![Client (iot_http_client_connection](/IoT/images/iot_2.png)
### **2.1.2. Server (iot\_http\_server\_connection)** {#2.1.2.-server-(iot_http_server_connection)}

This component allows the Faceplate system to act as an HTTP server, accepting requests from external clients (SCADA systems, web applications, sensors) for reading or writing data.

To exchange data, you need to configure:

* **Path** \- URL path where the server expects data (for example, `/api/v1/data`).

* **Method** \- Supported request methods (`GET, POST, PUT, DELETE, HEAD, PATCH, TRACE, OPTIONS`).

* **Headers** \- Headers are used to transfer metadata between client and server. 

* **Query** \- Variables passed in the URL after the question mark (for example, `?device_id=123&status=active`).

* **Certificate** \- Path to the client SSL certificate file for HTTPS. `/etc/ssl/client.crt`

When configuring the connection, you can specify a list of permanent headers that will be added to each packet:

* **Content-Type:** Defining the data format (for example, `application/json`, `text/plain`).  
* **Authorization:** Transmitting access tokens (Bearer token) or Basic Auth data.  
* **User-Agent:** Identifying the Faceplate system client.

**Important:** Configuring **Path** and **Method** is mandatory.
![Server (iot_http_server_connection)](/IoT/images/iot_5.png)
## **2.2. MQTT** {#2.2.-mqtt}

MQTT (Message Queuing Telemetry Transport) is an open network protocol at the application level, operating over TCP/IP.

The platform includes only the following protocol component types:

* **iot\_mqtt\_publisher:** 	\- "Publisher".

* **iot\_mqtt\_subscriber:** \- "Subscriber".

The MQTT broker is not part of the protocol components on the Faceplate side and is an external service that needs to be connected to.

The MQTT broker must support protocol version 3.1.1 or higher, must accept all messages, filter them, determine who is subscribed, and send messages to subscribers.

### **2.2.2. Publisher (iot\_mqtt\_publisher)** {#2.2.2.-publisher-(iot_mqtt_publisher)}

The component is designed for publishing data from the Faceplate system to specific broker topics. To exchange data with the broker, you need to configure:

* **Host / Port:** MQTT broker address and port (default 1883 or 8883 for SSL).  
* **Client ID:** Determined by Faceplate software, for example  
  faceplate\_emqtt\_n01BnvEEqYTTfLjRdt4ke4DpVIvzycdlRMhz3tsKpJEteupJY57RH5XOXTw3fWbPD4eCmut2gaepwdjFekklmg=.  
* **Authentication:** Login and password for server access.  
* **Topic:** Path (for example, `sensors/factory1/temp`) to which data will be sent.  
* **QoS (Quality of Service):** Guaranteed delivery level (0 — at most once, 1 — at least once, 2 — exactly once).  
* **Key \-** Path to the private key file for mutual TLS (mTLS). `/etc/ssl/client.key`  
* **Certificate \-** Path to the client SSL certificate file for HTTPS. `/etc/ssl/client.crt`  
* **CA Certificate \-** Path to the certificate authority certificate for server verification. `/etc/ssl/certs/rootCA.pem`
![MQTT Publisher](/IoT/images/iot_6.png)
### **2.2.3. Subscriber (iot\_mqtt\_subscriber)** {#2.2.3.-subscriber-(iot_mqtt_subscriber)}

The component is designed for receiving data from external systems by subscribing to topics. To exchange data with the broker, you need to configure:
![MQTT Subscriber](/IoT/images/iot_7.png)
* **Host / Port:** MQTT broker address and port (default 1883 or 8883 for SSL).  
* **Client ID:** Determined by Faceplate software, for example  
* faceplate\_emqtt\_n01BnvEEqYTTfLjRdt4ke4DpVIvzycdlRMhz3tsKpJEteupJY57RH5XOXTw3fWbPD4eCmut2gaepwdjFekklmg=.  
* **Authentication:** Login and password for server access.  
* **Topic:** Topic template for subscription (for example, `sensors/factory1/temp`) to which data will be sent.

## **2.3. WebSocket** {#2.3.-websocket}

WebSocket is a communication protocol that establishes a persistent, bidirectional (duplex) connection between client and server through a single TCP connection, allowing them to exchange data in real-time.  

Protocol usage support is provided by Components:

* **iot\_websocket\_client\_connection:**  Client for establishing connection to server.  
* **iot\_websocket\_server\_connection:** Server for client connections.

### **2.3.1. Client (iot\_websocket\_client\_connection)** {#2.3.1.-client-(iot_websocket_client_connection)}

The **iot\_websocket\_client\_connection** component in the Faceplate system is designed for organizing **persistent bidirectional data exchange** in real-time between the platform and an external WebSocket server.

To exchange data, you need to configure:

* **URL \-** Full WebSocket server address (protocol `ws://` or `wss://`).`ws://echo.websocket.org`  
* **Headers \-** HTTP headers transmitted during handshake (for example, for authorization).`Authorization: Bearer <token>`  
* **Initialization request \-** JSON message sent immediately after opening the socket (login/registration).`{ "type": "auth", "key": "secret" }`  
* **Initialization response \-** Expected response from the server confirming readiness for data exchange.`{ "status": "authorized" }`  
* **Key \-** Path to the private key file for mutual TLS (mTLS). `/etc/ssl/client.key`  
* **Certificate \-** Path to the client SSL certificate file for HTTPS. `/etc/ssl/client.crt`  
* **CA Certificate \-** Path to the certificate authority certificate for server verification. `/etc/ssl/certs/rootCA.pem`
![Client (iot_websocket_client_connection)](/IoT/images/iot_9.png)
### **2.3.2. Server (iot\_websocket\_server\_connection)** {#2.3.2.-server-(iot_websocket_server_connection)}

The **iot\_websocket\_server\_connection** component turns the Faceplate system into a **WebSocket server**. Unlike the client, which connects to external resources itself, the server component opens a port and **awaits incoming connections** from external clients (browsers, mobile applications, or third-party controllers).

To exchange data, you need to configure:

* **Host \-** Network interface (IP address) of the server. `0.0.0.0` (all interfaces)   
* **Port \-** Port that the server will listen on. `8081`  
* **Path (Endpoint) \-** URL path for connecting specific clients.`/telemetry` or `/commands`

**Start as a client \-** Hybrid mode in which the server can initiate an outgoing WebSocket connection as a client.
![Server (iot_websocket_server_connection)](/IoT/images/iot_10.png)
#