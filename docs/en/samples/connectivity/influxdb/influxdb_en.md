# Loading Data into InfluxDB (HTTPS)

Document: Faceplate Data Exchange Specification → InfluxDB
Version: 1.0

## 1. Solution Architecture

## 4. InfluxDB Data Loading Example

This example is an application project with a solution for loading data into InfluxDB based on standard Faceplate tools. For a better understanding, it is recommended to familiarize yourself with the following components:
- prtotypes
- primitives
- iot_connections
- global_modules

To load the project, you need to download the export file (https:github.com/faceplate-docs/faceplate/prototypes/connectivity/influxdb) and import it into Faceplate.

### 4.1 Required Environment

This project is a solution developed in standard Faceplate editors that implements the following functionality:
1. Collecting data from objects marked for sending to an influxdb instance. 2. Necessary data conversion and message generation in Line Protocol format
3. Sending data via HTTP(S) to the specified address with delivery confirmation (code 204).

### 4.2 Project Import and Configuration
1. To begin setting up the project environment, download and import Faceplate into the project.
2. After the import is complete, the list of available prototypes should include elements named influxdb, pump, and sensor, where:
a. influxdb - a prototype containing all the necessary mechanisms for exchanging data with an InfluxDB instance;
b. pump - an object representing a pump as an object in the project hierarchy;
c. sensor - an object representing a single measurement point.
Descriptions of these prototypes are provided in the [prototypes] section (docs/ru/samples/prptotypes).
3. The project tree should contain a structure with objects describing the hierarchy:

<project hierarchy>/<monitoring object>/<sensor set>

where area is a directory grouping monitoring objects by their physical or logical location, for example:

"station A/pump #1/flow"

This hierarchy serves as the basis for creating a point relative to the **workshop** directory for generating a telegram and writing it to InfluxDB in Line Protocol format:

<monitoring object>,<tag name>=<tag value> <sensor name>=<sensor value> timestamp

The influxdb object is designed to find all specified object types and groups the sensor objects within them into a single data block, then transforming the messages.

To convey the uniqueness of a monitoring object, use the tags <tag name>=<tag value>. In InfluxDB, tags are used to create a filter when querying data. This way, you can create a message relative to any project structure by specifying the required number of tags in the message.

### Scaling

The scaling process is based on adding influxdb and pump prototypes to the required directories in the project tree.

Both prototypes can be extended by the user to solve additional problems and are provided for informational purposes.

Recommendation: Send data in batches (batch writing) – 500–1000 rows per request for optimal performance.

## 5. Security and Fault Tolerance

- Certificate Verification: Ensure root CAs are installed on the Faceplate server to verify the InfluxDB SSL certificate.
- Buffering: If the connection is lost, data is saved to a local buffer to preserve points until the connection is restored.