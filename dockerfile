FROM python:3.8-slim

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt


WORKDIR /app
ADD . /app


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
