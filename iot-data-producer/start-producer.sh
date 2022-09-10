#!/usr/bin/env bash

# python iot-producer.py test2
python iot-producer.py anemometer &
python iot-producer.py anemometer2 &
python iot-producer.py humidity_sensor &
python iot-producer.py humidity_sensor2 &
python iot-producer.py leaf_wetness &
python iot-producer.py leaf_wetness2
python iot-producer.py rain_sensor &
python iot-producer.py solar_radiation &
python iot-producer.py thermometer &
python iot-producer.py thermometer2