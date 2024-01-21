FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY req.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY skbox .




