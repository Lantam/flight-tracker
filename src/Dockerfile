FROM python:3.11.2

WORKDIR /usr/src/app

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401,W503 ./flight_tracker ./map

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
