
.PHONY: build

all: build

multiarch:
	sudo podman run --rm --privileged docker.io/multiarch/qemu-user-static --reset -p yes

build: multiarch
	podman build --arch arm --override-arch arm -t zigbee-bridge .

deploy:
	podman tag zigbee-bridge registry.home:5000/zigbee-bridge
	podman push registry.home:5000/zigbee-bridge

