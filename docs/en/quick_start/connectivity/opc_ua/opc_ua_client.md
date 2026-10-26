# Faceplate

Document: Quick Start. Faceplate (OPC UA Client) → OPC UA Server
Version: 4.0.7

# Introduction: Integration via OPC UA

This section describes the concept and practical steps for organizing data exchange in the Faceplate environment. A practical example is provided for retrieving data from an external system using the OPC UA industry standard.

## Solution Architecture

This guide implements the following data transfer chain:

- **Source (Server):** Third-party software or controller (in this example, _Prosys OPC UA Simulation Server_) simulating the operation of process equipment.
- **Receiver (Client):** The Faceplate platform, which connects to the source, reads variable values, and stores them in its own database (history).

The example uses the Prosys OPC UA Simulation server as the data source. The simulation server is designed for testing OPC UA clients, connections, and information models.

The Prosys OPC UA Simulation Server includes predefined simulation signals that can be connected to any variable and allow you to simulate data from real equipment, especially with the help of information models. The signals also provide a simulated data history according to OPC UA specifications.

## Guide Objective

By the end of this section, you will learn how to:

- Configure a transport channel (Connection) for communication with an external server.
- Create bindings (Bindings) for specific process parameters.
- Configure archiving of received data for subsequent analysis and visualization in the operator interface (**Runtime**).

# Necessary steps for implementing integration

## Preparing Prosys Simulation Server

Before configuring in Faceplate, start Prosys Simulation Server and record the following data in the **Status** tab:

- **Connection Address (Endpoint URL):** Typically, this is opc.tcp://\[PC_NAME\]:53530/OPCUA/SimulationServer.
- **Security Policy:** For the first test, select None (if server settings allow).

## Creating a connection in Faceplate (Connection)

Create a new connection of the type plc_opcua_client_connection.

### **Settings:**

- **Endpoint URL:** Paste the URL copied from Prosys (e.g., opc.tcp://192.168.1.10:53530/OPCUA/SimulationServer).
- **Security Mode:** Select None (according to the server settings for a simplified test).
- **User Identity:** Select Anonymous (Prosys Simulator allows anonymous logins by default).
- **State:** Set to **RUN**.

**Diagnostics:** If the status changes to **RUN** and the **Error** field is empty, then Faceplate has successfully established a session with Prosys.

## Setting up data binding (Binding)

Now we need to select the data we want to receive. Prosys Simulation Server generates random values ​​(sine waves, sawtooth waves, etc.).

### How to find the node address (NodeId)

In Prosys, go to the **Address Space** tab. Find, for example, the Sawtooth variable:

- It is usually located in the folder: Objects -> StaticData -> Sensors.
- Its **NodeId** will look something like this: ns=3;s=Sawtooth or ns=3;i=1001.

### Setting up in Faceplate

Create the plc_opcua_client_binding object within your connection:

- **Name:** Prosys_Sawtooth
- **Tag:** Select the tag in Faceplate where the data will be written (e.g., Global.Sensors.SawtoothValue).
- **OPC tag (NodeId):** Insert the address from Prosys: ns=3;s=Sawtooth.
- **Access:** Set to R (Read).
- **Sampling Interval:** Specify how often to poll the server (e.g., 1000 ms).

### Using the Browse Function

If you don't know the exact NodeId, use the **Browse** button in the Faceplate interface when setting up the binding:

- Click the node tree button.
- Faceplate will connect to Prosys and display the server folder hierarchy.
- Simply select the desired variable by clicking it - the NodeId will be filled in automatically.

## Working with Prosys

- **Certificates:** If you decide to use encryption (SignAndEncrypt), after the first attempt to connect Faceplate in Prosys Simulation Server, go to the **Certificates** tab and move the Faceplate certificate from the "Rejected" list to "Trusted."
- **Data Types:** Prosys passes Sawtooth and Sinusoid as Double. Make sure your tag in Faceplate supports real numbers.

## Summary

After the binding is set to **RUN**, the value in the Faceplate tag will begin updating according to the ramp graph from the simulator. This confirms that the exchange is configured correctly.