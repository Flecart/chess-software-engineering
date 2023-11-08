FROM python:3.11 as builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENV TELEGRAM_TOKEN=""
ENV BACKEND_URL=""

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src/ ./src
COPY *.py ./

RUN apt update
RUN apt install libffi-dev  # maybe also the cairo package

ENTRYPOINT ["python", "-m", "bot"]
