DOCKER_NAME=christiandelgado7/miniredis
VERSION=1.0.0
CONTAINER_NAME=miniredis
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
REST_PORT=8080

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	docker build -t $(DOCKER_NAME_FULL) .

run:
	@docker run -it \
		-p $(REST_PORT):$(REST_PORT) \
		--name $(CONTAINER_NAME) \
		$(CONFIG) --rm $(DOCKER_NAME_FULL)

run-detached:
	@docker run -it \
		-p $(REST_PORT):$(REST_PORT) \
		--name $(CONTAINER_NAME) \
		$(CONFIG) -d $(DOCKER_NAME_FULL)
