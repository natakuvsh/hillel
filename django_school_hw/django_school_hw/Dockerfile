FROM python:3.8

ENV PYTHONBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY . .


RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000

CMD celery -A django_school_hw worker -l INFO

