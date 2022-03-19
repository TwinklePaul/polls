FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /polls

COPY Pipfile Pipfile.lock /polls/

RUN pip install pipenv && pipenv install --system

COPY . /polls/