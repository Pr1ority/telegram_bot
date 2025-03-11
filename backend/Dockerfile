FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY backend/ .

RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["gunicorn", "telegram_bot.wsgi:application", "--bind", "0.0.0.0:8080"]