NAME = hivebox
VERSION="0.0.1"
IMAGE = $(NAME):$(VERSION)
APPDIR="app"

all: build forced_run

start:
	@docker start $(NAME)

stop:
	@docker stop $(NAME)

reload: stop start

run:
	@docker run --env-file app/.env -p 8080:80 --name $(NAME) $(IMAGE)

detached:
	@docker run --env-file app/.env -d -p 8080:80 --name $(NAME) $(IMAGE)

temp_run:
	@docker run --env-file app/.env --name $(NAME) $(IMAGE) --rm

build:
	@docker build -t $(IMAGE) $(APPDIR)

logs:
	@docker logs $(NAME)

clean:
	@docker rm -f hivebox || true

fclean: clean
	@docker rmi $(IMAGE) || true

re: fclean build detached

.PHONY: run build clean
