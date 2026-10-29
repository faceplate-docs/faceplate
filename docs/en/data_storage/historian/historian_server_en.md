# Purpose

Historian Server is a specialized high-performance node designed for the accumulation, long-term storage, and rapid retrieval of large amounts of data (time series and event logs).

Using a dedicated Historian server allows you to implement the concept of data separation:

* Runtime data: processing operational information "in memory" for instant control.  
* Historical data: deep archival storage for subsequent analysis, trending, and reporting.

# Architecture

The storage subsystem is based on the Ecomet DBMS \- an object-based database.

## Storage model

* Metadata (RocksDB): highly reliable storage of object configurations, their attributes, and relationships. Provides a graph structure for the project (object tree).  
* Timeseries Engine: A proprietary engine for recording streaming data from devices. Optimized for high-density sequential recording (thousands of changes per second).  
* Hybrid access: using RAM for instant access to data slices (Snapshots) and disk for archives.

# Data optimization mechanisms

## Sharding

Data in Historian is divided into time segments called shards.

* Each shard represents a separate set of files for a fixed interval (e.g. 1 hour or 1 day).  
* This allows the system to perform cold backups by simply copying files from completed shards and instantly remove obsolete data.

## Compression

To minimize the load on the disk subsystem, the LZ4 compression algorithm is used. It allows for a 5-10x reduction in stored data volume with virtually no loss in processor performance, which is critical for systems with archive depths of several years.

# Data retention policy

The data life cycle is managed through the max\_age parameter.

* Automatic cleanup: The system cyclically checks shard expiration dates. If a shard completely exceeds its max\_age, it is permanently deleted.  
* Flexible settings: Storage periods can be configured individually for different types of data (e.g. archived data \- 1 year, messages \- 1 month).

# Distributed work and scalability

Historian can operate in various configurations:

* Dedicated node: on a separate server for load balancing. Launch with the command:  
  * env ATTACH\_TO=fp@runtime-node.fp ./bin/fp\_historian console  
* Replication (Hot Standby): Supports hot standby, where data is written to both the primary and secondary Historian servers simultaneously.

A more detailed description of the settings is available at [the link](../storage/Storage_en.md) .

# Maintenance schedule

To ensure stable operation and prevent performance degradation of the Ecomet DBMS, the following rules must be observed:

## System requirements and limits

* Descriptor Limits: The ulimit \-n parameter must be set to at least 200,000. Failure to set the limit will result in a server crash when attempting to open new shards.  
* Disk space: At least 20% of the total disk space must be free. This is necessary for RocksDB's background compaction processes. When the disk is 80% full, system performance is considered critical.  
* Drive Type: High Load systems require Enterprise SSD/NVMe drives with a high write endurance (DWPD).

## Monitoring and security

* Audit: Regularly check write queues and database size.  
* Power: It is mandatory to use a UPS with a configured graceful shutdown script when the battery charge is low to maintain the integrity of RocksDB indexes.  
* Network Connectivity: When running Historian on a separate node, it is recommended to use a dedicated network interface (VLAN) to protect process traffic from delays.  

> _written by nkn_ 