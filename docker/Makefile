all:
	docker compose -f srcs/docker-compose.yml up --build

up:
	docker compose -f srcs/docker-compose.yml up
	# docker compose -f srcs/docker-compose.yml up --detach

stop:
	docker compose -f srcs/docker-compose.yml stop

down:
	docker compose -f srcs/docker-compose.yml down

restart: stop up

clean:
	docker compose -f srcs/docker-compose.yml down -v 

fclean: clean
	find avatars/ -type d -mindepth 1 -exec rm -rf {} +
	docker image rm transcendence-backend
	docker image rm postgres
	docker image rm transcendence-nginx
	docker image prune

re: fclean all

clean-docker:
	docker system prune -af --volumes

reset:
	docker stop $(shell docker ps -qa); docker rm $(shell docker ps -qa); docker rmi -f $(shell docker images -qa); docker volume rm $(shell docker volume ls -q); docker network rm $(shell docker network ls -q) 2>/dev/null

sh-backend:
	docker exec -it backend /bin/bash

sh-postgres:
	docker exec -it postgres /bin/bash

.PHONY: all start stop down restart clean fclean re clean-docker reset