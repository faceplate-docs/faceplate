Руководство: Создание и настройка нового кластера Faceplate

Данный документ описывает процесс развертывания нового кластера Faceplate (Runtime и Historian), его первоначальную настройку и тюнинг производительности.

1. Подготовка инфраструктуры

1.1. Требования к серверам

Операционная система: Ubuntu Server 22.04.05 LTS и выше, Debian 12.

Сеть: Рекомендуется выделить локальную подсеть (например, 10.230.0.0/24) для локального обмена данными, обеспечивающую канал связи от 1 Гб/c.

1.2. Настройка DNS и /etc/hosts

Корректная настройка локальных имен критична для работы кластера.

Откройте файл /etc/hosts на каждом сервере.

Пропишите IP-адреса и локальные имена всех серверов кластера.

Важно: Содержимое секции с именами нод Faceplate в /etc/hosts должно быть абсолютно идентичным на всех серверах. Без этого обмен данными невозможен.

Пример конфигурации:

10.230.0.11   rt-server1.fp
10.230.0.12   rt-server2.fp
10.230.0.13   his-server1.fp



2. Установка и структура приложения

2.1. Размещение файлов

Приложение разворачивается в следующей структуре каталогов:

/DATASET/project/scada/faceplate/ — файлы приложения (Runtime/Historian).

/DATASET/project/scada/local/ — база данных и локальные настройки.

/DATASET/project/scada/local/logs/ — файлы журналов (console.log, error.log).

2.2. Сертификаты

Для HTTPS соединений разместите файлы сертификатов в /DATASET/project/scada/faceplate/etc/certs:

ca-chain.cert.pem

node.cert.pem

node.key.pem

3. Базовая конфигурация (Tuning)

Настройка конфигурационных файлов в /DATASET/project/scada/faceplate/releases/4.0.6/ (и подпапке apps/).

3.1. vm.args (Настройки VM Erlang)

Задайте уникальные параметры для каждой ноды:

-name: Уникальное имя ноды (например, fp@rt-server1.fp).

-setcookie: Единый пароль (cookie) для взаимодействия всех серверов в кластере.

+MIscs: Флаг лимитирования памяти литерала (в МБ).

3.2. fp.logger.config (Логирование)

Настройте пути вывода логов в блоках console_handler и error_handler:

/DATASET/project/scada/local/logs/console.log

/DATASET/project/scada/local/logs/error.log

4. Запуск и сборка кластера

Запуск производится в сессии tmux (имя сессии scada).

4.1. Запуск первой ноды

На первом сервере выполните:

./faceplate console



4.2. Добавление остальных нод

Для подключения последующих серверов выполните команду запуска один раз с переменной ATTACH_TO, указывающей на уже работающую ноду.

Команда добавления:

env ATTACH_TO=fp@rt-server1.fp ./faceplate console



(Где fp@rt-server1.fp — имя первой ноды).

При последующих перезапусках используйте обычную команду ./faceplate console.

5. Настройка хранилища (Faceplate Studio)

