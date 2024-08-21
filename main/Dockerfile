FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y gcc libc-dev 



COPY ${PYPROJECT_TOML_PATH} /app/
COPY main/app /app/


RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

RUN pip install uvicorn


CMD ["sh", "-c", "uvicorn --factory main.app.application.api.main:create_app --host 0.0.0.0 --port 8000"]