
.PHONY: build

all: build

multiarch:
	sudo podman run --rm --privileged docker.io/multiarch/qemu-user-static --reset -p yes

build: multiarch
	podman build --arch arm --override-arch arm -t mqtt-bridge .

deploy:
	podman tag mqtt-bridge registry.home:5000/mqtt-bridge
	podman push registry.home:5000/mqtt-bridge

