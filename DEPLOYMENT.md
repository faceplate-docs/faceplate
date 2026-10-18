# Развёртывание документации как веб-сервиса

Документация собирается в статический сайт генератором **MkDocs** с темой
**Material for MkDocs** (оба — open source, MIT). Готовый сайт — обычные
HTML-файлы, которые отдаёт любой веб-сервер.

Поскольку структура файлов в `docs/en` и `docs/ru` различается, для каждого
языка собирается отдельный сайт. В шапке страницы есть переключатель языков.

```
site/
  index.html   — определяет язык браузера и перенаправляет на /ru/ или /en/
  en/          — английский сайт   (конфиг mkdocs.en.yml)
  ru/          — русский сайт      (конфиг mkdocs.ru.yml)
```

## Файлы

| Файл | Назначение |
|---|---|
| `mkdocs.base.yml` | Общие настройки: тема, расширения Markdown, переключатель языков |
| `mkdocs.en.yml`, `mkdocs.ru.yml` | Язык, каталог исходников и **навигация** (оглавление) сайта |
| `requirements.txt` | Python-зависимости для сборки |
| `tools/build_site.sh` | Собирает оба языка в `site/` и добавляет стартовые страницы |
| `tools/check_links.py` | Проверяет относительные ссылки и картинки в `docs/` |
| `Dockerfile`, `deploy/nginx.conf`, `docker-compose.yml` | Образ nginx с собранным сайтом |
| `.github/workflows/docs.yml` | CI: сборка на каждый push/PR, публикация на GitHub Pages из `dev` |

## Локальный просмотр

```bash
pip install -r requirements.txt
mkdocs serve -f mkdocs.ru.yml      # http://127.0.0.1:8000/ , перезагрузка при правках
mkdocs serve -f mkdocs.en.yml -a 127.0.0.1:8001
```

Полная сборка обоих языков:

```bash
tools/build_site.sh                # результат в ./site
python3 -m http.server -d site 8080
```

## Вариант 1. Docker (свой сервер)

```bash
docker compose up -d --build
# http://localhost:8080/
```

Порт задаётся переменной `DOCS_PORT`. Публичные адреса сайта (для
canonical-ссылок и sitemap) — переменными `DOCS_SITE_URL_EN` и
`DOCS_SITE_URL_RU`, например:

```bash
DOCS_SITE_URL_EN=https://docs.faceplate.io/en/ \
DOCS_SITE_URL_RU=https://docs.faceplate.io/ru/ \
DOCS_PORT=8080 docker compose up -d --build
```

Образ содержит только nginx и статику, поэтому его можно поставить за
существующий reverse proxy (nginx, Traefik, Caddy) с TLS. HTTPS в образе не
настраивается — это задача внешнего прокси.

Обновление: `git pull`, затем снова `docker compose up -d --build`.

## Вариант 2. GitHub Pages (бесплатный хостинг)

Workflow `.github/workflows/docs.yml` собирает сайт на каждый push и pull
request в `dev` и `main`, а при push в `dev` публикует его на GitHub Pages.

Разовая настройка в репозитории: **Settings → Pages → Build and deployment →
Source: GitHub Actions**. После этого сайт доступен по адресу
`https://faceplate-docs.github.io/faceplate/` (`/en/` и `/ru/`).

Чтобы публиковать с ветки `main`, замените `refs/heads/dev` в условии
`if:` задачи `deploy` и добавьте `main` в адреса сборки.

Собственный домен (например `docs.faceplate.io`) подключается в тех же
настройках Pages; тогда нужно поправить `DOCS_SITE_URL_*` в workflow.

## Вариант 3. Любой статический хостинг

`tools/build_site.sh` создаёт каталог `site/`, который можно выложить на
любой статический хостинг или S3-совместимое хранилище. Сервер должен
отдавать `index.html` для каталогов (в `deploy/nginx.conf` это
`try_files $uri $uri/ $uri/index.html`).

## Добавление страниц в сайт

Страница попадает в меню сайта только если указана в секции `nav`
соответствующего `mkdocs.<lang>.yml`. Файл, не указанный в `nav`, всё равно
собирается и доступен по прямой ссылке. Пути в `nav` указываются
относительно `docs/<lang>/`.

## Известные особенности

- Стартовая страница каждого языка — `readme.md`. MkDocs не считает её
  индексом каталога, поэтому `tools/build_site.sh` добавляет
  `site/<lang>/index.html` с перенаправлением на `readme/`.
- Имена файлов с пробелами и кириллицей (`Архивы и Тренды.md`,
  `deploy as docker.md`) собираются корректно, но дают длинные URL с
  процентным кодированием. При желании их можно переименовать и обновить
  `nav` и ссылки.
- В `docs/` есть ранее сломанные ссылки (см. `python3 tools/check_links.py`).
  Сборка их не блокирует. Когда ссылки исправлены, включите строгий режим:
  `MKDOCS_STRICT=1 tools/build_site.sh` и уберите `continue-on-error` в
  workflow — тогда CI будет падать на новых сломанных ссылках.
- Поиск работает на клиенте (lunr.js) и индексирует оба языка.
