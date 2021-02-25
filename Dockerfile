FROM python:3.8.5-buster

LABEL MAINTAINER="gabin.lanore@gmail.com"

ENV PATH="/app:${PATH}"
ENV DOCKER_MODE=True

ENV IP_RANGE_LIST="192.168.0.0/24"
ENV MONGO_URL="mongodb://mongo:27017/"
ENV MONGO_DB_NAME="ipisinthisdb"

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "TouDoum.py" ]