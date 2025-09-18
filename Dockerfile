FROM python:3.13

WORKDIR /app

RUN pip install poetry==2.1.4

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .
