# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

COPY requirements.txt .

ARG DEBIAN_FRONTEND=noninteractive

RUN python3 -m pip install -r requirements.txt 

COPY app.py config.py constants.py ./

CMD ["python3", "app.py"]
