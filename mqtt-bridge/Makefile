
.PHONY: multiarch build

all: build

multiarch:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

build: multiarch
	docker build . -t mqtt-bridge

deploy:
	docker tag mqtt-bridge registry.home:5000/mqtt-bridge
	docker push registry.home:5000/mqtt-bridge

