**Guide**: **Creating and Configuring a New Faceplate Cluster**

This document describes the process of deploying a new Faceplate cluster (Runtime and Historian), its initial configuration, and performance tuning.
![Пример кластера](/Redundancy/FP_cluster.png)
Faceplate cluster example

1\. **Infrastructure Preparation**

1.1. **Server Requirements**

\- Operating System: **Ubuntu Server 22.04.05 LTS and higher.**

\- Network: For local data exchange between servers, it is recommended to allocate a local subnet (e.g., 10.230.0.0/24), providing a communication channel of 1 Gb/s and higher.

1.2. **DNS and /etc/hosts Configuration**

A key factor for cluster operation is the correct configuration of local names.

1\. Open the /etc/hosts file on each server.

2\. Register the IP addresses and local names of all servers that will be part of the cluster.

Important: The content of /etc/hosts (the section with Faceplate node names) must be absolutely identical on all servers in the cluster. Without this, data exchange between nodes is impossible.

Configuration example:

**10.230.0.11 rt-server1.fp**

**10.230.0.12 rt-server2.fp**

**10.230.0.13 his-server1.fp**

2\. **Installation and Application Structure**

2.1. **File Placement**

The application must be deployed in the following directory structure:

\- /DATASET/project/scada/faceplate/ - application files (Runtime/Historian).

\- /DATASET/project/scada/local/ - database and local settings.

\- /DATASET/project/scada/local/logs/ - log files (console.log, error.log).

2.2. **Certificates**

For HTTPS connections to work, place the certificate files in the directory **/DATASET/project/scada/faceplate/etc/certs**:

**\- ca-chain.cert.pem**

**\- node.cert.pem**

**\- node.key.pem**

3\. **Basic Configuration (Tuning)**

