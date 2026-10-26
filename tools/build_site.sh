#!/usr/bin/env bash
# Build the English and Russian documentation sites into ./site.
#
#   site/index.html   -> redirects to the visitor's language (ru or en)
#   site/en/          -> English site (mkdocs.en.yml)
#   site/ru/          -> Russian site (mkdocs.ru.yml)
#
# Environment:
#   DOCS_SITE_URL_EN / DOCS_SITE_URL_RU  public URLs of each language site,
#                                        used for canonical links and sitemaps
#                                        (default http://localhost:8080/<lang>/)
#   MKDOCS_STRICT=1                      fail the build on MkDocs warnings
set -euo pipefail

cd "$(dirname "$0")/.."

STRICT=()
if [[ "${MKDOCS_STRICT:-0}" == "1" ]]; then
  STRICT=(--strict)
fi

rm -rf site
mkdir -p site

for lang in en ru; do
  echo "==> Building ${lang}"
  mkdocs build "${STRICT[@]}" -f "mkdocs.${lang}.yml"
  # The entry page of each language is readme.md (lower-case), which MkDocs
  # does not treat as the directory index. Add an index that forwards to it.
  if [[ ! -f "site/${lang}/index.html" ]]; then
    cat > "site/${lang}/index.html" <<HTML
<!DOCTYPE html>
<html lang="${lang}"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=readme/">
<link rel="canonical" href="readme/">
<title>FACEPLATE Documentation</title></head>
<body><a href="readme/">FACEPLATE Documentation</a></body></html>
HTML
  fi
done

# Root page: pick the language from the browser, fall back to English.
cat > site/index.html <<'HTML'
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>FACEPLATE Documentation</title>
<meta name="robots" content="noindex">
<script>
  var lang = (navigator.language || "en").toLowerCase().indexOf("ru") === 0 ? "ru" : "en";
  window.location.replace(lang + "/");
</script>
<noscript><meta http-equiv="refresh" content="0; url=en/"></noscript>
</head>
<body>
<p><a href="en/">English</a> · <a href="ru/">Русский</a></p>
</body></html>
HTML

cat > site/robots.txt <<'TXT'
User-agent: *
Allow: /
TXT

echo "==> Done: $(du -sh site | cut -f1) in ./site"
