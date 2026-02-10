# Historian Server Configuration Guide

## 1. Introduction

This document provides a technical description of the configuration and operation of the Historian server as part of the Faceplate Studio SCADA system. The document is intended for system administrators and automation engineers.

## 2. Data Storage Architecture

### 2.1. Server Types

The Faceplate Studio SCADA system implements two primary server types for historical data storage:

- **Runtime Server** — the core system component responsible for real-time data processing and forwarding data to other system components.
- **Historian Server** — a dedicated server for long-term archival data storage. Using the Historian server offloads the Runtime server and enables the use of hardware optimized for historical data storage and analysis tasks.

### 2.2. Benefits of Distributed Architecture

**Reliability and fault tolerance:** using multiple servers increases system fault tolerance through workload distribution and data redundancy.

### 2.3. Data Storage Schemes

The system supports the following configurations:

1. **Runtime Server** — data storage on the primary processing server.
2. **Runtime Server + Historian Server** — distributed storage with a dedicated server for archival data.

To select the optimal storage scheme, configure the archiving parameters described in the following section.

## 3. Database Configuration

The database in Faceplate Studio is organized into three main sections: Runtime, Log, and Timeseries. Each section is responsible for storing a specific type of data.

### 3.1. Runtime Section

The Runtime section is used to configure parameters for receiving and storing real-time data.

![Runtime section configuration](/Historian/images/img_1.png)

*Figure 1 — Runtime section configuration in the database interface*

The figure shows the data storage configuration for the `fp@main-rt-server2.fp` server. The system supports the following storage modes:

- **`:atom:disc:`** — disk storage using the **`:atom:zaya_rocksdb`** module.
- **`:atom:ram:`** — in-memory storage using the **`:atom:zaya_ets`** module.
- **`:atom:ramdisc:`** — combined storage (RAM + disk) via the **`:atom:zaya_ets_rocksdb`** module.

### 3.2. Log Section

The Log section is used to configure parameters for receiving, storing, and managing system messages (alarms, events).

![Log section configuration](/Historian/images/img_2.png)

*Figure 2 — Log section configuration for alarm storage*

The configuration defines storage parameters for the `fp@main-his-server1.fp` server. Key parameters:

- **`:atom:dir:`** — path to the directory for alarm data storage.
- **`:atom:disc:`** — uses the **`:atom:zaya_rocksdb`** module for disk storage without additional parameters.
- **`:atom:max_age:`** — alarm retention period in days. Once the specified period expires, the database for the corresponding time range is deleted along with all alarms it contains.
- **`:atom:read_only_age:`** — data age in days at which the corresponding database (shard) is switched to read-only mode. In this mode, write and modification operations are prohibited, and inter-node synchronization for this shard is disabled.
- **`:atom:shard_depth:`** — time range in days covered by a single database shard. All alarms created within this range are assigned to the corresponding shard.

### 3.3. Timeseries Section

The Timeseries section is used to configure parameters for receiving, storing, and managing time-series archival data.

![Timeseries section configuration](/Historian/images/img_3.png)

*Figure 3 — Timeseries section configuration with RocksDB settings*

This configuration defines the RocksDB-based archive storage parameters. Key parameters:

- **`:atom:buffer_limit:`** — buffer size limit (1 GB).
- **`:atom:nodes:`** — specifies the storage node with the directory for data placement.
- **`:atom:remove_age:`** — data retention depth. Data older than the specified period (e.g., 365 days) is automatically deleted.
- **`:atom:open_options:`** — RocksDB database open and operation settings:
  - Block size: 32 KB;
  - Compression: lz4;
  - Level-0 compaction triggers;
  - Limits: level size — 1 GB, number of files — 512, background tasks — 16;
  - Write buffers: 128 MB, maximum 4 buffers.
- **`:atom:read:`** — read with caching, without checksum verification.
- **`:atom:write:`** — asynchronous data write.
- **`:atom:shard_depth:`** — data sharding depth in days.

This configuration is optimized for high performance and long-term archival data storage.

## 4. Historian Server Attachment Procedure

Attaching the Historian server to the system is required to enable storage for Timeseries (archives) and Log (messages) data types. The procedure is performed in the following sequence:

### 4.1. Starting the Historian Server

Start the Historian server specifying the Runtime server to which it will be attached. Use the following command:

```
env ATTACH_TO=fp@rt-server2.fp ./bin/fp_historian console
```

where:

- **ATTACH_TO=fp@rt-server2.fp** — environment variable specifying the name of the Runtime server to which the Historian server is being attached;
- **./bin/fp_historian** — executable file for starting the Historian server;
- **console** — server startup mode (console mode with log output to the terminal).

### 4.2. Database Configuration

Add the Historian server to the database configuration by performing the following steps:

1. Open the database object in the system configuration interface.
2. Modify the Log and Timeseries sections by specifying the Historian server as the data storage node.
3. Specify the storage path for Log and Timeseries data on the Historian server.
4. Compile and save the configuration file.

### 4.3. Configuration Verification

Check the Faceplate and Historian server logs for errors. This is necessary to confirm that the Historian server connection and configuration are correct.

### 4.4. Removing the Runtime Server from Storage Configuration

After successful data migration and operational verification, remove the Runtime server from the storage node list in the database object. This ensures that all archival data is stored exclusively on the Historian server.

### 4.5. Final Verification

Perform a final review of the system logs to confirm correct operation and the absence of errors after reconfiguring the data storage.
