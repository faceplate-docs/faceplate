# Faceplate Documentation

Documentation for **FACEPLATE**, a software package for collecting data from
industrial equipment and IoT sources, converting it into information, storing
it, and giving access to it through the **Studio** (development) and
**Runtime** (operator) web interfaces.

The documentation is kept in two languages under `docs/en` and `docs/ru`.
Source `.docx` files that some pages were converted from live in `docs/source`.
See [CONTRIBUTING.md](CONTRIBUTING.md) for how pages are organised and
[DEPLOYMENT.md](DEPLOYMENT.md) for how the documentation website is built
and deployed (MkDocs + Material, Docker or GitHub Pages).

---

## English

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

---

## Русский

### Общие сведения
- [Общие сведения, запуск и лицензирование](docs/ru/readme.md)
- [Первые шаги в FACEPLATE Studio: структура проекта](docs/ru/Project_strucure/FACEPLATE-start.md)
- [Установка и запуск FACEPLATE в Docker-контейнере](<docs/ru/samples/deploy as docker.md>)

### Сбор данных
- [PLC-соединения: обзор](docs/ru/plc_connections/general_ru.md)
  - [Modbus TCP/RTU](docs/ru/plc_connections/plc_modbus_connection_ru.md)
  - [OPC UA Client](docs/ru/plc_connections/old_plc_opcua_client_connection_ru.md)
  - [OPC UA Server](docs/ru/plc_connections/old_plc_opcua_server_connection_ru.md)
  - [OPC DA (Classic)](docs/ru/plc_connections/plc_opcda_connection_ru.md)
  - [Siemens S7 (ISO-on-TCP)](docs/ru/plc_connections/old_plc_s7_connection_ru.md)
  - [Ethernet/IP (Rockwell Automation)](docs/ru/plc_connections/plc_ethernet_ip_connection_ru.md)
  - [IEC 60870-5-101 Client](docs/ru/plc_connections/plc_iec101_client_connection_ru.md)
  - [IEC 60870-5-101 Server](docs/ru/plc_connections/plc_iec101_server_connection_ru.md)
  - [IEC 60870-5-104 Client](docs/ru/plc_connections/plc_iec104_client_connection_ru.md)
  - [IEC 60870-5-104 Server](docs/ru/plc_connections/plc_iec104_server_connection_ru.md)
  - [M-Bus (Meter-Bus)](docs/ru/plc_connections/plc_mbus_connection_ru.md)
  - [SNMP](docs/ru/plc_connections/plc_snmp_connection_ru.md)
  - [Функция Transformation](docs/ru/plc_connections/transformation_ru.md)
  - [Диагностика](docs/ru/plc_connections/diagnostics_ru.md)
- [Модуль IoT-соединений](docs/ru/IoT/IoT.docx.md)

### Хранение данных
- [Хранилища: базы данных и распределённое хранение](docs/ru/storage/Storage_ru.md)
- [Архивы и тренды](<docs/ru/Архивы и Тренды.md>)
- [Historian-сервер](docs/ru/historian/historian_server.md)

### Интеграции
- [Microsoft Power BI](docs/ru/PowerBI_ru/PowerBi_FP_ru.md)
- [REST API интерфейс](<docs/ru/samples/connectivity/rest api/rest api.md>)
- [OPC UA Client (пример)](docs/ru/samples/connectivity/opc_ua_client/opc_ua_client.md)
- [Power BI (пример)](docs/ru/samples/connectivity/powerbi/powerbi_ru.md)
- [Загрузка данных в InfluxDB по HTTPS](docs/ru/samples/connectivity/influxdb/influxdb.md)

### Шаблоны прототипов
- [Шаблон интеграции с InfluxDB](docs/ru/samples/prptotypes/influxdb/influxdb.md)
- [Шаблон Pump](docs/ru/samples/prptotypes/pump/pump.md)
- [Шаблон Sensor](docs/ru/samples/prptotypes/sensor/sensor.md)

### Машинное обучение
- [Модели прогнозирования](docs/ru/machine_learning/forecasting_models_ru.md)
- [Экспорт проекта (`faceplate_project-*.xlsx`)](docs/ru/machine_learning/project_export_ru.md)

### Администрирование
- [Резервирование ресурсов](docs/ru/Redundancy/Redundancy_ru.md)
- [Модуль Git](docs/ru/git/git_ru.md)
- [Интеграция с Git (краткое руководство)](<docs/ru/Git в Faceplate.md>)
