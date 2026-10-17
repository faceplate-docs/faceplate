# FACEPLATE Documentation

FACEPLATE is a SCADA/EMS platform for industrial and energy companies: PLC data acquisition, historian, calculations, digital twins and an operator web UI in one product.

> The Russian documentation is the source. English pages are translated after the Russian page is approved.

## Find your section

| If you are… | Start with |
|---|---|
| a dispatcher or operator | [Operator guide](operator/README.md) |
| an engineer building a project | [Project engineer guide](engineer/README.md) |
| an administrator or DevOps | [Administrator guide](admin/README.md) |
| new to the platform | [Platform overview](overview/README.md) |

## Contents

### Overview

- [Platform overview](overview/README.md)
- [Architecture](overview/architecture.md)
- [Glossary](overview/glossary.md)

### Operators

- [Operator guide](operator/README.md)
- [Signing in and the interface](operator/getting-started.md)
- [Monitoring](operator/monitoring.md)
- [Equipment control](operator/control.md)
- [Alarms and events](operator/alarms.md)
- [Trends and history](operator/trends.md)
- [Reports and data export](operator/reports.md)

### Project engineers

- [Project engineer guide](engineer/README.md)
- [Project model: objects, prototypes, fields](engineer/project-model.md)
- [Query language](engineer/query-language.md)
- [Device connections](engineer/connections/README.md)
  - [Modbus](engineer/connections/modbus.md)
  - [IEC 60870-5-101/104](engineer/connections/iec-104.md)
  - [OPC UA / OPC DA](engineer/connections/opc-ua.md)
  - [IoT: MQTT, HTTP, WebSocket](engineer/connections/iot.md)
  - [Other protocols](engineer/connections/other-protocols.md)
- [Archives](engineer/archives.md)
- [Alarm configuration](engineer/alarms.md)
- [Calculations (fp-calculation)](engineer/calculations.md)
- [Server scripts](engineer/scripts.md)
- [Topology colouring (graph_engine)](engineer/graph-engine.md)
- [Screens and mimics](engineer/screens/README.md)
  - [Tables (Grid element)](engineer/screens/grid.md)
  - [Front-end JS libraries](engineer/screens/js-libraries.md)
  - [Built-in UI elements](engineer/screens/ui-elements.md)
- [Project versioning (fp_git)](engineer/versioning.md)
- [Platform API](engineer/api/README.md)
  - [Objects API (CRUD)](engineer/api/objects-crud.md)
  - [Archives API](engineer/api/archives-api.md)

### Administrators

- [Administrator guide](admin/README.md)
- [System requirements](admin/requirements.md)
- [Installation](admin/installation.md)
- [Configuration](admin/configuration.md)
- [Running in containers](admin/docker.md)
- [Projects and clean databases](admin/projects.md)
- [Users and access](admin/users-access.md)
- [Redundancy and replication](admin/replication.md)
- [Backup and restore](admin/backup-restore.md)
- [Upgrading](admin/upgrade.md)
- [Logs and troubleshooting](admin/troubleshooting.md)

### Reference

- [Reference](reference/README.md)
- [Protocols matrix](reference/protocols.md)
- [Changelog](reference/changelog.md)

[Русская версия](../ru/README.md)
