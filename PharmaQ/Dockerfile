FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=project.settings_exam

EXPOSE 8000

CMD ["gunicorn", "PharmaQ.wsgi:application", "--workers", "2", "--bind", "0.0.0.0:8000"]