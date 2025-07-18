FROM python:3.9-slim
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements-dev.txt
COPY ./app /app
COPY ./core /core
WORKDIR /app
EXPOSE 8000

ARG DEV=true

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        pip install -r /tmp/requirements-dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user
