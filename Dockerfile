FROM python:3.11.2

WORKDIR /flight_tracker

COPY requirements.txt .

RUN apt-get update && pip install --upgrade pip && pip install -r requirements.txt

COPY . .
