FROM python:3.7
MAINTAINER  Dulatov Omurbek <oma.dulatov@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system

COPY ./docker/django/start.sh /start.sh
RUN chmod +x /start.sh

COPY . .

EXPOSE 8000