FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]