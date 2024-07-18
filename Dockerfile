FROM python:3.11-slim as exchange-poetry

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip3 install --no-cache-dir poetry


FROM exchange-poetry as exchange-base

COPY pyproject.toml pyproject.toml

RUN poetry install

FROM exchange-base as exchange-main
COPY . .
