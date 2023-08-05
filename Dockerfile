FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

RUN pip install poetry

ADD . /src

WORKDIR /src

RUN poetry install

CMD ["poetry","run","autonodelabel","-v","-s"]