Before launching, it is necessary to configure key configuration files located in **/DATASET/project/scada/faceplate/releases/4.0.6/** (and the **apps/** subfolder).

3.1. **vm.args** (**Erlang** Virtual Machine Settings)

In this file, you need to set unique parameters for each node:

\- -**name**: Specify a unique node name (e.g., [fp@rt-server1.fp](mailto:fp@rt-server1.fp)).

\- -**setcookie**: Set a single cookie for all servers in the cluster. This is the password for node interaction.

\- **+MIscs**: Flag for limiting literal memory (configured in megabytes).

3.2. **fp.logger.config** (Logging Configuration)

Configure the paths for log output in the console_handler and error_handler blocks. Ensure that the paths point to a correct folder, for example:

**\- /DATASET/project/scada/local/logs/console.log**

**\- /DATASET/project/scada/local/logs/error.log**

4\. **Launching and Assembling the Cluster**

Launching is performed in a tmux session (session name scada).

4.1. **Launching the First Node**

On the first server, execute the launch command in console mode:

./faceplate console

4.2. **Adding Remaining Nodes to the Cluster**

To connect subsequent servers (Runtime 2, Runtime 3, or Historian) to the cluster, the launch command needs to be executed once with the environment variable **ATTACH_TO**. It points to an already running node.

Command for adding a node:

**env ATTACH_TO=**[**fp@rt-server1.fp**](mailto:fp@rt-server1.fp) **./faceplate console** (Where [**fp@rt-server1.fp**](mailto:fp@rt-server1.fp) is the name of the first launched node). After successful addition to the cluster, use the regular command **./faceplate console** for subsequent restarts.

5\. Storage Configuration (**Faceplate Studio**)

After launching the cluster, it is necessary to configure the databases via Faceplate Studio (<http://xxx.xxx.xxx.xxx:90000/fp/studio>).

Settings are divided into three categories.

5.1. **Runtime** (Operational Data)

Configuration for storing tag values in real-time.

\- **Modules**: It is recommended to use a combination of **RAM** and disk

(**zaya_ets_rocksdb**) or only disk (**zaya_rocksdb**).

It is necessary that the number of nodes and parameters in "Storage Configuration" correspond; the config below is duplicated for the number of nodes.
```
":atom:fp@uzn-server1.fp": {":atom:disc": {":atom:module": ":atom:zaya_rocksdb",  
<br/>":atom:params": {}  
<br/>},  
<br/>":atom:ram": {  
<br/>":atom:module": ":atom:zaya_ets",  
<br/>":atom:params": {}  
<br/>},  
<br/>":atom:ramdisc": {  
<br/>":atom:module": ":atom:zaya_ets_rocksdb",  
<br/>":atom:params": {}  
<br/>}  
```
5.2. **Messages** (Logs and Alarms)

\- max_age: Set the storage period for alarms (in days).

\- shard_depth: Set the time range for one shard (database file) in days.

\- read_only_age: Data age after which the archive switches to "read-only" mode.

5.3. **Archives**

Settings for the long-term archive (usually based on RocksDB):

\- **remove_age**: Archive storage depth (e.g., 365 days).

\- **buffer_limit**: Write buffer limit (e.g., 1 GB).

\- **open_options**: Performance settings (block size 32 KB, lz4 compression, asynchronous write).

6.2. **Roles and Memory Limits**

In the "Permissions" section, configure users and their memory consumption limits:

\- Operators (monitoring): Recommended limit ~4000 MB.

\- Engineers (active work, log export): Recommended limit ~8000 MB.

6.3. **Launching in Service Mode**

After debugging the application project, it is intended to switch to running Faceplate in service mode.

An interactive installer is proposed.

Copy the script into a new file, place it next to the source distribution, name it "install_fp_service.sh", apply the command chmod +x install_fp_service.sh i.e., make it executable, and run ./install_fp_service.sh then follow the interactive mode of the script.
```
\# !/bin/bash  
<br/>\# ==========================================  
<br/>\# Interactive installer for 'foreground' service (WITHOUT LOGS)  
<br/>\# ==========================================  
<br/>\# --- Colors for output ---  
<br/>RED='\\033\[0;31m'  
<br/>GREEN='\\033\[0;32m'  
<br/>BLUE='\\033\[0;34m'  
<br/>YELLOW='\\033\[1;33m'  
<br/>NC='\\033\[0m' # No Color  
<br/>\# --- Functions ---  
<br/>print_info() {  
<br/>echo -e "\\n\${BLUE}INFO:\${NC} \$1"  
<br/>}  
<br/>print_success() {  
<br/>echo -e "\${GREEN}SUCCESS:\${NC} \$1"  
<br/>}  
<br/>print_error() {  
<br/>echo -e "\${RED}ERROR:\${NC} \$1"  
<br/>}  
<br/>\# === 1. CHECK FOR ROOT ===  
<br/>print_info "Starting 'foreground' service installer..."  
<br/>if \[ "\$EUID" -ne 0 \]; then  
<br/>print_error "This script must be run with root privileges."  
<br/>echo "Please run: sudo ./install_fg_service.sh"  
<br/>exit 1  
<br/>fi  
<br/>\# === 2. INTERACTIVE INPUT ===  
<br/>print_info "Please answer a few questions."  
<br/>echo "You can press Enter to use the default values (in brackets)."  
<br/>\# -e allows using auto-completion, -i sets the default value  
<br/>read -e -i "fp.service" -p " 1. Enter name for .service file: " SERVICE_NAME  
<br/>read -e -i "master" -p " 2. Enter username (User): " SERVICE_USER  
<br/>read -e -i "sudo" -p " 3. Enter group name (Group): " SERVICE_GROUP  
<br/>read -e -i "/DATASET/project/scada/faceplate" -p " 4. Enter full path to Faceplate folder: " FACEPLATE_PATH  
<br/>\# Remove / at the end if present  
<br/>FACEPLATE_PATH=\${FACEPLATE_PATH%/}  
<br/>\# === 3. VALIDATION ===  
<br/>print_info "Checking entered data..."  
<br/>\# Check that the binary exists  
<br/>EXEC_FILE="\$FACEPLATE_PATH/bin/faceplate"  
<br/>if \[ ! -f "\$EXEC_FILE" \]; then  
<br/>print_error "Binary NOT FOUND at path: \$EXEC_FILE"  
<br/>echo "Please check the path and try again."  
<br/>exit 1  
<br/>else  
<br/>print_success "Binary found: \$EXEC_FILE"  
<br/>fi  
<br/>\# Check user and group  
<br/>if ! id "\$SERVICE_USER" &>/dev/null; then  
<br/>print_error "User '\$SERVICE_USER' does not exist on the system."  
<br/>exit 1  
<br/>fi  
<br/>if ! getent group "\$SERVICE_GROUP" &>/dev/null; then  
<br/>print_error "Group '\$SERVICE_GROUP' does not exist on the system."  
<br/>exit 1  
<br/>fi  
<br/>print_success "User and group exist."  
<br/>\# === 4. FILE GENERATION ===  
<br/>\# Destination path  
<br/>SERVICE_DEST_FILE="/etc/systemd/system/\$SERVICE_NAME"  
<br/>print_info "Preparing unit-file..."  
<br/>\# Generate content of .service file into a variable  
<br/>SERVICE_CONTENT=\$(cat <<EOF  
<br/>\[Unit\]  
<br/>Description=Faceplate SCADA Application Service (Foreground)  
<br/>After=network.target  
<br/>\[Service\]  
<br/>\# !! Process runs in foreground  
<br/>Type=simple  
<br/>\# === DISABLE LOGS (DISK SAVING) ===  
<br/>StandardOutput=null  
<br/>StandardError=null  
<br/>\# =========================================  
<br/>User=\$SERVICE_USER  
<br/>Group=\$SERVICE_GROUP  
<br/>WorkingDirectory=\$FACEPLATE_PATH  
<br/>\# !! Run binary directly  
<br/>ExecStart=\$EXEC_FILE foreground  
<br/>Restart=always  
<br/>RestartSec=5  
<br/>LimitNOFILE=200000  
<br/>\[Install\]  
<br/>WantedBy=multi-user.target  
<br/>EOF  
<br/>)  
<br/>\# === 5. CONFIRMATION ===  
<br/>echo -e "\\n\${YELLOW}--- CHECK DATA ---\${NC}"  
<br/>echo "Service will be installed here: \${GREEN}\$SERVICE_DEST_FILE\${NC}"  
<br/>echo "File content:"  
<br/>echo -e "\${BLUE}---------------------------------\${NC}"  
<br/>echo "\$SERVICE_CONTENT"  
<br/>echo -e "\${BLUE}---------------------------------\${NC}"  
<br/>echo ""  
<br/>read -p "Is everything correct? (y/n): " confirm  
<br/>if \[ "\$confirm" != "y" \] && \[ "\$confirm" != "Y" \]; then  
<br/>echo "Installation cancelled."  
<br/>exit 0  
<br/>fi  
<br/>\# === 6. INSTALLATION ===  
<br/>print_info "Stopping old service (if it existed)..."  
<br/>systemctl stop "\$SERVICE_NAME" &>/dev/null  
<br/>print_info "1. Writing file to \$SERVICE_DEST_FILE..."  
<br/>echo -e "\$SERVICE_CONTENT" > "\$SERVICE_DEST_FILE"  
<br/>print_info "2. Reloading systemd daemons (daemon-reload)..."  
<br/>systemctl daemon-reload  
<br/>print_info "3. Enabling service autostart (enable)..."  
<br/>systemctl enable "\$SERVICE_NAME"  
<br/>print_info "4. Starting service \$SERVICE_NAME (start)..."  
<br/>systemctl start "\$SERVICE_NAME"  
<br/>\# === 7. FINAL ===  
<br/>print_success "Installation and launch completed!"  
<br/>echo "Checking service status (in 2 seconds):"  
<br/>sleep 2  
<br/>systemctl status "\$SERVICE_NAME"  
<br/>exit 0  
```
In case of recovery, it is necessary to launch Faceplate in Force mode.

To do this, launch the first node in the console according to point 4, the remaining nodes are launched in service mode.

After recovery is complete, the first node must be stopped in the console and switched to service mode.