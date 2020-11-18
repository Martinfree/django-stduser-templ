#!/bin/bash

echo "Stoping docker"
docker-compose stop

echo "Removing Compose containers"
docker-compose rm --all -f

docker-compose ps

docker ps

echo "Removing Docker containers, images and volumes"

docker stop $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)
docker volume rm -f $(docker volume ls  -q)
