<p align="left">
  <a href="https://faceplate-docs.github.io/faceplate/"><img src="brand/assets/faceplate-logo.png" alt="FACEPLATE" width="420"></a>
  <br>
  <em>Physical AI for energy and industrial infrastructure</em> · <a href="https://faceplate.io/">faceplate.io</a>
</p>

# Faceplate Documentation

Documentation for **FACEPLATE**, a software package for collecting data from
industrial equipment and IoT sources, converting it into information, storing
it, and giving access to it through the **Studio** (development) and
**Runtime** (operator) web interfaces.

**Published site:** <https://faceplate-docs.github.io/faceplate/>
(English at [/en/](https://faceplate-docs.github.io/faceplate/en/), Russian at
[/ru/](https://faceplate-docs.github.io/faceplate/ru/)).

The documentation is kept in two languages under `docs/en` and `docs/ru`.
This README links to the English pages only; the Russian version is read on
the published site. Source `.docx` files that some pages were converted from
live in `docs/source`.
See [CONTRIBUTING.md](CONTRIBUTING.md) for how pages are organised and
[DEPLOYMENT.md](DEPLOYMENT.md) for how the documentation website is built
and deployed (MkDocs + Material, Docker or GitHub Pages).

## Repository structure

Each topic lives in its own folder with its images next to the page. The
English and Russian trees are organised the same way, with the same folder
and file names; the language is given by the top folder.

```
docs/
├── en/
│   ├── access/
│   │   ├── images/  (4 files)
│   │   ├── roles.md
│   │   └── users.md
│   ├── administration/
│   │   ├── diagnostics/
│   │   │   ├── images/  (5 files)
│   │   │   └── diagnostics.md
│   │   ├── git/
│   │   │   ├── images/  (2 files)
│   │   │   └── git.md
│   │   ├── license/
│   │   │   ├── images/  (7 files)
│   │   │   └── license.md
│   │   ├── logs/
│   │   │   ├── images/  (1 file)
│   │   │   └── logs.md
│   │   ├── nodes/
│   │   │   ├── images/  (9 files)
│   │   │   └── nodes.md
│   │   ├── redundancy/
│   │   │   ├── images/  (6 files)
│   │   │   └── redundancy.md
│   │   ├── replica/
│   │   │   ├── images/  (2 files)
│   │   │   └── replica.md
│   │   └── update/
│   │       ├── images/  (3 files)
│   │       └── update.md
│   ├── alarms/
│   │   ├── alarm/
│   │   │   ├── images/  (7 files)
│   │   │   └── alarm.md
│   │   └── dsf/
│   │       ├── images/  (3 files)
│   │       └── dsf.md
│   ├── data_collection/
│   │   ├── IoT/
│   │   │   ├── images/  (26 files)
│   │   │   ├── actions.md
│   │   │   ├── http.md
│   │   │   ├── IoT.md
│   │   │   ├── mqtt.md
│   │   │   ├── sources.md
│   │   │   └── websocket.md
│   │   └── plc_connections/
│   │       ├── images/  (108 files)
│   │       ├── examples/
│   │       │   └── modbus_training_server.py
│   │       ├── bindings.md
│   │       ├── diagnostics.md
│   │       ├── general.md
│   │       ├── iec_reference.md
│   │       ├── index.md
│   │       ├── old_plc_opcua_client_connection.md
│   │       ├── old_plc_opcua_server_connection.md
│   │       ├── old_plc_s7_connection.md
│   │       ├── plc_dcon_connection.md
│   │       ├── plc_ethernet_ip_connection.md
│   │       ├── plc_iec101_client_connection.md
│   │       ├── plc_iec101_server_connection.md
│   │       ├── plc_iec104_client_connection.md
│   │       ├── plc_iec104_server_connection.md
│   │       ├── plc_iec62056_connection.md
│   │       ├── plc_mbus_connection.md
│   │       ├── plc_mercury230_connection.md
│   │       ├── plc_modbus_connection.md
│   │       ├── plc_opcda_connection.md
│   │       ├── plc_snmp_connection.md
│   │       └── transformation.md
│   ├── data_storage/
│   │   ├── archives/
│   │   │   ├── images/  (10 files)
│   │   │   ├── aggregates.md
│   │   │   ├── archives.md
│   │   │   └── trends.md
│   │   ├── historian/
│   │   │   └── historian_server.md
│   │   └── storage/
│   │       ├── images/  (10 files)
│   │       └── storage.md
│   ├── general/
│   │   ├── docker/
│   │   │   └── deploy as docker.md
│   │   └── project_structure/
│   │       ├── images/  (9 files)
│   │       └── FACEPLATE-start.md
│   ├── integrations/
│   │   ├── influxdb/
│   │   │   └── influxdb.md
│   │   ├── opc_ua/
│   │   │   └── opc_ua_client.md
│   │   ├── powerbi/
│   │   │   ├── images/  (1 file)
│   │   │   ├── powerbi.md
│   │   │   └── PowerBi_FP.md
│   │   ├── powerfactory_service/
│   │   │   ├── images/  (7 files)
│   │   │   └── powerfactory_service.md
│   │   └── rest api/
│   │       └── rest api.md
│   ├── machine_learning/
│   │   ├── forecasting_models.md
│   │   └── project_export.md
│   ├── mnemo/
│   │   ├── images/  (101 files)
│   │   ├── alarms_trends.md
│   │   ├── bindings.md
│   │   ├── controls.md
│   │   ├── datasources.md
│   │   ├── editor.md
│   │   ├── events.md
│   │   ├── gauges.md
│   │   ├── graphics.md
│   │   ├── images.md
│   │   ├── lists.md
│   │   ├── reports.md
│   │   ├── screens.md
│   │   └── tables.md
│   ├── project_logic/
│   │   ├── calculation/
│   │   │   ├── images/  (11 files)
│   │   │   └── calculation.md
│   │   ├── js_library/
│   │   │   ├── images/  (8 files)
│   │   │   └── js_library.md
│   │   ├── library_modules/
│   │   │   ├── images/  (6 files)
│   │   │   └── library_modules.md
│   │   └── user_script/
│   │       ├── images/  (9 files)
│   │       └── user_script.md
│   ├── project_objects/
│   │   ├── catalogs/
│   │   │   ├── images/  (10 files)
│   │   │   └── catalogs.md
│   │   ├── localization/
│   │   │   ├── images/  (9 files)
│   │   │   └── localization.md
│   │   ├── primitives/
│   │   │   ├── images/  (10 files)
│   │   │   └── primitives.md
│   │   └── prototypes/
│   │       ├── images/  (18 files)
│   │       └── prototypes.md
│   ├── templates/
│   │   ├── influxdb/
│   │   │   └── influxdb.md
│   │   ├── pump/
│   │   │   └── pump.md
│   │   └── sensor/
│   │       └── sensor.md
│   └── readme.md
├── ru/
│   ├── access/
│   │   ├── images/  (4 files)
│   │   ├── roles.md
│   │   └── users.md
│   ├── administration/
│   │   ├── diagnostics/
│   │   │   ├── images/  (5 files)
│   │   │   └── diagnostics.md
│   │   ├── git/
│   │   │   ├── images/  (2 files)
│   │   │   └── git.md
│   │   ├── license/
│   │   │   ├── images/  (7 files)
│   │   │   └── license.md
│   │   ├── logs/
│   │   │   ├── images/  (1 file)
│   │   │   └── logs.md
│   │   ├── nodes/
│   │   │   ├── images/  (9 files)
│   │   │   └── nodes.md
│   │   ├── redundancy/
│   │   │   ├── images/  (6 files)
│   │   │   └── redundancy.md
│   │   ├── replica/
│   │   │   ├── images/  (2 files)
│   │   │   └── replica.md
│   │   └── update/
│   │       ├── images/  (3 files)
│   │       └── update.md
│   ├── alarms/
│   │   ├── alarm/
│   │   │   ├── images/  (7 files)
│   │   │   └── alarm.md
│   │   └── dsf/
│   │       ├── images/  (3 files)
│   │       └── dsf.md
│   ├── data_collection/
│   │   ├── IoT/
│   │   │   ├── images/  (26 files)
│   │   │   ├── actions.md
│   │   │   ├── http.md
│   │   │   ├── IoT.md
│   │   │   ├── mqtt.md
│   │   │   ├── sources.md
│   │   │   └── websocket.md
│   │   └── plc_connections/
│   │       ├── images/  (108 files)
│   │       ├── examples/
│   │       │   └── modbus_training_server.py
│   │       ├── bindings.md
│   │       ├── diagnostics.md
│   │       ├── general.md
│   │       ├── iec_reference.md
│   │       ├── index.md
│   │       ├── old_plc_opcua_client_connection.md
│   │       ├── old_plc_opcua_server_connection.md
│   │       ├── old_plc_s7_connection.md
│   │       ├── plc_dcon_connection.md
│   │       ├── plc_ethernet_ip_connection.md
│   │       ├── plc_iec101_client_connection.md
│   │       ├── plc_iec101_server_connection.md
│   │       ├── plc_iec104_client_connection.md
│   │       ├── plc_iec104_server_connection.md
│   │       ├── plc_iec62056_connection.md
│   │       ├── plc_mbus_connection.md
│   │       ├── plc_mercury230_connection.md
│   │       ├── plc_modbus_connection.md
│   │       ├── plc_opcda_connection.md
│   │       ├── plc_snmp_connection.md
│   │       └── transformation.md
│   ├── data_storage/
│   │   ├── archives/
│   │   │   ├── images/  (10 files)
│   │   │   ├── aggregates.md
│   │   │   ├── archives.md
│   │   │   └── trends.md
│   │   ├── historian/
│   │   │   └── historian_server.md
│   │   └── storage/
│   │       ├── images/  (10 files)
│   │       └── storage.md
│   ├── general/
│   │   ├── docker/
│   │   │   └── deploy as docker.md
│   │   └── project_structure/
│   │       ├── images/  (9 files)
│   │       └── FACEPLATE-start.md
│   ├── integrations/
│   │   ├── influxdb/
│   │   │   └── influxdb.md
│   │   ├── opc_ua/
│   │   │   └── opc_ua_client.md
│   │   ├── powerbi/
│   │   │   ├── images/  (1 file)
│   │   │   ├── powerbi.md
│   │   │   └── PowerBi_FP.md
│   │   ├── powerfactory_service/
│   │   │   ├── images/  (7 files)
│   │   │   └── powerfactory_service.md
│   │   └── rest api/
│   │       └── rest api.md
│   ├── machine_learning/
│   │   ├── forecasting_models.md
│   │   └── project_export.md
│   ├── mnemo/
│   │   ├── images/  (101 files)
│   │   ├── alarms_trends.md
│   │   ├── bindings.md
│   │   ├── controls.md
│   │   ├── datasources.md
│   │   ├── editor.md
│   │   ├── events.md
│   │   ├── gauges.md
│   │   ├── graphics.md
│   │   ├── images.md
│   │   ├── lists.md
│   │   ├── reports.md
│   │   ├── screens.md
│   │   └── tables.md
│   ├── project_logic/
│   │   ├── calculation/
│   │   │   ├── images/  (11 files)
│   │   │   └── calculation.md
│   │   ├── js_library/
│   │   │   ├── images/  (8 files)
│   │   │   └── js_library.md
│   │   ├── library_modules/
│   │   │   ├── images/  (6 files)
│   │   │   └── library_modules.md
│   │   └── user_script/
│   │       ├── images/  (9 files)
│   │       └── user_script.md
│   ├── project_objects/
│   │   ├── catalogs/
│   │   │   ├── images/  (10 files)
│   │   │   └── catalogs.md
│   │   ├── localization/
│   │   │   ├── images/  (9 files)
│   │   │   └── localization.md
│   │   ├── primitives/
│   │   │   ├── images/  (10 files)
│   │   │   └── primitives.md
│   │   └── prototypes/
│   │       ├── images/  (18 files)
│   │       └── prototypes.md
│   ├── templates/
│   │   ├── influxdb/
│   │   │   └── influxdb.md
│   │   ├── pump/
│   │   │   └── pump.md
│   │   └── sensor/
│   │       └── sensor.md
│   ├── Git в Faceplate.md
│   ├── readme.md
│   ├── title.md
│   └── Архивы и Тренды.md
└── source/
    ├── git_ru.docx
    ├── iot_ru.docx
    ├── PLC-соединения OPC client.docx
    ├── PLC-соединения OPC server.docx
    ├── PLC_connections.docx
    ├── powerbi_ru.docx
    ├── Quick start.docx
    ├── quick_start.docx
    └── readme_ru.docx
```

Other files at the repository root: `mkdocs.base.yml`, `mkdocs.en.yml` and
`mkdocs.ru.yml` (site configuration and navigation), `brand/assets/` (logo,
favicon and brand stylesheet), `tools/` (site build and link checker),
`Dockerfile`, `deploy/nginx.conf`, `docker-compose.yml` (self-hosting) and
`.github/workflows/docs.yml` (CI and GitHub Pages).

## Contents (English)

### General
- [General information, launch and licensing](docs/en/readme.md)
- [First steps in FACEPLATE Studio: project structure](docs/en/general/project_structure/FACEPLATE-start.md)
- [Deploying FACEPLATE in a Docker container](<docs/en/general/docker/deploy as docker.md>)

### Access
- [Users](docs/en/access/users.md)
- [Roles and access rights](docs/en/access/roles.md)

### Data acquisition
- [PLC connections: overview](docs/en/data_collection/plc_connections/index.md)
  - [Field preparation and bindings](docs/en/data_collection/plc_connections/bindings.md)
  - [Modbus TCP training example](docs/en/data_collection/plc_connections/general.md)
  - [Modbus TCP/RTU](docs/en/data_collection/plc_connections/plc_modbus_connection.md)
  - [DCON](docs/en/data_collection/plc_connections/plc_dcon_connection.md)
  - [OPC UA client](docs/en/data_collection/plc_connections/old_plc_opcua_client_connection.md)
  - [OPC UA server](docs/en/data_collection/plc_connections/old_plc_opcua_server_connection.md)
  - [OPC DA (Classic)](docs/en/data_collection/plc_connections/plc_opcda_connection.md)
  - [Siemens S7 (ISO-on-TCP)](docs/en/data_collection/plc_connections/old_plc_s7_connection.md)
  - [EtherNet/IP (Rockwell Automation)](docs/en/data_collection/plc_connections/plc_ethernet_ip_connection.md)
  - [IEC 60870-5-101 client](docs/en/data_collection/plc_connections/plc_iec101_client_connection.md)
  - [IEC 60870-5-101 server](docs/en/data_collection/plc_connections/plc_iec101_server_connection.md)
  - [IEC 60870-5-104 client](docs/en/data_collection/plc_connections/plc_iec104_client_connection.md)
  - [IEC 60870-5-104 server](docs/en/data_collection/plc_connections/plc_iec104_server_connection.md)
  - [M-Bus (Meter-Bus)](docs/en/data_collection/plc_connections/plc_mbus_connection.md)
  - [Mercury 230](docs/en/data_collection/plc_connections/plc_mercury230_connection.md)
  - [SNMP](docs/en/data_collection/plc_connections/plc_snmp_connection.md)
  - [IEC 62056](docs/en/data_collection/plc_connections/plc_iec62056_connection.md)
  - [IEC101/IEC104 types and attributes](docs/en/data_collection/plc_connections/iec_reference.md)
  - [Transformation feature](docs/en/data_collection/plc_connections/transformation.md)
  - [PLC communication checks](docs/en/data_collection/plc_connections/diagnostics.md)
- [IoT connections](docs/en/data_collection/IoT/IoT.md)
  - [HTTP](docs/en/data_collection/IoT/http.md)
  - [MQTT](docs/en/data_collection/IoT/mqtt.md)
  - [WebSocket](docs/en/data_collection/IoT/websocket.md)
  - [Sources](docs/en/data_collection/IoT/sources.md)
  - [Actions](docs/en/data_collection/IoT/actions.md)

### Data storage
- [Storages: which servers hold the project data](docs/en/data_storage/storage/storage.md)
- [Archives](docs/en/data_storage/archives/archives.md)
- [Historian server](docs/en/data_storage/historian/historian_server.md)

### Alarms and events
- [Messages and alarms](docs/en/alarms/alarm/alarm.md)
- [Dispatcher advisor](docs/en/alarms/dsf/dsf.md)

### Project objects
- [Primitives](docs/en/project_objects/primitives/primitives.md)
- [Prototypes](docs/en/project_objects/prototypes/prototypes.md)
- [Catalogs](docs/en/project_objects/catalogs/catalogs.md)
- [Localization](docs/en/project_objects/localization/localization.md)

### Screens
- [Screen editor](docs/en/mnemo/editor.md)
- [Graphic elements](docs/en/mnemo/graphics.md)
- [Buttons and value input](docs/en/mnemo/controls.md)
- [Selection from lists](docs/en/mnemo/lists.md)
- [Dial and linear gauges](docs/en/mnemo/gauges.md)
- [Tables and timeline](docs/en/mnemo/tables.md)
- [Bindings and animation](docs/en/mnemo/bindings.md)
- [Data sources on a screen](docs/en/mnemo/datasources.md)
- [Scripts and events](docs/en/mnemo/events.md)
- [Screens and navigation](docs/en/mnemo/screens.md)
- [Reports and screen printing](docs/en/mnemo/reports.md)
- [Alarms and trends on a screen](docs/en/mnemo/alarms_trends.md)
- [Image library](docs/en/mnemo/images.md)

### Project logic
- [Calculations](docs/en/project_logic/calculation/calculation.md)
- [User scripts](docs/en/project_logic/user_script/user_script.md)
- [Library modules](docs/en/project_logic/library_modules/library_modules.md)
- [JS libraries](docs/en/project_logic/js_library/js_library.md)

### Integrations
- [Microsoft Power BI](docs/en/integrations/powerbi/PowerBi_FP.md)
- [REST API interface](<docs/en/integrations/rest api/rest api.md>)
- [OPC UA client (quick start)](docs/en/integrations/opc_ua/opc_ua_client.md)
- [Power BI (quick start)](docs/en/integrations/powerbi/powerbi.md)
- [Loading data into InfluxDB over HTTPS](docs/en/integrations/influxdb/influxdb.md)
- [Powerfactory Service](docs/en/integrations/powerfactory_service/powerfactory_service.md)

### Prototype templates
- [InfluxDB integration template](docs/en/templates/influxdb/influxdb.md)
- [Pump template](docs/en/templates/pump/pump.md)
- [Sensor template](docs/en/templates/sensor/sensor.md)

### Machine learning
- [Forecasting models](docs/en/machine_learning/forecasting_models.md)
- [Project export (`faceplate_project-*.xlsx`)](docs/en/machine_learning/project_export.md)

### Administration
- [Resource redundancy](docs/en/administration/redundancy/redundancy.md)
- [Cluster nodes](docs/en/administration/nodes/nodes.md)
- [Licensing](docs/en/administration/license/license.md)
- [Replication](docs/en/administration/replica/replica.md)
- [Git module](docs/en/administration/git/git.md)
- [Diagnostics of Runtime objects](docs/en/administration/diagnostics/diagnostics.md)
- [Server logs](docs/en/administration/logs/logs.md)
- [Version and update](docs/en/administration/update/update.md)
