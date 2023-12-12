FROM alpine:3.19.0

RUN apk add python3 py3-pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

RUN which python3

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
