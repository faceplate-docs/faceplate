# Users

A document for the integration engineer who creates accounts for operators and other users of the project.

# Contents

- [Glossary](#glossary)
- [Introduction](#introduction)
- [Main part](#main-part)
    - [User list](#user-list)
    - [Creating a user](#creating-a-user)
    - [User card](#user-card)
    - [Password](#password)
    - [User roles](#user-roles)
    - [Logging in to Studio and Runtime](#logging-in-to-studio-and-runtime)
    - [Deleting a user](#deleting-a-user)
- [Conclusion](#conclusion)

# Glossary

| Term | Meaning |
|---|---|
| User | An account for logging in to Studio and Runtime: login, password, roles and rights on screens |
| Role | A named set of rights on screens. A user gets the rights of all their roles. See [Roles and access rights](roles.md) |
| Personal rights | Rights on screens given to the user directly, not through a role |

# Introduction

A FACEPLATE user is the account a person logs in with to Studio or Runtime. It holds the login and password, contact details, roles and personal rights on screens. Roles and rights decide which screens the person sees in Runtime and whether they can change values on them.

The section is in the Studio main menu: **User rights** → **Users**.

The running example is the shift operator `ivanov` with the role `shift_operators`.

You will need access to Studio (`http://<server>:9000/fp/studio`) with an account that is allowed to change the project.

# Main part

## User list

On the left is the list of project users, with the delete (bin) and create (**+**) buttons and a search box above it. Search finds users whose login starts with the entered text. It searches for three or more characters; a shorter text shows the whole list. The built-in accounts `system` and `admin` are not shown in the list.

Click a user to open their card on the right.

## Creating a user

Click **+**, enter the login in the "Define name" window and click **OK**.

The new user can log in at once: the password equals the login, the role is `operators`, there are no personal rights. Open the card, set the password, roles and rights, and save.

## User card

![User card](images/users_01_user.png)

| Field | Purpose |
|---|---|
| **Login** | Name used to log in |
| **Password**, **Retype password** | New password, see [Password](#password). Empty fields keep the current password |
| **Roles** | User roles, see [User roles](#user-roles) |
| **Memory Limit (MB)** | Memory limit the server gives to the user's session. Empty means the server default |
| **Email** | Address in the form `name@server.com` |
| **Phone** | 11 digits, optionally starting with `+`. Several numbers are separated by commas |

The table below the fields shows the user's rights on screens: own (**User rights**), received through links (**External links**) and through roles (**Role rights**). Only the **User rights** columns can be changed; the others show the result. The columns are explained in [Roles and access rights, section "Rights on screens"](roles.md#rights-on-screens).

**Save** stores the changes; **Cancel** and the arrow left of the title close the card without saving.

## Password

Password requirements:

- at least 6 characters;
- only Latin letters, digits and the characters `!@#$%^&*_-`;
- at least one lowercase and one uppercase letter, one digit and one character from the list above.

The **Retype password** field becomes available once the password meets the requirements. If the retyped password does not match, **Save** shows a password mismatch message and the password stays unchanged.

Example: `Demo_123`.

## User roles

In the **Roles** list, select the user's roles. The user gets the rights of all selected roles together with their personal rights.

Every user has the `operators` role: if you remove it, it comes back after saving. Therefore rights given to the `operators` role go to all users.

To let the user work in Studio, give them the `.administrators` role. Other roles are created in **User rights** → **Roles**, see [Roles and access rights](roles.md).

In the example `ivanov` has the roles `operators` and `shift_operators`, and personal Read and Write rights on `/mnemo_demo`.

## Logging in to Studio and Runtime

Studio (`http://<server>:9000/fp/studio`) and Runtime (`http://<server>:9000/fp/runtime`) use the same login and password from the card.

Studio opens only for users with the `.administrators` role. Other users see an access denied message after logging in.

Runtime opens for any user. Its **Screens** menu lists only the screens the user has rights on, see [Roles and access rights, section "What the user sees in Runtime"](roles.md#what-the-user-sees-in-runtime).

## Deleting a user

Select the user, click the bin and confirm with **yes**.

# Conclusion

Workflow:

1. **User rights** → **Users** → **+** → login → **OK**.
2. In the card set a password that meets the requirements, the roles and, if needed, personal rights on screens. **Save**.
3. For work in Studio add the `.administrators` role.
4. Check the result: log in to Runtime as the user and open **Screens**.
