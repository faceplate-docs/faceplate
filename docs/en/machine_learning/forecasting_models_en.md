# Forecasting models

> **Status:** Draft — the data structures below are taken from real project exports; the configuration UI and training workflow still need to be documented by the Faceplate team.

Faceplate includes machine-learning models that forecast process values
(for example electricity and power consumption of an object) from archived
history and optional external inputs. Models live in the project tree and are
managed through the **model control** object (`prototype@model_control`).

## Model identity

Every model is identified by its full path in the project tree. The path is
the unique key for a model and is used everywhere a model is referenced.

```
/PROJECT/KAZ/REGION/OBJECT/...
 │        │   │      └── object (site, substation, plant …)
 │        │   └───────── region
 │        └───────────── country level (may be absent in older projects)
 └────────────────────── project
```

In older projects the country level is absent: `/PROJECT/REGION/OBJECT/...`.
When matching paths between old and new projects, strip the `/KAZ/` segment.

## Model attributes

| Attribute | Description |
|---|---|
| Path | Unique key, see above. |
| Title | Human-readable name. |
| Type | What is forecast, for example power or electricity. TODO: full list of types. |
| `disabled` | Whether the model is switched off. Stored as a boolean (`:atom:true` / `:atom:false` in current exports). Disabled models are not trained or executed. |
| `input` | Historical input signals as `fp://` addresses. Called `historical [input]` in older projects. |
| `configuration` | JSON with per-horizon settings, see below. |
| `state` | JSON with per-horizon runtime status and quality metrics, see below. |

## Inputs

A model takes one or more inputs:

| Input | Role | Description |
|---|---|---|
| Historical signal | required | Archived values of the forecast quantity, referenced by `fp://` address, for example `fp://PROJECT/REGION/OBJECT/SIGNAL`. See [Archives](../Archives/Archives.md). |
| Weather | feature | Weather data for the object's location, used as an additional feature. |
| Maintenance requests | regressor | Planned repair / maintenance requests, used as a regressor. |

TODO: how weather and maintenance sources are connected and which fields
they provide.

## Horizons and configuration

A model can forecast on up to three horizons: `day`, `month` and `year`.
Each horizon is configured independently in the `configuration` JSON:

```json
{
  "day":   { "model_path": "xgb/...",     "input_range": 604800,  "output_range": 86400 },
  "month": { "model_path": "prophet/...", "input_range": 7776000, "output_range": 2592000 },
  "year":  { "model_path": "prophet/...", "input_range": 94608000, "output_range": 31536000 }
}
```

| Field | Description |
|---|---|
| `model_path` | Algorithm and model location. The first path segment names the algorithm: `xgb` (gradient boosting) or `prophet` (time-series decomposition). TODO: full list of supported algorithms and the meaning of the rest of the path. |
| `input_range` | Length of history used for training / inference, in seconds. |
| `output_range` | Length of the forecast, in seconds (for example `86400` = 1 day). |

TODO: other configuration fields (retraining schedule, hyper-parameters,
resampling).

## State and forecast quality

The `state` JSON holds the runtime status of each horizon:

```json
{
  "day":   { "status": "COMPLETE", "avg_fact": 1234.5, "avg_fore": 1250.1, "bias": 0.0126 },
  "month": { "status": "IDLE" },
  "year":  { "status": "ERROR" }
}
```

| Field | Description |
|---|---|
| `status` | `COMPLETE` — forecast produced; `IDLE` — not run yet / waiting; `ERROR` — last run failed. |
| `avg_fact` | Average actual value over the evaluation window. |
| `avg_fore` | Average forecast value over the same window. |
| `bias` | Systematic forecast error. TODO: exact formula and sign convention. |

TODO: where the evaluation window is defined, additional error metrics, and
how errors are surfaced in the Studio UI and in the Message module.

## Operations

TODO: creating a model in the UI, training and retraining, viewing the
forecast on a screen, disabling a model, bulk review of models.

For bulk review of all models in a project, use the
[project export](project_export_en.md).

---
Русская версия: [forecasting_models_ru.md](../../ru/machine_learning/forecasting_models_ru.md)
