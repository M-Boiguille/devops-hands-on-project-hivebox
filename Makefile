ifneq (,$(wildcard app/.env))
include app/.env
export
endif

NAME = hivebox
VERSION = $(APP_VERSION)
IMAGE = $(NAME):$(VERSION)
APPDIR = app

.PHONY: all start stop reload run detached temp_run build logs clean fclean re

all: build detached

start:
	docker start $(NAME)

stop:
	docker stop $(NAME)

reload: stop start

run:
	docker run --env-file app/.env -p 8080:80 --name $(NAME) $(IMAGE)

detached:
	docker run --env-file app/.env -d -p 8080:80 --name $(NAME) $(IMAGE)

temp_run:
	docker run --env-file app/.env --rm $(IMAGE)

build:
	docker build -t $(IMAGE) $(APPDIR)

logs:
	docker logs $(NAME)

clean:
	docker rm -f $(NAME) || true

fclean: clean
	docker rmi $(IMAGE) || true

re: fclean build detached
