FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update && \
    apt-get install -y build-essential gcc g++ libstdc++6 linux-headers-generic && \
    pip install --upgrade pip && \
    pip install -U poetry && \
    poetry export --dev -o requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

ENV PYTHONPATH "/app"

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-cache /wheels/*

COPY ./ /app

CMD python ./src/main.py