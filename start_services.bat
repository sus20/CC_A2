@echo off

docker run -d --name image_api 12221994/image_api
docker run -d --name image_analyzer_api 12221994/image_analyzer_api
docker run -d --name users_job 12221994/users_job
docker run -d --name camera_job 12221994/camera_job
docker run -d --name leaf_disease_recognizer_job 12221994/leaf_disease_recognizer_job
docker run -d --name db_synchronizer_job 12221994/db_synchronizer_job
docker run -d --name producer_plant_db 12221994/producer_plant_db
docker run -d --name consumer_plant_db 12221994/consumer_plant_db
docker run -d --name zookeeper wurstmeister/zookeeper
docker run -d --name kafka wurstmeister/kafka