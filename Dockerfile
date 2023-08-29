FROM python:3.8.10 AS base_builder
LABEL maintaine="Aymene AHDIBI <ahdibiaymen@gmail.com>"
LABEL name="Website-Snapshot-API"
LABEL description="Snapshot websites in HTML/PNG format"

ARG build_env=dev
ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV TZ=Europe/Paris \
    USERNAME=phishing \
    OPENSSL_CONF=/etc/ssl/ \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

WORKDIR /opt/p-i

RUN apt update && apt install -y\
    python3-dev \
    build-essential \
    libssl-dev \
    firefox-esr \
    && pip install poetry==$POETRY_VERSION \
    && useradd --user-group --system -s /bin/bash -m -d /opt/p-i -u 1000 --no-log-init ${USERNAME} \
    && mkdir -p /etc/custom \
    && touch /etc/custom/drivers \
    && chown -R ${USERNAME}:${USERNAME} /etc/custom

COPY src ./src
COPY tests ./tests
COPY [".flaskenv", "poetry.lock", "pyproject.toml", "wsgi.py", "README.md", "./"]
COPY --chown=${USERNAME}:${USERNAME} docker-entrypoint.sh /docker-entrypoint.sh

RUN poetry config virtualenvs.create false \
    && if [ "${build_env}" != "dev" ]; then \
      poetry install --without dev --no-interaction --no-ansi; \
      rm -rf .flaskenv pyproject.toml poetry.lock README.md; \
    else \
      poetry install --no-interaction --no-ansi; \
    fi \
    && chown -R ${USERNAME}:${USERNAME} .

USER ${USERNAME}

RUN python src/webdrivers_installer.py

CMD ["/docker-entrypoint.sh"]

FROM base_builder AS dev_builder
FROM base_builder AS prod_builder
