# Dockerfile
FROM python:3.9.19-alpine

WORKDIR /app

COPY    requirements.txt    /app
COPY    .env        /app
COPY    api.py      /app
COPY    app.py      /app
COPY    elastic.py  /app
COPY    movies.json /app
COPY    Redis.py    /app

RUN pip install -r requirements.txt


CMD ["python", "app.py"]
