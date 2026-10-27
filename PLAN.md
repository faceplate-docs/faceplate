# План наполнения документации

Статусы: `—` заглушка · `черновик` · `на проверке` · `готово`.
Приоритет: **1** — материал уже есть, переносим и дорабатываем; **2** — нужно собрать из кода и проекта; **3** — нужны скриншоты и проверка на стенде.

Источники — материалы из рабочей папки `faceplate` (не входят в репозиторий).

## Обзор

| Страница | Пр. | RU | EN | Источники |
|---|---|---|---|---|
| overview/README.md | 1 | — | — | `Faceplate_brochure.md`, `00 Обзор проекта.md` |
| overview/architecture.md | 1 | — | — | `00 Обзор проекта.md` (список приложений `apps/*`), брошюра (стек) |
| overview/glossary.md | 1 | черновик | — | — |

## Оператору

| Страница | Пр. | RU | EN | Источники |
|---|---|---|---|---|
| operator/getting-started.md | 3 | — | — | стенд |
| operator/monitoring.md | 3 | — | — | экран `monitoring_objects` (`fp_grid`), стенд |
| operator/control.md | 3 | — | — | `Faceplate_pump_control.md` (пульт управления) |
| operator/alarms.md | 3 | — | — | стенд, `fp_alarm` |
| operator/trends.md | 3 | черновик | — | `operator/Архивы и Тренды.md` (разд. 5–7), стенд, виджет `rt.js` |
| operator/reports.md | 2 | — | — | выгрузка архивов в CSV/JSON |

## Инженеру проекта

| Страница | Пр. | RU | EN | Источники |
|---|---|---|---|---|
| engineer/project-model.md | 2 | — | — | код `fp`, заметки по путям `/root/FP/...` |
| engineer/query-language.md | 2 | — | — | `Faceplate_API_Reference.docx`, примеры запросов `get … from … where` |
| engineer/connections/* | 2 | — | — | код `git/fp/apps/fp_*` (протоколы) |
| engineer/archives.md | 1 | — | — | `fp_archive_module.md`, `fp_userlib_archive_handler`, `archive_filter_example.json` |
| engineer/alarms.md | 2 | — | — | код `fp_alarm` |
| engineer/calculations.md | 2 | — | — | код `fp_calculation`, заметки по полю `script` |
| engineer/scripts.md | 2 | — | — | `fp_prototype_SE_node.erl`, `fp_script`, `fp_script_js` |
| engineer/graph-engine.md | 1 | — | — | `fp_graph_engine/fp_graph_engine.md` |
| engineer/screens/README.md | 2 | — | — | схемы проекта |
| engineer/screens/grid.md | 1 | — | — | `fp_grid/*.scn`, документ `fp_grid_style.md` |
| engineer/screens/js-libraries.md | 1 | — | — | заметки по `fp.rt.load_library`, `tagSubscribe`, записи полей |
| engineer/screens/ui-elements.md | 1 | — | — | `fp_ui/README.md`, документ `fp_ui_style.md` |
| engineer/versioning.md | 1 | — | — | `fp_git_module_api.md`, `fp_git_ui/README.md` |
| engineer/api/README.md | 1 | — | — | `Faceplate_API_Reference.docx` |
| engineer/api/objects-crud.md | 1 | — | — | `Faceplate_API_CRUD_Examples.docx` |
| engineer/api/archives-api.md | 1 | — | — | `fp_archive_read_write_api.md`, `fp_userlib_system_utils.md` |

## Администратору

| Страница | Пр. | RU | EN | Источники |
|---|---|---|---|---|
| admin/requirements.md | 2 | — | — | брошюра (масштаб), стенд |
| admin/installation.md | 2 | — | — | `bin/faceplate foreground`, шаблон systemd |
| admin/configuration.md | 2 | — | — | конфиги релиза (DB, FP_TS, logs, порты) |
| admin/docker.md | 2 | — | — | схема запуска в контейнерах, Dockge |
| admin/projects.md | 2 | — | — | схема переключения проектов |
| admin/users-access.md | 2 | — | — | код `fp_auth` |
| admin/replication.md | 2 | — | — | код `fp_replica`, брошюра (DataBridge) |
| admin/backup-restore.md | 3 | — | — | стенд |
| admin/upgrade.md | 3 | — | — | стенд |
| admin/troubleshooting.md | 2 | — | — | `fp_graph_engine.md` (отладка из шелла), опыт поддержки |

## Справочник

| Страница | Пр. | RU | EN | Источники |
|---|---|---|---|---|
| reference/protocols.md | 2 | черновик | — | код `git/fp/apps` |
| reference/changelog.md | 3 | черновик | — | история релизов |
