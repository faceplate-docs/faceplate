# General information

FACEPLATE is a software package that provides the user with a unified environment and a set of tools for collecting and converting data into information, storing it, and organizing access to it through various interfaces.  
FACEPLATE features a sophisticated web interface designed for both developers and end users.

* Developers use the Studio interface to develop projects: setting up connections, designing user interfaces, time series data, mathematical models, etc.  
* End users utilize the Runtime interface, which provides access to real-time information, including information on the current asset status, analytics, KPIs, AI recommendations, alerts about potential deviations, and much more.

## Usage

FACEPLATE allows you to consolidate all existing and continuously incoming data about an object into a single information space and provides the following capabilities:

* visualization of current and archived data;  
* performing in-depth analysis of accumulated and current data using reports, graphs and charts;  
* identifying anomalies and correlations, as well as generating forecasts using high-tech tools, including machine learning methods;  
* obtaining contextual information about the control object and management recommendations, including options for action in critical situations, based on LLM models;  
* modeling various scenarios for the development of situations using mathematical models.

## Functional

The functionality of the FACEPLATE software package is flexible and can be changed during the technical specification approval stage.  
Functionality by software package modules:

* The General View is the project's main module, displaying a hierarchical list of all objects, screens, and components within the project. It's used for navigating the project structure and quickly accessing its elements.  
* Prototypes is a module for managing object prototypes and their display. It allows you to create, edit, and reuse standard project elements, ensuring a consistent style and reducing development time.  
* Primitives – a module for managing basic project elements  
* Catalogs is a module for organizing data into a set of tables. This functionality displays information in a user-friendly format, organized into a set of tables.  
* Library Modules – a module for creating and managing script libraries. It allows for centralized storage and reuse of common functions and logic blocks.  
* Localization is a module for configuring interface language localization. It allows you to manage text translations and adapt your project for a multilingual environment.  
* Permissions is a module for managing user access and role rights. It is used to define permissions for viewing, editing, and administering project elements.  
* Servers – a module for monitoring the status of FACEPLATE servers. Displays information about the availability, load, and current status of the system's server components.  
* Message – a module of the messaging system. A messaging system for recording and archiving events with the ability to display and manage them; customizing message categories; displaying, alerting, and archiving  
* Archive is a data archiving system module. The built-in archiving subsystem supports data storage and processing needs for projects of varying complexity and allows for the evaluation of process parameter dynamics over long periods of time.  
* Aggregates – an editor for creating custom aggregates for trends. Allows you to create aggregated indicators and derived data based on historical values.  
* Security Settings – Security and Authorization Settings Editor. Used to configure the OAuth 2.0 protocol and manage authentication and authorization mechanisms.  
* Calculation – a module for creating computational blocks, including formulas, rules, and data processing algorithms. It is used to implement calculations and signal processing logic.  
* Git – a module for integrating with the Git version control system. It allows you to manage versions of a project under development, perform commits, compare, and synchronize changes.  
* Graph Engine is a graph, diagram, and visual data analysis editor. It is used to represent relationships, data flows, and analytical dependencies.  
* IoT Connections is a module for editing and configuring IoT connections. It is designed for connecting external IoT devices and data sources.  
* PLC Drivers – a module for setting up and managing connections to programmable logic controllers (PLCs). Provides integration with industrial equipment.  
* Powerfactory service – a module for integration with electrical network analysis and modeling services.  
* Replica is a module for editing project replicas. It allows you to manage information synchronization within a project.  
* Script – a module for editing custom scripts. It is used to implement additional logic, automation, and data processing.  
* Storage is a database configuration module used to organize data storage methods.

# Launch

To run successfully, the server must meet the following requirements:  
Server environment:

* Operating system: 64-bit Linux distributions  
  * Ubuntu (starting with version 22.04.5)  
  * CentOS (starting with version 9\)  
  * Debian (since version 11\)  
  * Red Hat (since version 9\)  
* Architecture: x86\_64  
* RAM: from 4 GB  
* Disk space: from 10 GB of free space  
* Network: TCP/IP access for connecting client workstations

Client environment:

* Any device with a web browser  
* Web browser  
  * Apple Safari (starting with version 18.0)  
  * Google Chrome (starting with version 144.0.1)  
  * Microsoft Edge (starting with version 143.0.1)  
  * Mozilla Firefox (starting with version 147.0.1)  
* Mobile browser versions are supported

General requirements:

* Correctly configured system time and network parameters  
* Possibility of accessing the server via HTTP/HTTPS  
* Server hardware resources are selected depending on the expected load and scale of system operation.

These requirements are sufficient for basic startup and test use of FACEPLATE; for industrial and high-load systems, a more powerful configuration is required.  
The path to the folder from which the application will be launched must consist of Latin characters and must not contain spaces, brackets, or special characters.  
FACEPLATE runs on the server from the distribution package with the faceplate executable file in the bin directory. Administrator privileges are required to run the application. To launch the application, open a terminal and run the following commands:

* ulimit \-n 200000  
  * It is necessary to set a limit on the maximum number of simultaneously open files  
* ./faceplate console  
  * console \- launch an application with an interactive shell

After successful launch, the following interfaces are available: FACEPLATE Studio, FACEPLATE Runtime, ECOMET.  
Information on setting up the running node, paths to logs, the database, and more is available at [the link](https://github.com/faceplate-docs/faceplate/blob/dev/docs/ru/README.md) .

## FACEPLATE Studio

FACEPLATE development environment. A client can connect from any device with network access to the FACEPLATE server.   
To do this, navigate to one of the following addresses in your browser:

* http://\<ip address\>:9000/fp/studio  
* https://\<ip address\>:9443/fp/studio

## FACEPLATE Runtime

The FACEPLATE runtime environment is designed for operators. To open the runtime environment in a browser, use one of the following URLs:

* http://\<ip address\>:9000/fp/runtime  
* https://\<ip address\>:9443/fp/runtime

Where \<ip address\> is the IP address of the server running FACEPLATE. Connections from client devices are established if network access to the FACEPLATE server is available.

# Licensing

A license is required for the continuous operation of the server. A license issued for one server cannot be used on another.