#!/usr/bin/bash


echo -e "\n[ Cleaning docker ]\n"

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

echo -e "\n[ Building Docker ]\n"

docker-compose build

echo -e "\n[ Starting Docker Compose ]\n"
docker-compose up -d

docker exec django_api python manage.py makemigrations authentication
docker exec django_api python manage.py migrate --noinput

