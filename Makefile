# TODO: make all to include elk etc
#in case of emergency: sudo systemctl restart docker.socket docker.service
# sudo lsof -i :80; sudo kill -9 <PID>

all:
	sudo sysctl -w vm.max_map_count=262144
	# docker compose up --build backend nginx postgres
	docker compose up -d --build backend nginx postgres

up:
	# docker compose up
	docker compose up --detach

elk:
	docker compose up --build setup es01 kibana logstash01

stop:
	docker compose stop

down:
	docker compose down

restart: stop up

clean:
	docker compose down -v

fclean: clean
	sudo find docker/avatars/ -mindepth 1 -type d -exec rm -rf {} +
	docker image rm transcendence-backend
	# docker image rm postgres:17.2
	docker image rm transcendence-nginx
	rm -rf .docker/srcs/elk/esbackup/*
	# docker image prune

re: fclean all

clean-docker:
	docker system prune -af --volumes

reset:
	docker stop $(shell docker ps -qa); docker rm $(shell docker ps -qa); docker rmi -f $(shell docker images -qa); docker volume rm $(shell docker volume ls -q); docker network rm $(shell docker network ls -q) 2>/dev/null

sh-backend:
	docker exec -it backend /bin/bash

sh-postgres:
	docker exec -it postgres /bin/bash

ip-host:
	@docker/srcs/backend/tools/iphost.sh

.PHONY: all start stop down restart clean fclean re clean-docker reset dev sh-backend sh-postgres ip-host