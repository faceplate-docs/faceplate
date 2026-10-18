# Deploying the documentation as a website

The documentation is built into a static site by **MkDocs** with the
**Material for MkDocs** theme (both open source, MIT). The result is plain
HTML that any web server can serve.

Because the file layouts of `docs/en` and `docs/ru` differ, each language is
built as a separate site. A language switcher is shown in the page header.

```
site/
  index.html   — detects the browser language and redirects to /ru/ or /en/
  en/          — English site   (config mkdocs.en.yml)
  ru/          — Russian site   (config mkdocs.ru.yml)
```

## Files

| File | Purpose |
|---|---|
| `mkdocs.base.yml` | Shared settings: theme, Markdown extensions, language switcher |
| `mkdocs.en.yml`, `mkdocs.ru.yml` | Language, source folder and the site **navigation** |
| `requirements.txt` | Python dependencies for the build |
| `tools/build_site.sh` | Builds both languages into `site/` and adds the entry pages |
| `tools/check_links.py` | Checks relative links and images in `docs/` |
| `Dockerfile`, `deploy/nginx.conf`, `docker-compose.yml` | nginx image with the built site |
| `.github/workflows/docs.yml` | CI: build on every push/PR, publish to GitHub Pages from `dev` |

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve -f mkdocs.en.yml      # http://127.0.0.1:8000/ , reloads on edit
mkdocs serve -f mkdocs.ru.yml -a 127.0.0.1:8001
```

Full build of both languages:

```bash
tools/build_site.sh                # output in ./site
python3 -m http.server -d site 8080
```

## Option 1. Docker (own server)

```bash
docker compose up -d --build
# http://localhost:8080/
```

The port is set with `DOCS_PORT`. The public site URLs (used for canonical
links and sitemaps) are set with `DOCS_SITE_URL_EN` and `DOCS_SITE_URL_RU`,
for example:

```bash
DOCS_SITE_URL_EN=https://docs.faceplate.io/en/ \
DOCS_SITE_URL_RU=https://docs.faceplate.io/ru/ \
DOCS_PORT=8080 docker compose up -d --build
```

The image contains only nginx and static files, so it can sit behind an
existing reverse proxy (nginx, Traefik, Caddy) that terminates TLS. HTTPS is
not configured inside the image; that is the job of the outer proxy.

To update: `git pull`, then `docker compose up -d --build` again.

## Option 2. GitHub Pages (free hosting)

The workflow `.github/workflows/docs.yml` builds the site on every push and
pull request to `dev` and `main`, and publishes it to GitHub Pages on every
push to `dev`.

One-time repository setup: **Settings → Pages → Build and deployment →
Source: GitHub Actions**. The site is then served at
<https://faceplate-docs.github.io/faceplate/> (`/en/` and `/ru/`).

To publish from `main` instead, change `refs/heads/dev` in the `if:`
condition of the `deploy` job.

A custom domain (for example `docs.faceplate.io`) is attached in the same
Pages settings; then update `DOCS_SITE_URL_*` in the workflow.

## Option 3. Any static hosting

`tools/build_site.sh` produces the `site/` folder, which can be uploaded to
any static hosting or S3-compatible storage. The server must serve
`index.html` for directories (in `deploy/nginx.conf` this is
`try_files $uri $uri/ $uri/index.html`).

## Branding

Brand assets live in `brand/assets/` and are copied into every build through
`theme.custom_dir` in `mkdocs.base.yml`:

| File | Use |
|---|---|
| `faceplate-logo.png` | Wordmark shown in the site header and in README.md |
| `faceplate-mark.png`, `favicon.png`, `apple-touch-icon.png`, `favicon-32.png` | The "A" mark cropped from the wordmark, used as the favicon |
| `brand.css` | Brand colours and header layout for the Material theme |

The brand red is `#D71921`, sampled from the wordmark. Light scheme: white
header with the red wordmark and a red rule beneath it. Dark scheme:
near-black header. Links, active navigation items and accents use the brand
red. To change a colour, edit the variables at the top of `brand.css`.

## Adding pages to the site

A page appears in the site menu only when it is listed in the `nav` section
of the corresponding `mkdocs.<lang>.yml`. A file that is not in `nav` is
still built and reachable by direct link. Paths in `nav` are relative to
`docs/<lang>/`.

## Known details

- The entry page of each language is `readme.md`. MkDocs does not treat it as
  the directory index, so `tools/build_site.sh` adds `site/<lang>/index.html`
  with a redirect to `readme/`.
- File names with spaces and Cyrillic characters (`Архивы и Тренды.md`,
  `deploy as docker.md`) build correctly but produce long percent-encoded
  URLs. They can be renamed if desired; update `nav` and links afterwards.
- `docs/` contains some pre-existing broken links (see
  `python3 tools/check_links.py`). They do not block the build. Once they are
  fixed, enable strict mode: `MKDOCS_STRICT=1 tools/build_site.sh`, and
  remove `continue-on-error` in the workflow so CI fails on new broken links.
- Search runs in the browser (lunr.js) and indexes both languages.
- MkDocs is pinned below 2.0 in `requirements.txt`; the Material theme prints
  a notice about MkDocs 2.0 during the build, which can be ignored.
