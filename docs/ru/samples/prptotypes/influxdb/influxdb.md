# Шаблон интеграции с базой временных рядов InfluxDB.

Решение использует встроенные механизмы Faceplate для работы с внешними API построенном по принципам REST  и протокола HTTPS. Передача данных осуществляется методом POST на эндпоинт InfluxDB API (v2.x).

Основные компоненты:
- Faceplate — HTTP-клиент, собирающий и отправляющий данные.
- HTTPS (TLS) — шифрование канала передачи.
- InfluxDB API v2 — приём данных в формате Line Protocol.
- API Token — аутентификация запросов.

Источники: 
    1. [Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/)
    2. [InfluxDB API](https://docs.influxdata.com/influxdb/v2/write-data/developer-tools/api/)

## 1. Технические требования

### 1.1 Механизм передачи данных

Решение использует встроенные механизмы Faceplate для работы с внешними API построенном по принципам REST  и протокола HTTPS. Передача данных осуществляется методом POST на эндпоинт InfluxDB API (v2.x).

### 2. Формат данных (Line Protocol)

Для записи в InfluxDB данные должны быть в формате [Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/):

measurement,tag_key=tag_value field_key=field_value timestamp

Пример строки:
telemetry,device=sensor_01 temperature=22.5,pressure=1013 1673785630000000000

Примечания:
- measurement — имя измерения, например отражающее место или объект измерения.
- tag — индексируемое поле (строка).
- field — значение (число, строка или булево).
- timestamp — в наносекундах (опционально; если отсутствует, InfluxDB присвоит текущий).

## 2. Компоненты прототипа

### 2.1 Контест

В контексте прототипа находится объект **iot_http_client** являющимся HTTP(S) клиентом для записи данных через REST API InfluxDB.

### 2.2 Параметры подключения

Для формирования запроса из Faceplate потребуются следующие параметры:

| Параметр | Описание | Пример |
|---|---:|---|
| URL | Адрес сервера InfluxDB | https://influx-server.com:8086 |
| Org | Название организации | my_company |
| Bucket | Имя целевого bucket | telemetry_bucket |
| Token | API токен доступа | MySecretToken |

Пример конечной точки записи:
https://influx-server.com:8086/api/v2/write?org=my_company&bucket=telemetry_bucket&precision=ns

Заголовки:
- Authorization: Token YOUR_API_TOKEN
- Content-Type: text/plain; charset=utf-8
- Accept: application/json

### Поля 



### Поведение 

Циклическое или событийное сканирования дерева проекта, сбор данных, формирование, отправка в экземпляр БД InfluxDB.

Код подтверждения 204 от REST API InfluxDB говрит об успешной записи данных.
Код подтверждения 401 от REST API InfluxDB говрит об отсутсвтвии авторизации (необходимо создать и добавить токен).