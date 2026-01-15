# Git Integration in Faceplate

Faceplate features a built-in tool for version control based on Git. This allows you to manage changes (commits, branches, rollbacks) and synchronize with external repositories (GitLab) directly from the Studio interface.

The module consists of three sections:
1.  **Settings**
2.  **Local Diff**
3.  **Remote Diff**

---

## 1. Settings

Before starting, you must configure the connection to the remote repository. Two modes are available:

### A. Clone
Used when a project already exists in GitLab and needs to be copied into Faceplate. This is useful for working on existing components.

* **Username / Password:** GitLab credentials for authentication.
* **Remote URL:** The HTTPS link to the repository (copied from the GitLab interface).
* **Branch name:** The name of the working branch.
* **Project prefix (Context folder):** The path to the project folder inside the GitLab repository. This allows you to work with a specific project within a larger repository.

### B. Init (Initialize)
Used to initialize a new GitLab repository or link the current local project to an empty project in GitLab.

* Requires the same authentication and URL fields as Cloning.
* **Init Button:** Initializes the repository.
* **Reset Button:** Appears after initialization; allows you to delete the local project if necessary.

---

## 2. Managing Changes

### Local Diff
This section manages changes on your local machine.

**Workflow:**
1.  **Commit:** Saves current changes to the local version history. You must enter a commit message (e.g., "first commit").
2.  **Push:** Sends the committed changes to the remote GitLab server.

After executing the `Push` command, the data will be updated and visible in the GitLab web interface.

### Remote Diff
This section is for synchronizing your local project with data on the server.

**Available Commands:**
* **Pull:** Downloads and applies changes from the remote repository to your local project.
* **Rollback:** Reverts the project to the state of the last commit. **Warning:** All uncommitted changes made after the last commit will be permanently lost.
* **Rebase:** Merges changes from one branch into another, maintaining the order of commits.

---

## Recommendations
* Use **Clone** to integrate existing projects.
* Perform **Commits** regularly to save your change history.
* It is recommended to **Pull** before starting work to ensure you have the latest version of the project from other developers.
