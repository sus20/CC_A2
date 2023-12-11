@echo off
docker stop image_api
docker stop image_analyzer_api
docker stop users_job
docker stop camera_job
docker stop leaf_disease_recognizer_job
docker stop db_synchronizer_job
docker stop producer_plant_db
docker stop consumer_plant_db
docker stop zookeeper
docker stop kafka

@echo off
docker rm -f image_api
docker rm -f image_analyzer_api
docker rm -f users_job
docker rm -f camera_job
docker rm -f leaf_disease_recognizer_job
docker rm -f db_synchronizer_job
docker rm -f producer_plant_db
docker rm -f consumer_plant_db
docker rm -f zookeeper
docker rm -f kafka
