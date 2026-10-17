# Project export

> **Status:** Draft — the format below is taken from real exports; the export procedure in the UI still needs to be documented by the Faceplate team.

A Faceplate project can be exported to an Excel workbook named
`faceplate_project-<N>.xlsx`, where `<N>` is the project number. The export
is the usual way to review all forecasting models of a project at once.

## Workbook structure

| Sheet | Contents |
|---|---|
| `prototype@model_control` | One row per forecasting model (required). |
| `Лист1` | Optional list of models that use the weather feature (model path in the second column). |
| `Лист2` | Optional list of models that use the maintenance regressor (model path in the second column). |

`Лист1` and `Лист2` are not always present; when a newer export lacks them,
the lists from an older export of the same project are still valid.

## Columns of `prototype@model_control`

| Column | Current format | Older format |
|---|---|---|
| Model path (key) | `prototype@model_control` | `prototype@model_control` |
| Historical inputs | `input` | `historical [input]` |
| Disabled flag | `:atom:true` / `:atom:false` | `True` / `False` |
| `configuration` | JSON, see [Forecasting models](forecasting_models_en.md) | same |
| `state` | JSON with `day` / `month` / `year` status and metrics | absent |
| `icon`, `nodes` | Large auxiliary columns; can be skipped when analysing | same |

Paths in `Лист1` / `Лист2` use the short form `/PROJECT/REGION/...`, while
the main sheet uses `/PROJECT/KAZ/REGION/...`. Remove the `/KAZ/` segment
before matching.

## Typical analyses

- List of models with region, object, type, status and inputs.
- Which models use weather or maintenance inputs.
- Algorithms per horizon (`xgb` / `prophet` × `day` / `month` / `year`).
- Forecast horizon ranges (`output_range` min / max / median).
- Coverage: objects that have both power and electricity models, only one, or none.
- Forecast quality per horizon from the `state` column.

TODO: how to trigger the export in the UI and whether other sheets or
object types are exported.

---
Русская версия: [project_export_ru.md](../../ru/machine_learning/project_export_ru.md)
