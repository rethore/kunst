build:
	sudo docker build -t piredtu/kunst_meteor kunst
	sudo docker build -t piredtu/kunst_python python

push:
	sudo docker push piredtu/kunst_meteor
	sudo docker push piredtu/kunst_python

recreate:
	sudo docker rm kunst_meteor_1
	sudo docker rm kunst_python_1

up:
	sudo docker-compose up -d

stop:
	sudo docker-compose stop

log_python:
	sudo docker logs -f kunst_python_1

log_meteor:
	sudo docker logs -f kunst_meteor_1
