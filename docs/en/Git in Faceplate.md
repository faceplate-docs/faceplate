# Faceplate Git Module

## 1. General Overview
**The Git Module** is an integrated tool for version control within the Faceplate development environment. It allows for saving modification history, organizing collaborative work among multiple users, and synchronizing the local project with an external server (e.g., GitLab or GitHub).

### 1.1. Architecture
Version control in Faceplate is built on a three-level architecture that ensures autonomous operation and data safety.

Data Flow Diagram:
**Local Project ↔ Local Git Repository ↔ Remote Server (GitLab)**

#### Level Descriptions:
1.  **Local Project (Workspace):**
    * This is the current state of the project visible and editable in Studio (active mimic diagrams, tags, scripts).
    * *Important:* Changes at this level are not yet protected by version history. If an object is deleted here, it cannot be recovered without Git.
2.  **Local Git Repository (Version Base):**
    * A hidden archive located on the same physical server (node) where Faceplate is installed.
    * The **Commit** command moves a "snapshot" of the project from the workspace to this archive.
    * This provides a full history and the ability to **Reset** locally without a network connection.
3.  **Remote Server (GitLab / GitHub):**
    * A centralized external storage system.
    * The **Push** command sends local commits to the server.
    * This ensures backup protection against local server failure and enables team collaboration via **Pull**.

---

## 2. Interface and Basic Commands
The module interface is divided into three tabs corresponding to the development life cycle: Settings, Local Diff, and Remote Diff.

### 2.1. Interface Tabs
* **Settings:** Used for configuring the repository connection, cloning (**Clone**), and initializing projects (**Init**).
* **Local Diff:** Manages current changes on the server. Includes commands for fixing (**Commit**), sending (**Push**), and resetting (**Reset**) data.
* **Remote Diff:** Interactions with the external repository. Used to retrieve updates (**Pull**), roll back versions (**Rollback**), or merge branches (**Rebase**).

### 2.2. Command Glossary
| Command | Description |
| :--- | :--- |
| **Commit** | Fixing a "snapshot" of current local changes with a description. |
| **Push** | Sending local commits to the remote server. |
| **Pull** | Downloading and applying changes from the remote server. |
| **Reset** | Canceling uncommitted changes (reverting to the last commit). |
| **Rollback** | Reverting the entire project to a specific past version. |
| **Rebase** | Rewriting local changes on top of the latest remote updates to maintain a linear history. |

---

## 3. Repository Configuration (Settings)

Before starting work, determine how the project connects to Git. Two scenarios are available:

### 3.1. Scenario A: Cloning (Clone)
Used if the project already exists in GitLab and needs to be downloaded to a new Faceplate server.

**Parameters:**
* **Remote URL:** HTTPS link to your repository.
* **Auth:** Login and Password (or Access Token) for GitLab.
* **Branch name:** The working branch (usually `main` or `master`).
* **Project prefix:** Path to the project folder inside the repository (allows storing multiple projects in one repository).

### 3.2. Scenario B: Initialization (Init)
Used to create a new repository from scratch or link a current local project to an empty GitLab repository.
* After filling in data, press **Init**.
* If an error occurs, a **Reset** button appears to allow re-initialization.

---

## 4. Procedures

### 4.1. Initial Setup and Deployment
**Prerequisites:**
* The Faceplate instance is deployed for cloning or initialization.
* Default administrator account is available: user **system** with password **111111**.

**Important:**
* All user settings will be deleted upon cloning.
* For the first login and after cloning, the default password can be used.
* **Validate Token/Password:** If using an Access Token, ensure it has `read_repository` and `write_repository` rights.
* **Check Project Prefix:** Ensure the path is correct to avoid pulling/pushing files to the wrong location.

**Cloning Steps:**
1.  Log in to Studio using the **system** account.
2.  Go to the "Users" section, create a new user with administrator rights, and set a memory limit.
3.  Switch to the newly created user.
4.  Go to the Git section, enter the required data, press **Clone**, and wait for the download to complete.
5.  The created user will be replaced by user accounts downloaded from the repository.
6.  Select an existing user with administrator rights (or create a new one), set a password, and switch to that user.
7.  Go to the Git section and re-enter the repository password; upon successful authentication, the user receives rights to work with Git.

### 4.2. Work Process (Git Workflow)

#### Step 1. Synchronization (Pull)
Before starting work, go to the **Remote Diff** tab and press **Pull**. This ensures you are working with the actual version and prevents overwriting others' edits. Check Studio to ensure objects display correctly after the update.

#### Step 2. Development and Verification
Perform changes. Before committing, check the functionality of created objects in Studio. Check the **Local Diff** tab to ensure only intended files are modified. Use **Reset** to revert accidental changes to specific files.

#### Step 3. Commit
1.  Enter a short, meaningful comment (e.g., *"Added pressure archive"*, not *"fix"*).
2.  Press **Commit**. Changes are saved to the local server history.

#### Step 4. Publish (Push)
Press **Push** to send committed data to GitLab. It is recommended to verify in the GitLab web interface that the commit appeared and the branch is updated.

---

## 5. Best Practices and Troubleshooting

### 5.1. "Clean" Development
* **Review Changes:** Before clicking **Commit**, scroll through the file list to check for accidentally deleted scripts or tags.
* **Task Separation:** If you completed two different tasks (e.g., alarms and button colors), make **two different commits**. This allows for rolling back one task without losing the other.
* **Reset System Parameters:** If you changed system parameters "for yourself" during testing (e.g., reduced polling periods), use **Reset** on those files before the final commit.

### 5.2. Conflicts and Collaboration
* **Rebase:** If two users modified the same screen, use **Rebase** instead of a simple Merge. This moves your commits to the end of the queue after your colleague's edits, keeping the history linear.
* **Check After Rebase:** Verify in Studio that your objects interact correctly with your colleague's objects.
* **Rollback:** If the project fails to start after a Pull, use **Rollback** to a previous stable commit (check the history description).

### 5.3. Historical Data and Archives
* **Structure Sync:** Git transfers the archive **structure** (field names, data types), but not the historical data (trends) itself.
* **Check Links:** After pulling a new archive, ensure the corresponding database or folder is created on your Faceplate node.

### 5.4. Shift Handoff
* **Empty Local Diff:** Before leaving, ensure the Local Diff tab is empty (all changes committed or reset).
* **Final Push:** Ensure the outgoing commit counter is zero. Data left only in the local repository is invisible to other users.
* **Status Comment:** The final commit of the day should be detailed (e.g., *"Boiler screen #1 80% done, pressure alarms not linked"*).

---

## 6. Practical Use Case: Collective Development
*Scenario: Two users working on one project.*

**Stage 1: Database Creation (User #1)**
1.  Creates `archive_pressure` and links a tag to it.
2.  In **Local Diff**, writes the message *"Added pressure archive"*, clicks **Commit**, then **Push**.
3.  Changes are now safe on the GitLab server.

**Stage 2: Adding Graphics (User #2)**
1.  Performs **Pull** in the **Remote Diff** tab. The archive created by User #1 appears in their project.
2.  Creates a mimic diagram, adds an **Input-Output field**, and links it to `archive_pressure`.
3.  Performs **Commit** (*"Added main screen"*) and **Push**.

**Stage 3: Finalization**
1.  User #1 performs **Pull**, receives the finished mimic diagram, and verifies the entire system in Runtime.