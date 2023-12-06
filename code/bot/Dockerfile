FROM python:3.11 AS builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN touch README.md

RUN poetry install --no-root && rm -rf "$POETRY_CACHE_DIR"

FROM python:3.11-slim-buster AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENV PROTOCOL=https
ENV WS_PROTOCOL=wss
ENV HOST=app.t1-check-mates.mooo.com/backend

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY bot/ ./bot/

RUN apt update && apt install -y libffi-dev libcairo2 && apt clean

ENTRYPOINT ["python", "-m", "bot.__init__"]
