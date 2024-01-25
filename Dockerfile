FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY skbox .

COPY req.txt req.txt

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev

RUN pip install --upgrade pip
RUN pip install -r req.txt

CMD python manage.py runserver 0.0.0.0:8000




