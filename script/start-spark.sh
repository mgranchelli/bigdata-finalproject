#!/usr/bin/env bash

docker cp ../spark/spark-app-docker.py spark-master:./opt/bitnami/spark/spark-app-docker.py
docker exec -it spark-master pip3 install influxdb_client
docker exec -it spark-master ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 spark-app-docker.py

# local: $SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 --master yarn spark/spark-app-local.py