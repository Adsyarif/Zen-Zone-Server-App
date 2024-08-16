# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

ARG FLASK_DEBUG
ARG FLASK_ENV
ARG TYPE
ARG HOST_DB
ARG NAME_DB
ARG PORT
ARG USER
ARG PASSWORD
ARG JWT_SECRET_KEY

RUN echo $FLASK_DEBUG
RUN echo $FLASK_ENV
RUN echo $TYPE
RUN echo $HOST_DB
RUN echo $NAME_DB
RUN echo $PORT
RUN echo $USER
RUN echo $PASSWORD
RUN echo $JWT_SECRET_KEY

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY . /app

RUN poetry run flask 

CMD ["/app/.venv/bin/gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]