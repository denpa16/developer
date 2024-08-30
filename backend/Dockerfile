FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --user --no-cache-dir poetry==1.8
ENV PATH="${PATH}:/root/.local/bin"
RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install --no-interaction --no-ansi

COPY / /app/
RUN chmod +x entrypoint.*
