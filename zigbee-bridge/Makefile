
.PHONY: build

all: build

build:
	podman build --arch arm --override-arch arm -t zigbee-bridge .

deploy:
	podman tag zigbee-bridge registry.home:5000/zigbee-bridge
	podman push registry.home:5000/zigbee-bridge

