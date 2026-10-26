# Contributing to the Faceplate documentation

## Языки

1. Сначала пишется русская страница в `docs/ru/`.
2. После утверждения она переводится в `docs/en/` — **тот же путь и то же имя файла**.
3. Пока перевода нет, английская страница содержит заглушку «Translation pending» со ссылкой на русскую.
4. Если русская страница изменилась, английская обновляется в том же PR или помечается `> Translation outdated`.

## Аудитории и разделы

| Раздел | Читатель | Пишем о |
|---|---|---|
| `operator/` | диспетчер, оператор | что видно на экране и что нажимать; без кода и путей в БД |
| `engineer/` | инженер проекта | объекты, прототипы, связь с ПЛК, архивы, расчёты, экраны, API |
| `admin/` | администратор, DevOps | установка, конфигурация, контейнеры, резервирование, бэкапы |
| `overview/`, `reference/` | все | общие понятия и сводные таблицы |

Одна страница — одна аудитория. Если тема нужна двум аудиториям (например, тренды), пишем две страницы и ссылаемся друг на друга.

## Типы страниц

Каждая страница относится к одному типу — шаблоны в `templates/`:

- **Концепция** (`concept.md`) — объясняет, как что-то устроено и зачем.
- **Инструкция** (`howto.md`) — пошагово решает одну задачу.
- **Справочник** (`reference.md`) — перечисляет параметры, поля, функции, коды.

Тип и статус указываются второй строкой страницы:

```
> Тип: инструкция · Статус: черновик
```

Статусы: `черновик` → `на проверке` → `готово`.

## Файлы и ссылки

- Имена файлов — латиница, строчные, через дефис: `backup-restore.md`.
- Раздел с подстраницами — папка с `README.md` внутри.
- Ссылки только относительные: `[Архивы](../engineer/archives.md)`.
- Изображения — в `docs/<язык>/assets/<раздел>/`, имя по содержанию: `grid-filter-panel.png`.
- Новую страницу добавляйте в оглавление `docs/<язык>/README.md` и в «Содержание раздела» родительского `README.md`, а также в `PLAN.md`.

## Стиль

- Обращаемся на «вы», в инструкциях — повелительное наклонение: «Откройте схему», «Нажмите «Найти»».
- Названия кнопок и пунктов меню — в кавычках-ёлочках, как в интерфейсе.
- Имена полей, объектов, функций, путей — моноширинным шрифтом: `out_value`, `fp-calculation`.
- Пути объектов в примерах — без префикса `/root/FP/PROJECT/`, как они отображаются в интерфейсе.
- Термины — по [глоссарию](docs/ru/overview/glossary.md). Новый термин сначала добавьте в глоссарий.
- Примеры кода — рабочие, проверенные на текущей версии платформы; язык блока указывается (` ```js `, ` ```erlang `, ` ```json `).
- Заметки и предупреждения:

```
> **Примечание.** …
> **Внимание.** …
```

- Незаполненные места помечайте `<!-- TODO: … -->` — их легко найти поиском.

## Layout

```
docs/
  en/        English pages
  ru/        Russian pages
  source/    original .docx files that some pages were converted from
tools/       helper scripts (link checker, site build)
mkdocs.*.yml MkDocs configuration: shared settings and one nav per language
README.md    table of contents for both languages
DEPLOYMENT.md how the site is built and deployed
```

Each topic lives in its own folder with an `images/` sub-folder next to the
page, for example `docs/en/storage/Storage_en.md` and
`docs/en/storage/images/1.png`. English pages end in `_en.md`, Russian pages
in `_ru.md`, where the folder name alone is not enough to tell them apart.

Every topic should exist in both languages. When you add or rename a page,
add or rename its counterpart in the other language too (or create it with a
heading and a short note that the translation is pending), and add both to
the table of contents in `README.md`.

## Page conventions

- Markdown, one topic per file. Prefer lowercase folder and file names with
  underscores and no spaces, so links work without escaping.
- Images are referenced with relative paths (`images/name.png`), never with
  absolute paths or links to another branch.
- Links to other pages are relative to the current file, for example
  `../plc_connections/general_en.md`. Links that start with `/` do not work on
  GitHub.
- Pages that were written by a specific author end with an author line such
  as `> _written by nkn_`.
- Pages that are not yet complete carry a status line near the top and `TODO`
  markers in the text, so open items can be found with a search:

  ```
  > **Status:** Draft — details need confirmation by the Faceplate team.
  ```

- Keep product names and identifiers exactly as they appear in FACEPLATE
  Studio, for example `prototype@model_control`, `fp://`, `output_range`.

## Previewing the site

The documentation is published as a website built with MkDocs (see
[DEPLOYMENT.md](DEPLOYMENT.md)). To preview your changes locally:

```bash
pip install -r requirements.txt
mkdocs serve -f mkdocs.en.yml      # or mkdocs.ru.yml
```

A new page appears in the site menu only after it is added to the `nav`
section of `mkdocs.en.yml` or `mkdocs.ru.yml`, with its path relative to
`docs/en/` or `docs/ru/`.

## Checking links before you push

`tools/check_links.py` verifies that every relative link and image reference
in `docs/` points to an existing file:

```bash
python3 tools/check_links.py
```

It prints each broken link with the page it is on and exits with a non-zero
code if any are found.

## Workflow

Day-to-day work happens on the `dev` branch; `main` receives reviewed
changes. Open a pull request against `dev` for new or updated pages.
