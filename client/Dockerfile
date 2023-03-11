FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt update && apt install redis-server -y

COPY . .

RUN chown -R 777 ./

