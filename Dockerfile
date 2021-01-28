FROM python:3.7.9-alpine3.12

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --upgrade pip
COPY ./requirements.txt /code/requirements.txt 
RUN chmod +x /code/requirements.txt && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /code/