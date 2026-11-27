# Catalogs

A document for the integration engineer who keeps reference data in the project as tables.

# Contents

- [Glossary](#glossary)
- [Introduction](#introduction)
- [Main part](#main-part)
    - [Creating a catalog](#creating-a-catalog)
    - [Fields](#fields)
    - [Records](#records)
    - [Searching records](#searching-records)
    - [Behaviour](#behaviour)
    - [Copying and deleting](#copying-and-deleting)
    - [Exporting and importing a catalog](#exporting-and-importing-a-catalog)
    - [Excel exchange](#excel-exchange)
    - [Catalog on a mnemonic diagram](#catalog-on-a-mnemonic-diagram)
- [Conclusion](#conclusion)

# Glossary

| Term | Meaning |
|---|---|
| Catalog | A reference data table of the project from the **Catalogs** section: a set of fields (columns), records (rows) and an optional Behaviour |
| Record | A row of a catalog. The record name (`.name`) is unique within the catalog |
| Behaviour | An Erlang module with the functions `on_create/1`, `on_edit/1`, `on_delete/1`. The server calls them when a record is created, edited and deleted |
| `.prt` file | The catalog export file: fields, records and Behaviour |

# Introduction

A catalog is a reference data table inside the project: equipment models, sensor types, reason codes, material parameters and any other lists that are easier to keep as a table than as a tree of objects. The catalog fields define the table structure, the records hold the data. Behaviour lets you check or complete records when they are saved.

The section is in the Studio main menu: **Catalogs**. Each catalog has three parts, each opened with its own button:

| Part | Button | Contents |
|---|---|---|
| **Content** | **Content** | The table of catalog records |
| **Fields** | **Fields** | Table columns: name, type, storage, index, default value |
| **Behaviour** | **Behaviour** | Erlang code that the server runs on operations with records |

The example used throughout is the sensor model catalog `sensor_models` with the fields `vendor` (manufacturer), `unit` (unit of measure), `range_min`, `range_max` (measuring range) and `certified` (calibration flag).

You will need access to Studio (`http://<server>:9000/fp/studio`) with an account that is allowed to change the project.

# Main part

## Creating a catalog

Open **Catalogs** in the Studio main menu. The table shows the name and comment of each catalog, the search line above the table searches by name.

![Catalogs in the Studio main menu](images/01_menu.png)

![Catalog list](images/02_list.png)

Click **Create**, fill in **Name** (required) and **Comment** and save. Empty Fields and Content are created together with the catalog.

![Catalog creation form](images/03_create.png)

After saving, the catalog appears in the list. To open it, select the catalog and click **Content**, **Fields** or **Behaviour**, or double-click it: Content opens. A navigation line appears above the table of the open catalog (**Catalogs / sensor_models / Content**): **Catalogs** returns to the list, the arrow next to the part switches between the catalog parts.

## Fields

Select the catalog and click **Fields**. The field form is the same as for a prototype: each parameter is described in [Prototypes](../prototypes/prototypes.md#fields), section "Fields". For a catalog the following matter:

| Parameter | Effect in a catalog |
|---|---|
| **Type** | The input control in the record form: `string` — text, `integer` and `float` — number, `bool` — switch |
| **Default value** | Prefilled in the form of a new record |
| **Index** | `3gram` enables search by part of a value with a query of 3 or more characters (section [Searching records](#searching-records) below) |
| **excel** | The field takes part in the Excel exchange (section [Excel exchange](#excel-exchange) below) |

Fields of the example: `vendor` and `unit` of type `string`, `range_min` and `range_max` of type `float` with default values `0` and `100`, `certified` of type `bool`. All fields have the **export** and **excel** flags set.

![Catalog fields](images/04_fields.png)

## Records

Select the catalog and click **Content**. The table columns are `.name` and the catalog fields.

![Catalog records](images/05_content.png)

Click **Create**, enter `.name` and the field values and save. An existing record opens on double-click.

![Record form](images/06_record_form.png)

> [!NOTE]
> The value `false` of a `bool` field is not shown in the table: the cell is empty. In the record form the switch is set to **off**.

## Searching records

Above the records table choose a column, enter a value and click **Search**. The cross button on the right resets the filter.

Letter case matters everywhere except one case: a text field with the `3gram` index and a query of 3 or more characters.

| Column | Query of 1–2 characters | Query of 3 or more characters |
|---|---|---|
| `.name` | By part of the name, case-sensitive: `PT` finds `PT_150`, `PT_3051` and `TT_PT100`, `pt` finds nothing | The same: `3051` finds `PT_3051` |
| A text field with the `3gram` index | By part of the value, case-sensitive: `Em` in `vendor` finds `Emerson`, `em` finds `Elemer` | By part of the value, case-insensitive: `Emer` and `emer` find `Emerson` and `Elemer` (`Elemer` contains `emer`) |
| A text field without `3gram` | By part of the value, case-sensitive: `Pa` in `unit` finds `kPa` and `MPa`, `pa` finds nothing | By exact value only, case-sensitive: `kPa` finds `kPa`, `kpa` finds nothing |
| A numeric or `bool` field | By exact value only: `20` does not find `200` | By exact value only: `200`, `true` |

![Search by part of a value](images/07_search.png)

## Behaviour

Select the catalog and click **Behaviour**. An Erlang code editor opens with a template of the module `fp_prototype_<catalog name>`:

| Function | When it is called |
|---|---|
| `on_create/1` | A record is created |
| `on_edit/1` | A record is edited |
| `on_delete/1` | A record is deleted |

The function receives the record object. Returning `ok` allows the operation. Raising an exception (`throw`) forbids it: the record is not created, changed or deleted, and the user sees the exception text. Click **Compile**, wait for `OK`, then **save**.

Example: check that the lower range limit is less than the upper one.

```erlang
-module(fp_prototype_sensor_models).

-include("fp.hrl").

-export([
    on_create/1,
    on_delete/1,
    on_edit/1
  ]).

on_create(Object)->
  check_range(Object).
on_edit(Object)->
  check_range(Object).
on_delete(_Object)->
  ok.

check_range(Object)->
  #{<<"range_min">> := Min, <<"range_max">> := Max} =
    fp_db:read_fields(Object, [<<"range_min">>, <<"range_max">>]),
  if
    is_number(Min), is_number(Max), Min >= Max ->
      throw(<<"range_min must be less than range_max">>);
    true ->
      ok
  end.
```

![Behaviour editor](images/08_behaviour.png)

A record with `range_min` = `10` and `range_max` = `5` is not saved: the **ERROR!** window shows the exception text, and the record form stays open with the entered values.

![Error from Behaviour](images/09_behaviour_error.png)

Behaviour also runs on Excel import. A row that fails the check is not changed, and the **ERROR!** window shows the record path and the exception text.

## Copying and deleting

Catalogs in the **Catalogs** list and records in **Content** are copied and deleted the same way.

**Copying.** Select a row, click **Copy**, then **Paste**. In the "Paste items?" window keep **Operation** = `copy`, set **Copies count** and click **OK**. The copy gets the suffix `_1`: `PT_150` → `PT_150_1`, `sensor_models` → `sensor_models_1`. A catalog copy gets all fields and records of the original.

**Deleting.** Select a row, click **Delete** and confirm with **yes**.

## Exporting and importing a catalog

**Export.** Select the catalog and click **Export**. The browser saves the file `catalog.prt` with the fields, records and Behaviour of the catalog.

**Import.** Click **Import**, turn on the modes, choose a `.prt` file with **Select files...** and save. On success the message "The catalog was imported successfully" appears.

![Catalog import](images/10_import.png)

| Switch | What it does |
|---|---|
| **create** | Creates fields and records from the file that do not exist in the catalog. Existing fields, records and Behaviour are not changed |
| **Update** | Overwrites existing fields, records and Behaviour with the values from the file |
| **Delete** | Deletes catalog fields and records that are not in the file |

## Excel exchange

Excel is convenient for filling in and editing records in bulk.

**Export.** In the **Catalogs** section click **Export .xlsx** on the right panel: the upper of the marked buttons. In the selection window select the catalogs (several with Ctrl) and click **Ok**. The **Select all** button exports all catalogs at once. The browser saves the file `faceplate_project.xlsx`.

![Excel exchange buttons on the right panel of Studio](images/11_xlsx_buttons.png)

![Selecting catalogs for export](images/12_xlsx_select.png)

Each catalog is a separate sheet `catalog@<catalog name>`. The first column is the record name, the others are the fields with the **excel** flag. `bool` values are written as `:atom:true` and `:atom:false`.

| catalog@sensor_models | certified | range_max | range_min | unit | vendor |
|---|---|---|---|---|---|
| PT_3051 | :atom:true | 1600 | 0 | kPa | Emerson |
| LT_80 | :atom:false | 35 | 0 | m | VEGA |

**Import.** Click **Import .xlsx** (the lower of the marked buttons), choose the file and click **ok**. In the `select_import_items` window select the sheets and click **OK**. A success message appears. Rows with new names create records, rows with existing names update them.

## Catalog on a mnemonic diagram

The operator picks a catalog record on a screen with the **CatalogSelect** element from the **Controls** palette: the `catalog` property sets the catalog, `value` is bound to a tag field, and the choice writes the full path of the record to the tag. Setup and Runtime behaviour are covered in [Selection from lists, section "Selecting a catalog record"](../../mnemo/lists.md#selecting-a-catalog-record).

# Conclusion

Working order for a catalog:

1. Create the catalog in **Catalogs**.
2. Describe the columns in **Fields**.
3. If needed, set record checks in **Behaviour**.
4. Fill in the records in **Content** or load them from Excel.
5. Move the catalog to another project with **Export** and **Import**.
