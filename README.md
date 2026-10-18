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
English and Russian trees are organised the same way, but some file and
folder names differ between the languages.

```
docs/
├── en/
│   ├── Archives/
│   │   ├── images/  (29 files)
│   │   └── Archives.md
│   ├── git/
│   │   └── git_en.md
│   ├── historian/
│   │   └── historian_server_en.md
│   ├── IoT/
│   │   ├── images/  (15 files)
│   │   └── IoT.md
│   ├── machine_learning/
│   │   ├── forecasting_models_en.md
│   │   └── project_export_en.md
│   ├── plc_connections/
│   │   ├── images/  (63 files)
│   │   ├── diagnostics_en.md
│   │   ├── general_en.md
│   │   ├── old_plc_opcua_client_connection_en.md
│   │   ├── old_plc_opcua_server_connection_en.md
│   │   ├── old_plc_s7_connection_en.md
│   │   ├── plc_ethernet_ip_connection_en.md
│   │   ├── plc_iec101_client_connection_en.md
│   │   ├── plc_iec101_server_connection_en.md
│   │   ├── plc_iec104_client_connection_en.md
│   │   ├── plc_iec104_server_connection_en.md
│   │   ├── plc_mbus_connection_en.md
│   │   ├── plc_modbus_connection_en.md
│   │   ├── plc_opcda_connection_en.md
│   │   ├── plc_snmp_connection_en.md
│   │   └── transformation_en.md
│   ├── PowerBI_en/
│   │   ├── images/  (1 file)
│   │   └── PowerBi_FP_en.md
│   ├── Project_strucure/
│   │   ├── images/  (9 files)
│   │   └── FACEPLATE-start.md
│   ├── quick_start/
│   │   ├── connectivity/
│   │   │   ├── influxdb/
│   │   │   │   └── influxdb_en.md
│   │   │   ├── opc_ua/
│   │   │   │   └── opc_ua_client.md
│   │   │   ├── powerbi/
│   │   │   │   └── powerbi_en.md
│   │   │   └── rest api/
│   │   │       └── rest api.md
│   │   ├── prptotypes/
│   │   │   ├── influxdb/
│   │   │   │   └── influxdb_en.md
│   │   │   ├── pump/
│   │   │   │   └── pump_en.md
│   │   │   └── sensor/
│   │   │       └── sensor_en.md
│   │   └── deploy as docker.md
│   ├── Redundancy/
│   │   ├── images/  (6 files)
│   │   └── Redundancy_en.md
│   ├── storage/
│   │   ├── images/  (10 files)
│   │   └── Storage_en.md
│   └── readme.md
├── ru/
│   ├── git/
│   │   └── git_ru.md
│   ├── historian/
│   │   └── historian_server.md
│   ├── IoT/
│   │   ├── images/  (15 files)
│   │   └── IoT.docx.md
│   ├── machine_learning/
│   │   ├── forecasting_models_ru.md
│   │   └── project_export_ru.md
│   ├── plc_connections/
│   │   ├── images/  (63 files)
│   │   ├── diagnostics_ru.md
│   │   ├── general_ru.md
│   │   ├── old_plc_opcua_client_connection_ru.md
│   │   ├── old_plc_opcua_server_connection_ru.md
│   │   ├── old_plc_s7_connection_ru.md
│   │   ├── plc_ethernet_ip_connection_ru.md
│   │   ├── plc_iec101_client_connection_ru.md
│   │   ├── plc_iec101_server_connection_ru.md
│   │   ├── plc_iec104_client_connection_ru.md
│   │   ├── plc_iec104_server_connection_ru.md
│   │   ├── plc_mbus_connection_ru.md
│   │   ├── plc_modbus_connection_ru.md
│   │   ├── plc_opcda_connection_ru.md
│   │   ├── plc_snmp_connection_ru.md
│   │   └── transformation_ru.md
│   ├── PowerBI_ru/
│   │   ├── images/  (1 file)
│   │   └── PowerBi_FP_ru.md
│   ├── Project_strucure/
│   │   ├── images/  (9 files)
│   │   └── FACEPLATE-start.md
│   ├── Redundancy/
│   │   ├── images/  (6 files)
│   │   └── Redundancy_ru.md
│   ├── samples/
│   │   ├── connectivity/
│   │   │   ├── influxdb/
│   │   │   │   └── influxdb.md
│   │   │   ├── opc_ua_client/
│   │   │   │   └── opc_ua_client.md
│   │   │   ├── powerbi/
│   │   │   │   └── powerbi_ru.md
│   │   │   └── rest api/
│   │   │       └── rest api.md
│   │   ├── prptotypes/
│   │   │   ├── influxdb/
│   │   │   │   └── influxdb.md
│   │   │   ├── pump/
│   │   │   │   └── pump.md
│   │   │   └── sensor/
│   │   │       └── sensor.md
│   │   └── deploy as docker.md
│   ├── storage/
│   │   ├── images/  (10 files)
│   │   └── Storage_ru.md
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
`mkdocs.ru.yml` (site configuration and navigation), `tools/` (site build and
link checker), `Dockerfile`, `deploy/nginx.conf`, `docker-compose.yml`
(self-hosting) and `.github/workflows/docs.yml` (CI and GitHub Pages).

## Contents (English)

### General
- [General information, launch and licensing](docs/en/readme.md)
- [First steps in FACEPLATE Studio: project structure](docs/en/Project_strucure/FACEPLATE-start.md)
- [Deploying FACEPLATE in a Docker container](<docs/en/quick_start/deploy as docker.md>)

### Data acquisition
- [PLC connections: overview](docs/en/plc_connections/general_en.md)
  - [Modbus TCP/RTU](docs/en/plc_connections/plc_modbus_connection_en.md)
  - [OPC UA client](docs/en/plc_connections/old_plc_opcua_client_connection_en.md)
  - [OPC UA server](docs/en/plc_connections/old_plc_opcua_server_connection_en.md)
  - [OPC DA (Classic)](docs/en/plc_connections/plc_opcda_connection_en.md)
  - [Siemens S7 (ISO-on-TCP)](docs/en/plc_connections/old_plc_s7_connection_en.md)
  - [EtherNet/IP (Rockwell Automation)](docs/en/plc_connections/plc_ethernet_ip_connection_en.md)
  - [IEC 60870-5-101 client](docs/en/plc_connections/plc_iec101_client_connection_en.md)
  - [IEC 60870-5-101 server](docs/en/plc_connections/plc_iec101_server_connection_en.md)
  - [IEC 60870-5-104 client](docs/en/plc_connections/plc_iec104_client_connection_en.md)
  - [IEC 60870-5-104 server](docs/en/plc_connections/plc_iec104_server_connection_en.md)
  - [M-Bus (Meter-Bus)](docs/en/plc_connections/plc_mbus_connection_en.md)
  - [SNMP](docs/en/plc_connections/plc_snmp_connection_en.md)
  - [Transformation feature](docs/en/plc_connections/transformation_en.md)
  - [Diagnostics](docs/en/plc_connections/diagnostics_en.md)
- [IoT Connections module](docs/en/IoT/IoT.md)

### Data storage
- [Storage: databases and distributed storage](docs/en/storage/Storage_en.md)
- [Archives](docs/en/Archives/Archives.md)
- [Historian server](docs/en/historian/historian_server_en.md)

### Integrations
- [Microsoft Power BI](docs/en/PowerBI_en/PowerBi_FP_en.md)
- [REST API interface](<docs/en/quick_start/connectivity/rest api/rest api.md>)
- [OPC UA client (quick start)](docs/en/quick_start/connectivity/opc_ua/opc_ua_client.md)
- [Power BI (quick start)](docs/en/quick_start/connectivity/powerbi/powerbi_en.md)
- [Loading data into InfluxDB over HTTPS](docs/en/quick_start/connectivity/influxdb/influxdb_en.md)

### Prototype templates
- [InfluxDB integration template](docs/en/quick_start/prptotypes/influxdb/influxdb_en.md)
- [Pump template](docs/en/quick_start/prptotypes/pump/pump_en.md)
- [Sensor template](docs/en/quick_start/prptotypes/sensor/sensor_en.md)

### Machine learning
- [Forecasting models](docs/en/machine_learning/forecasting_models_en.md)
- [Project export (`faceplate_project-*.xlsx`)](docs/en/machine_learning/project_export_en.md)

### Administration
- [Resource redundancy](docs/en/Redundancy/Redundancy_en.md)
- [Git module](docs/en/git/git_en.md)
