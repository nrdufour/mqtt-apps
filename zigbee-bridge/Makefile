
.PHONY: multiarch build

all: build

multiarch:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

build: multiarch
	docker build . -t zigbee-bridge

deploy:
	docker tag zigbee-bridge registry.home:5000/zigbee-bridge
	docker push registry.home:5000/zigbee-bridge

