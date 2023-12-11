@echo off

docker run -e ENV=dev -p 5050:5050 --name camera_job 12221994/camera_job
docker run -e ENV=dev -p 8080:8080 --name image_api 12221994/image_api
docker run -e ENV=dev -p 5051:5050 --name leaf_disease_recognizer_job 12221994/leaf_disease_recognizer_job
docker run -e ENV=dev -p 8081:8081 --name image_analyzer_api 12221994/image_analyzer_api
docker run -e ENV=dev -p 5052:5050 --name users_job 12221994/users_job
docker run -d --name producer_plant_db 12221994/producer_plant_db REM no need env



docker run -e ENV=dev -p 5051:5050 --name db_synchronizer_job 12221994/db_synchronizer_job
docker run -e ENV=dev -p --name consumer_plant_db 12221994/consumer_plant_db
docker run -d --name zookeeper wurstmeister/zookeeper
docker run -d --name kafka wurstmeister/kafka