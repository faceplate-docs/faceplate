# Документация FACEPLATE

FACEPLATE — SCADA/EMS-платформа для промышленных и энергетических предприятий: сбор данных с ПЛК, историзация, расчёты, цифровые двойники и веб-интерфейс оператора в одном продукте.

Документация описывает платформу версии 4.0.x. <!-- TODO: уточнить версию -->

## Выберите свой раздел

| Если вы… | Начните с |
|---|---|
| диспетчер или оператор | [Руководство оператора](operator/README.md) |
| инженер, который создаёт проект | [Руководство инженера проекта](engineer/README.md) |
| администратор или DevOps | [Руководство администратора](admin/README.md) |
| впервые знакомитесь с платформой | [Обзор платформы](overview/README.md) |

## Содержание

### Обзор

- [Обзор платформы](overview/README.md)
- [Архитектура](overview/architecture.md)
- [Глоссарий](overview/glossary.md)

### Оператору

- [Руководство оператора](operator/README.md)
- [Вход в систему и интерфейс](operator/getting-started.md)
- [Мониторинг объектов](operator/monitoring.md)
- [Управление оборудованием](operator/control.md)
- [Тревоги и события](operator/alarms.md)
- [Тренды и архивы](operator/trends.md)
- [Отчёты и выгрузка данных](operator/reports.md)

### Инженеру проекта

- [Руководство инженера проекта](engineer/README.md)
- [Модель проекта: объекты, прототипы, поля](engineer/project-model.md)
- [Язык запросов](engineer/query-language.md)
- [Связь с оборудованием](engineer/connections/README.md)
  - [Modbus](engineer/connections/modbus.md)
  - [МЭК 60870-5-101/104](engineer/connections/iec-104.md)
  - [OPC UA / OPC DA](engineer/connections/opc-ua.md)
  - [IoT: MQTT, HTTP, WebSocket](engineer/connections/iot.md)
  - [Прочие протоколы](engineer/connections/other-protocols.md)
- [Архивы](engineer/archives.md)
- [Настройка тревог](engineer/alarms.md)
- [Расчёты (fp-calculation)](engineer/calculations.md)
- [Серверные скрипты](engineer/scripts.md)
- [Топологическая раскраска схем (graph_engine)](engineer/graph-engine.md)
- [Экраны и мнемосхемы](engineer/screens/README.md)
  - [Таблицы (элемент Grid)](engineer/screens/grid.md)
  - [JS-библиотеки на фронте](engineer/screens/js-libraries.md)
  - [Готовые UI-элементы](engineer/screens/ui-elements.md)
- [Версионирование проекта (fp_git)](engineer/versioning.md)
- [API платформы](engineer/api/README.md)
  - [API объектов (CRUD)](engineer/api/objects-crud.md)
  - [API архивов](engineer/api/archives-api.md)

### Администратору

- [Руководство администратора](admin/README.md)
- [Системные требования](admin/requirements.md)
- [Установка](admin/installation.md)
- [Конфигурация](admin/configuration.md)
- [Запуск в контейнерах](admin/docker.md)
- [Проекты и запуск на чистой БД](admin/projects.md)
- [Пользователи и права доступа](admin/users-access.md)
- [Резервирование и репликация](admin/replication.md)
- [Резервное копирование и восстановление](admin/backup-restore.md)
- [Обновление платформы](admin/upgrade.md)
- [Журналы и диагностика](admin/troubleshooting.md)

### Справочник

- [Справочник](reference/README.md)
- [Сводная таблица протоколов](reference/protocols.md)
- [История изменений](reference/changelog.md)

[English version](../en/README.md)
