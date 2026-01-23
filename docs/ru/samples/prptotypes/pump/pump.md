# Шаблон интеграции с базой временных рядов InfluxDB.

Объект построенный на шаблоне Influxdb позволяет отправлять данные в экземпляр InfluxDB через REST API. Конфигурация прототипа позволяет обрабатывать объекты находящихся в директории где нахоодится объект и со всех вложенных папок.

Внешние источники: 
    1. [Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/)
    2. [InfluxDB API](https://docs.influxdata.com/influxdb/v2/write-data/developer-tools/api/)
    3. [Faceplate prototypes](/docs/en/prototypes)
    4. [Faceplate primitives](/docs/en/primitives)

## 1. Технические требования

### 1.1 Механизм передачи данных

Решение использует встроенные механизмы Faceplate для работы с внешними API построенном по принципам REST  и протокола HTTPS. Передача данных осуществляется методом POST на эндпоинт InfluxDB API (v2.x).

Основные компоненты:
- Faceplate — HTTP-клиент, собирающий и отправляющий данные.
- HTTPS (TLS) — шифрование канала передачи.
- InfluxDB API v2 — приём данных в формате Line Protocol.
- API Token — аутентификация запросов.

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
+-----------+---------------------------+-----------------------------------+
| Параметр  | Описание                  | Пример                            |
|-----------|---------------------------|-----------------------------------|
| URL       | Адрес сервера InfluxDB    | https://influx-server.com:8086    |
| Org       | Название организации      | my_company                        |
| Bucket    | Имя целевого bucket       | telemetry_bucket                  |
| Token     | API токен доступа         | MySecretToken                     |
+-----------+---------------------------+-----------------------------------+

Пример конечной точки записи:
https://influx-server.com:8086/api/v2/write?org=my_company&bucket=telemetry_bucket&precision=ns

Заголовки:
- Authorization: Token YOUR_API_TOKEN
- Content-Type: text/plain; charset=utf-8
- Accept: application/json

### Поля 
+------------------------------------------------------------------------------------------------------+
| название | тип      | подтип    | комментарий                                                        |
|----------|----------|-----------|--------------------------------------------------------------------|
| patterns | list     | string    | список типов объеков по которым агент                              |
|          |          |           | собирает и отправляет данные                                       |
| name     | string   |           | имя агента                                                         |
| state    | integer  |           | состояние агента                                                   |
+------------------------------------------------------------------------------------------------------+

### Поведение 

Циклическое или событийное сканирования дерева проекта, сбор данных, формирование, отправка в экземпляр БД InfluxDB.

Код подтверждения 204 от REST API InfluxDB говрит об успешной записи данных.
Код подтверждения 401 от REST API InfluxDB говрит об отсутсвтвии авторизации (необходимо создать и добавить токен).

Модуль:

%%%-------------------------------------------------------------------
%%% @doc InfluxDB Client Module
%%% This module facilitates the export of object field data to InfluxDB.
%%% It transforms internal database objects into the InfluxDB Line Protocol:
%%% `measurement,tag_set field_set timestamp`
%%% @end
%%%-------------------------------------------------------------------
-module(influx_client).
-include("fp.hrl").

%% API
-export([on_create/1, on_delete/1, on_edit/1]).
-export([write/2]).

%% @doc Hardcoded path pattern to locate sensor objects within a base object.
-define(SENSORS, [<<"/root/FP/prototypes/analog/fields">>]).

%%====================================================================
%% Callback API
%%====================================================================

on_create(_Object) -> ok.
on_edit(_Object)   -> ok.
on_delete(_Object) -> ok.

%%====================================================================
%% Public Functions
%%====================================================================

%% @doc
%% Scans the database for objects matching `Patterns`, collects their 
%% field values, and formats them into a single binary string suitable 
%% for an InfluxDB batch write.
%% @end
write(Root, Patterns) ->
    %% 1. Find all base objects matching the provided patterns
    BasePaths = lists:append([system_utils:find_objects(Root, Pattern) || Pattern <- Patterns]),
    
    %% 2. Generate an Influx line for each base object found
    AllRows = [collect_data(P, ?SENSORS) || P <- BasePaths],
    
    %% 3. Filter out empty results and join with newlines
    CleanRows = [R || R <- AllRows, R /= <<>>],
    
    Result = iolist_to_binary(lists:join(<<"\n">>, CleanRows)),
    ?LOGINFO("[DEBUG][PROTOTYPE][INFLUX] Final String: ~p", [Result]),
    Result.

%%====================================================================
%% Internal Functions
%%====================================================================

%% @private
%% Safe wrapper for data collection to prevent a single object error 
%% from crashing the entire batch process.
collect_data(Path, SensorPatterns) ->
    try
        try_collect_data(Path, SensorPatterns)
    catch 
        _Class:Error:_Stack ->
            ?LOGERROR("failed to collect data, path: ~p, patterns: ~p, error: ~p", [
                Path, SensorPatterns, Error
            ]),
            <<>>
    end.

%% @private
%% Extracts metadata (measurement/tags) and sensor values (fields) 
%% to construct the Line Protocol string.
try_collect_data(Path, SensorPatterns) ->
    %% Fetch core metadata from the base object
    #{
        <<"tags">> := Tags, 
        <<"measurement">> := Measurement
    } = fp_db:read_fields(?OBJECT(Path), [<<"measurement">>, <<"tags">>]),
    
    %% Tags are expected to be a JSON string; parse into a map
    TagsMap = try ?FROM_JSON(Tags) catch _:_ -> throw({invalid_tags, Tags}) end,
    
    %% Find all sensor objects nested under the current base path
    FoundSensors = lists:append([system_utils:find_objects(Path, Pattern) || Pattern <- SensorPatterns]),
    
    %% Aggregate sensor names and values into a Field Map
    FieldsMap = 
        lists:foldl(
            fun(Sensor, Acc) ->
                #{
                    <<".name">> := Name,
                    <<"out_value">> := Value
                } = fp_db:read_fields(?OBJECT(Sensor), [<<"out_value">>, <<".name">>], #{format => fun fp_db:to_json/2}),
                Acc#{Name => Value}
            end, 
            #{}, 
            FoundSensors
        ),
        
    %% Only return a string if we actually found data to report
    case map_size(FieldsMap) > 0 of
        true -> format_line(Measurement, TagsMap, FieldsMap);
        false -> <<>>
    end.

%% @private
%% Assembles the component parts into the final InfluxDB binary format.
format_line(Measurement, TagsMap, FieldsMap) ->
    TagsPart = join_kv(maps:to_list(TagsMap)),
    FieldsPart = join_kv(maps:to_list(FieldsMap)),
    %% Format: measurement,tags fields
    list_to_binary(io_lib:format("~s,~s ~s", [to_s(Measurement), TagsPart, FieldsPart])).

%% @private
%% Converts a list of {Key, Value} tuples into a comma-separated string: "K1=V1,K2=V2"
join_kv(KVList) ->
    Pairs = 
        [if 
            is_number(V) -> io_lib:format("~s=~p", [to_s(K), V]);
            true -> io_lib:format("~s=~s", [to_s(K), fp_util:coerce_value(string, V)])
         end || {K, V} <- KVList],
    string:join(Pairs, ",").

%% @private
%% Utility to ensure keys/values are in string format for io_lib.
to_s(V) when is_binary(V) -> binary_to_list(V);
to_s(V) when is_atom(V)   -> atom_to_list(V);
to_s(V) -> V.