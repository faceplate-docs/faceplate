# Project import and export

For the integration engineer who moves a project between servers or keeps a backup of it: how to save the project to a `project.fp` file and load this file into a project.

# Contents

- [Introduction](#introduction)
- [Main part](#main-part)
    - [Export](#export)
    - [What the file does not include](#what-the-file-does-not-include)
    - [Importing an export file](#importing-an-export-file)
- [Conclusion](#conclusion)

# Introduction

The `project.fp` export file holds the project objects. It is used to move the whole project or separate sections to another server and to keep a backup of the project before major changes. The file is also used in a FACEPLATE update, see [«FACEPLATE version and update»](../../administration/update/update.md).

You need access to Studio (`http://<server>:9000/fp/studio`) with an account that may change the project.

# Main part

## Export

The **Export project to file** and **Import project from file** buttons are the third and fourth icons from the top on the right vertical toolbar of Studio: the upper marked one is export, the lower one is import.

![Project export and import buttons on the Studio right toolbar](images/import_export_01_toolbar_buttons.png)

![Project export window with the list of sections](images/import_export_02_export.png)

Click **Export project to file**. The project is written to the file by sections. In the **ignore** list, check the sections that do not need to be saved: the export skips the checked sections and saves all unchecked ones to the file. To save the whole project, leave the list empty. Click **save**. The browser saves `project.fp`.

Sections in the **ignore** list:

| Section | What it holds |
|---|---|
| `global_libraries` | [Library modules](../../project_logic/library_modules/library_modules.md) and [JS libraries](../../project_logic/js_library/js_library.md) |
| `environment` | [Image library](../../mnemo/images.md), [localization dictionary](../localization/localization.md) and project system settings: [alarms](../../alarms/alarm/alarm.md), authorization, [graphic editor](../../mnemo/editor.md) and others |
| `primitives` | [Primitives](../primitives/primitives.md) |
| `catalogs` | [Catalogs](../catalogs/catalogs.md) |
| `prototypes` | [Prototypes](../prototypes/prototypes.md) |
| `usergroups` | [Roles](../../access/roles.md) |
| `users` | [Users](../../access/users.md): accounts without passwords. After the import, passwords are set again, see [«Users», section «Password»](../../access/users.md#password) |
| `project` | The project tree: folders, objects, screens |
| `user_rights` | [Role rights on screens](../../access/roles.md#rights-on-screens): viewing and changing |

## What the file does not include

Accumulated archive values and event log records are kept in the node database and are not part of the file. After an import into an empty database, the project archives are empty and fill up anew.

## Importing an export file

1. Click **Import project from file** and pick `project.fp` with **Select files...**.
2. Turn on the **Delete**, **create** and **Update** switches in the combination you need, see the table of combinations below. In **ignore**, check the same sections as on export; for a file of the whole project, leave the list empty. Click **save**.

    ![Project import window: file selected, create on](images/import_export_03_import.png)

3. Wait for `The project was imported successfully` and reload the page. The project folders and objects appear in the tree.

The import window matches the objects of the file and of the project by path. The switches define what to do with the differences:

| Switch | What it does |
|---|---|
| **Delete** | Deletes the project objects that are not in the file |
| **create** | Creates the file objects that are not in the project. Does not change objects that already exist |
| **Update** | Writes the field values from the file into the objects that exist both in the file and in the project. It is turned on together with **create** |

Switch combinations:

| Turned on | Object only in the file | Object in the file and in the project | Object only in the project | When to use |
|---|---|---|---|---|
| **create** | Created | Not changed | Stays | Moving the project into an empty database; adding what is missing without overwriting changes made in the project |
| **create** and **Update** | Created | Gets the fields from the file | Stays | Bringing in changes from the file and keeping the objects created only in this project |
| **Delete** and **create** | Created | Not changed | Deleted | Removing extras and adding what is missing without overwriting changes in shared objects |
| **Delete**, **create** and **Update** | Created | Gets the fields from the file | Deleted | Making the project an exact copy of the file |
| **Delete** | Not created | Not changed | Deleted | Only removing from the project what is not in the file |

An import with **Delete** also deletes objects created in the project after the file was made. Before such an import, save an export file of the current project: what was deleted can be restored from it by an import with **create**.

The **ignore** list on import must match the list the file was exported with. Sections checked on export are absent from the file, and an import with **Delete** removes their contents from the project. For example, if `users` and `usergroups` were checked on export but not on import, the import deletes the users and roles of the project, including the built-in ones.

If it is unknown which sections were checked on export, an import without **Delete** does not harm the project: **create** and **Update** do not touch sections that are absent from the file. To turn **Delete** on, check in **ignore** the sections that must stay in the project as they are: the import neither changes nor deletes the checked sections.

# Conclusion

The export file is saved with **Export project to file**: with an empty **ignore** list it holds the whole project, with checked sections it holds the project without them. It is imported with **Import project from file** and the same **ignore** list as on export. The **Delete**, **create** and **Update** switches are chosen by the table of combinations. Archive values and the event log are not part of the file.
