FROM alpine:3.21.0

RUN apk add python3 py3-paho-mqtt

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
