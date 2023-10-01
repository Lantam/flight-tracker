FROM python:3.11.2

WORKDIR /usr/src/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/src/entrypoint.sh
RUN chmod +x /usr/src/src/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/src/entrypoint.sh"]
