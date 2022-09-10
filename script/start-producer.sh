#!/usr/bin/env bash

docker cp ../iot-data-producer/iot-producer.py iot-source:./home/
docker exec -it iot-source rm -rf ./home/data
docker cp ../iot-data-producer/data iot-source:./home/
docker cp ../iot-data-producer/start-producer.sh iot-source:./home/
docker exec -it iot-source /bin/bash start-producer.sh