FROM alpine:3.19.1

RUN apk add \
	python3 \
        py3-influxdb \
        py3-paho-mqtt \
        py3-msgpack

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
