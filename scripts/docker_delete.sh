#!/usr/bin/bash

docker-compose rm --all -f
find . -path "apps/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "apps/*/migrations/*.pyc"  -delete

docker-compose ps

docker ps

docker stop $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)
docker volume rm -f $(docker volume ls  -q)
