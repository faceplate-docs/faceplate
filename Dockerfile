# Build the documentation with MkDocs, then serve the static result with nginx.
#
#   docker build -t faceplate-docs .
#   docker run --rm -p 8080:80 faceplate-docs
#
# Build arguments set the public URLs used for canonical links and sitemaps.

FROM python:3.12-slim AS build
ARG DOCS_SITE_URL_EN=http://localhost:8080/en/
ARG DOCS_SITE_URL_RU=http://localhost:8080/ru/
ENV DOCS_SITE_URL_EN=${DOCS_SITE_URL_EN} \
    DOCS_SITE_URL_RU=${DOCS_SITE_URL_RU} \
    PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY mkdocs.base.yml mkdocs.en.yml mkdocs.ru.yml ./
COPY tools/build_site.sh tools/
COPY brand/ brand/
COPY docs/ docs/
RUN tools/build_site.sh

FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/site /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/en/readme/ >/dev/null || exit 1