Настройка БД выполняется через Faceplate Studio (http://xxx.xxx.xxx.xxx:90000/fp/studio).

5.1. Runtime (Оперативные данные)

Конфигурация хранения тегов реального времени.

Модули: Рекомендуется zaya_ets_rocksdb (RAM + диск) или zaya_rocksdb (только диск).

Конфигурация: Должна дублироваться на количество нод.

Пример JSON конфигурации:

":atom:fp@uzn-server1.fp": {
    ":atom:disc": {
        ":atom:module": ":atom:zaya_rocksdb",
        ":atom:params": {}
    },
    ":atom:ram": {
        ":atom:module": ":atom:zaya_ets",
        ":atom:params": {}
    },
    ":atom:ramdisc": {
        ":atom:module": ":atom:zaya_ets_rocksdb",
        ":atom:params": {}
    }
}



5.2. Сообщения (Журналы и алармы)

max_age: Период хранения алармов (в днях).

shard_depth: Временной диапазон одного шарда/файла (в днях).

read_only_age: Возраст архива для перехода в режим "только чтение".

5.3. Архивы

Настройки для долговременного архива (RocksDB):

remove_age: Глубина хранения (напр., 365 дней).

buffer_limit: Лимит буфера записи (напр., 1 ГБ).

open_options: Размер блока 32 КБ, сжатие lz4, асинхронная запись.

6. Роли и Сервис

6.1. Лимиты памяти (Раздел "Права")

Операторы (мониторинг): Лимит ~4000 МБ.

Инженеры (активная работа, логи): Лимит ~8000 МБ.

6.2. Запуск в режиме сервиса

После отладки рекомендуется переход на запуск в режиме сервиса.

Инструкция по установке:

Создайте файл install_fp_service.sh рядом с дистрибутивом.

Сделайте его исполняемым: chmod +x install_fp_service.sh.

Запустите: ./install_fp_service.sh и следуйте инструкциям.

Скрипт установки (install_fp_service.sh):

#!/bin/bash
# ==========================================
#  Интерактивный установщик 'foreground' сервиса (БЕЗ ЛОГОВ)
# ==========================================
# --- Цвета для вывода ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- Функции ---
print_info() { echo -e "\n${BLUE}INFO:${NC} $1"; }
print_success() { echo -e "${GREEN}SUCCESS:${NC} $1"; }
print_error() { echo -e "${RED}ERROR:${NC} $1"; }

# === 1. ПРОВЕРКА НА ROOT ===
print_info "Запуск установщика 'foreground' сервиса..."
if [ "$EUID" -ne 0 ]; then
    print_error "Этот скрипт необходимо запускать с правами root."
    echo "Пожалуйста, запустите: sudo ./install_fp_service.sh"
    exit 1
fi

# === 2. ИНТЕРАКТИВНЫЙ ВВОД ===
print_info "Пожалуйста, ответьте на несколько вопросов."
echo "Вы можете нажать Enter, чтобы использовать значения по умолчанию (в скобках)."
read -e -i "fp.service" -p "  1. Введите имя для .service файла: " SERVICE_NAME
read -e -i "master" -p "  2. Введите имя пользователя (User): " SERVICE_USER
read -e -i "sudo" -p "  3. Введите имя группы (Group): " SERVICE_GROUP
read -e -i "/DATASET/project/scada/faceplate" -p "  4. Введите полный путь к папке Faceplate: " FACEPLATE_PATH
FACEPLATE_PATH=${FACEPLATE_PATH%/}

# === 3. ВАЛИДАЦИЯ ===
print_info "Проверка введенных данных..."
EXEC_FILE="$FACEPLATE_PATH/bin/faceplate"
if [ ! -f "$EXEC_FILE" ]; then
    print_error "Бинарник НЕ НАЙДЕН по пути: $EXEC_FILE"
    echo "Пожалуйста, проверьте путь и попробуйте снова."
    exit 1
else
    print_success "Бинарник найден: $EXEC_FILE"
fi

if ! id "$SERVICE_USER" &>/dev/null; then
    print_error "Пользователь '$SERVICE_USER' не существует в системе."
    exit 1
fi
if ! getent group "$SERVICE_GROUP" &>/dev/null; then
    print_error "Группа '$SERVICE_GROUP' не существует в системе."
    exit 1
fi
print_success "Пользователь и группа существуют."

# === 4. ГЕНЕРАЦИЯ ФАЙЛА ===
SERVICE_DEST_FILE="/etc/systemd/system/$SERVICE_NAME"
print_info "Подготовка unit-файла..."
SERVICE_CONTENT=$(cat <<EOF
[Unit]
Description=Faceplate SCADA Application Service (Foreground)
After=network.target
[Service]
Type=simple
StandardOutput=null
StandardError=null
User=$SERVICE_USER
Group=$SERVICE_GROUP
WorkingDirectory=$FACEPLATE_PATH
ExecStart=$EXEC_FILE foreground
Restart=always
RestartSec=5
LimitNOFILE=200000
[Install]
WantedBy=multi-user.target
EOF
)

# === 5. ПОДТВЕРЖДЕНИЕ ===
echo -e "\n${YELLOW}--- ПРОВЕРЬТЕ ДАННЫЕ ---${NC}"
echo "Сервис будет установлен сюда: ${GREEN}$SERVICE_DEST_FILE${NC}"
echo "Содержимое файла:"
echo -e "${BLUE}---------------------------------${NC}"
echo "$SERVICE_CONTENT"
echo -e "${BLUE}---------------------------------${NC}"
echo ""
read -p "Все верно? (y/n): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Установка отменена."
    exit 0
fi

# === 6. УСТАНОВКА ===
print_info "Остановка старого сервиса (если он был)..."
systemctl stop "$SERVICE_NAME" &>/dev/null
print_info "1. Запись файла в $SERVICE_DEST_FILE..."
echo -e "$SERVICE_CONTENT" > "$SERVICE_DEST_FILE"
print_info "2. Перезагрузка демонов systemd (daemon-reload)..."
systemctl daemon-reload
print_info "3. Включение автозагрузки сервиса (enable)..."
systemctl enable "$SERVICE_NAME"
print_info "4. Запуск сервиса $SERVICE_NAME (start)..."
systemctl start "$SERVICE_NAME"

# === 7. ФИНАЛ ===
print_success "Установка и запуск завершены!"
echo "Проверка статуса сервиса (через 2 секунды):"
sleep 2
systemctl status "$SERVICE_NAME"
exit 0



6.3. Восстановление (Force Mode)

В случае сбоя:

Остановите сервисы.

Запустите первую ноду в консоли (см. пункт 4.1) в режиме Force.

Остальные ноды запустите в режиме сервиса.

После восстановления остановите первую ноду в консоли и переведите ее в режим сервиса.

Анализ документа и предложения

При конвертации были внесены следующие корректировки и предложения:

Исправление опечаток: Исправлены слова "класстер" (кластер), "распологаем" (располагаем), "режуму" (режиму).

Структура: Документ разбит на логические блоки с заголовками H1, H2, H3 для удобной навигации.

JSON Синтаксис: В разделе 5.1 используется формат :atom:module. Если интерфейс SCADA требует чистый JSON, возможно, потребуется заменить :atom:module на "module". Рекомендуется проверить этот момент в документации вендора.

Безопасность: В скрипте по умолчанию используется группа sudo. Для продакшн-систем рекомендуется создать отдельную группу (например, faceplate), чтобы ограничить права доступа процесса.