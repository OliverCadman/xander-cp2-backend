FROM python:3.9-alpine3.13

LABEL maintainer='oliver.cadman@xandertalent.com'

ENV PYTHONUNBUFFERED 1

COPY ./app /app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev gcc python3-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV = "true"]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        django-user 

# Make sure there's no whitespace between the assignment operator!
ENV PATH="/py/bin:$PATH"

USER django-user