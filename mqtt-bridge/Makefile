
.PHONY: build

all: build

# Optional
# Simply need to have the following package installed (on archlinux):
# qemu-user-static and qemu-user-static-binfmt.
multiarch:
	sudo podman run --rm --privileged docker.io/multiarch/qemu-user-static --reset -p yes

build:
	podman build --arch arm --override-arch arm -t mqtt-bridge .

deploy:
	podman tag mqtt-bridge registry.home.arpa:5000/mqtt-bridge
	podman push registry.home.arpa:5000/mqtt-bridge

