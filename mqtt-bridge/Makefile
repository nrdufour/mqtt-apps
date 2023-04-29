
.PHONY: build

all: build

build:
	podman build --arch arm --override-arch arm -t mqtt-bridge .

deploy:
	podman tag mqtt-bridge registry.home:5000/mqtt-bridge
	podman push registry.home:5000/mqtt-bridge

