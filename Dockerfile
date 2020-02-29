FROM python:3.7.4-alpine3.10

ENV PYTHONUNBUFFERED 1

COPY ["requirements.txt", "/app/"]
WORKDIR /app

RUN apk add --update --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        pcre \
        gcc \
        musl-dev \
        linux-headers \
        make \
    && rm -rf /var/cache/apk/* \
    && pip install --no-cache-dir --upgrade pip==9.0.3 pip-tools==1.9.0 \
    && pip-sync requirements.txt \
    && apk del .build-deps \
    && rm -rf /root/.cache/*
