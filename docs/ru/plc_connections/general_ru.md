# PLC-соединения

## Назначение модуля

Модуль **PLC Connections** предназначен для настройки и управления соединениями между **Faceplate Runtime** и внешними устройствами/системами автоматизации:

- **PLC/RTU/IED** (контроллеры, терминалы, релейная защита)
- **Счётчики и измерители** (электросчётчики, теплосчётчики и т.д.)
- **OPC-серверы**
- Прочие источники технологических данных через промышленные протоколы

Через PLC-соединения система получает и/или отправляет:

- **Теги/сигналы** (AI/DI/DO/AO)
- **События и аварии**
- **Служебные статусы связи**
- **Команды управления** (если разрешено конфигурацией)

---

## Как используются PLC-соединения

PLC-соединения применяются для:

1. **Сбора телеметрии** Чтение значений датчиков, состояний, измерений.

2. **Отправки команд** Дискретное управление, уставки, подтверждения и т.д.

3. **Интеграции со сторонними системами** OPC DA/UA, шлюзы, SCADA-системы, RTU-концентраторы.

4. **Мониторинга доступности** Диагностика канала связи, статусы подключения, статистика обмена.

---

# Клиентские и серверные соединения

## Клиентское соединение (Client connection)

**Client connection** означает, что **Faceplate инициирует подключение** к удалённой стороне:

- Faceplate сам подключается по IP/порту (или по COM-порту)
- выполняет обмен по протоколу
- получает/передаёт данные

**Примеры:**
- IEC-104 Client → подключение к серверу РЗА/RTU
- Modbus Client → опрос устройства по TCP/RTU
- OPC UA Client → чтение данных с OPC UA сервера

---

## Серверное соединение (Server connection)

**Server connection** означает, что **Faceplate слушает входящие подключения** (принимает соединение как сервер):

- внешнее устройство/система подключается к Faceplate
- Faceplate обслуживает входящие запросы/сеансы
- выдаёт данные или принимает команды

**Примеры:**
- IEC-104 Server → верхняя SCADA подключается к Faceplate
- OPC UA Server → клиенты читают значения из Faceplate

---

# Поддерживаемые типы PLC-соединений

Ниже перечислены типы, доступные в папке **/plc**.

## Клиентские соединения (поддерживаемые)

- **plc_iec101_client_connection** → [IEC-101 Client](./plc_iec101_client_connection_ru.md)
- **plc_iec104_client_connection** → [IEC-104 Client](./plc_iec104_client_connection_ru.md)
- **plc_opcua_client_connection** → [OPC UA Client](./plc_opcua_client_connection_ru.md)

---

## Серверные соединения (поддерживаемые)

- **plc_iec101_server_connection** → [IEC-101 Server](./plc_iec101_server_connection_ru.md)
- **plc_iec104_server_connection** → [IEC-104 Server](./plc_iec104_server_connection_ru.md)
- **plc_opcua_server_connection** → [OPC UA Server](./plc_opcua_server_connection_ru.md)

---

## Прочие соединения (общие типы)

- **plc_ethernet_ip_connection** → [EtherNet/IP](./plc_ethernet_ip_connection_ru.md)
- **plc_mbus_connection** → [M-Bus](./plc_mbus_connection_ru.md)
- **plc_modbus_connection** → [Modbus](./plc_modbus_connection_ru.md)
- **plc_opcda_connection** → [OPC DA](./plc_opcda_connection_ru.md)
- **plc_s7_connection** → [Siemens S7](./plc_s7_connection_ru.md)
- **plc_snmp_connection** → [SNMP](./plc_snmp_connection_ru.md)

---

# Создание PLC-соединения

*Шаг 1.* В дереве проекта перейдите в директорию, где будет находиться PLC-соединение.
*Шаг 2.* Нажмите кнопку **«Создать»**.
*Шаг 3.* В дереве объектов откройте раздел **plc**.
*Шаг 4.* Убедитесь, что отображается список доступных типов соединений.
![PLC folder1](images/create_plc_connection_1.gif)
*Шаг 5.* Выберите необходимый тип соединения.
*Шаг 6.* Нажмите кнопку **«OK»**.
*Шаг 7.* Откроется окно конфигурации соединения.
![PLC folder2](images/create_plc_connection_2.gif)