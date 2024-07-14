###############################################################################
# BUILD IMAGE                                                                 #
###############################################################################
FROM python:3.12-slim AS build

RUN apt-get -y update \
    && apt-get install -y \
    libpq-dev \
    gcc \
    && pip install poetry

WORKDIR /usr/src

COPY poetry.lock pyproject.toml /usr/src/

RUN virtualenv -p python3.12 venv \
    && PATH="/usr/src/venv/bin:$PATH" \
    VIRTUAL_ENV="/usr/src/venv" \
    poetry install --only main

###############################################################################
# RUNTIME IMAGE                                                               #
###############################################################################
FROM python:3.12-slim

ENV PATH="/usr/src/venv/bin:$PATH"

EXPOSE 8000

WORKDIR /usr/src

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/src/venv /usr/src/venv
COPY ./app /usr/src/app

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "app.wsgi:application"]
