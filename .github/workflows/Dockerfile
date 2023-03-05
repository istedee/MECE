FROM python:3.8-slim-buster

WORKDIR /code


COPY requirements.txt .


RUN pip install -r requirements.txt

COPY ./app .


CMD [ "uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000", "--reload"]
