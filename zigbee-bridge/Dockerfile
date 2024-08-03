FROM alpine:3.20.2

RUN apk add python3 py3-paho-mqtt

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
