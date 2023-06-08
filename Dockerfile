FROM python:3.11-alpine

RUN pip install poetry

ADD . /src

WORKDIR /src

RUN poetry install