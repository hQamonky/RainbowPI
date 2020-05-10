# FROM alpine:latest
FROM arm32v7/python:3

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Intall the rpi.gpio python module
# RUN pip install --no-cache-dir rpi.gpio

COPY . .

CMD [ "python3", "./run.py" ]