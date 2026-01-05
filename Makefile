NAME = hivebox
VERSION="0.0.1"
IMAGE = $(NAME):$(VERSION)
APPDIR="app"

.PHONY: run, build, clean

run:
	@docker run --name $(NAME) $(IMAGE)

forced_run: clean run

temp_run:
	@docker run --name $(NAME) $(IMAGE) --rm

build:
	@docker build -t $(IMAGE) $(APPDIR)

clean:
	@docker rm hivebox || true
