from __future__ import print_function
from cmath import inf

from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType, ArrayType
from pyspark.sql.functions import from_json, col

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


messageSchema = StructType([
    StructField("key", ArrayType(StringType(), False)),
    StructField("value", ArrayType(FloatType(), False)),
    StructField("ts", IntegerType(), False)
])


class InfluxDBWriter:
    def __init__(self):
        self._token = '2c83186a-caab-425a-9594-9d4c00544939'
        self._org = 'primary'
        self.client = influxdb_client.InfluxDBClient(
            url="http://localhost:8086", token=self._token, org=self._org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def open(self, partition_id, epoch_id):
        print("Opened %d, %d" % (partition_id, epoch_id))
        return True

    def process(self, row):
        self.write_api.write(bucket='primary',
                             record=self._row_to_line_protocol(row))

    def close(self, error):
        self.write_api.__del__()
        self.client.__del__()
        print("Closed with error: %s" % str(error))

    def _row_to_line_protocol(self, row):
        print(row)
        
        if len(row['key']) > 1:
            if row['key'][0] == 'wind_speed_max' and row['key'][1] == 'wind_speed_min' and row['key'][2] == 'wind_dir':
                if round((row['value'][0] + row['value'][1])/2, 2) > inf:
                    print('WIND SPEED WARNING!')
                return influxdb_client.Point.measurement("wind_speed").tag("measure", "WIND") \
                    .field("Max", row['value'][0]).field("Min", row['value'][1]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .field("Dir", row['value'][2]) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'wind_speed_max2' and row['key'][1] == 'wind_speed_min2' and row['key'][2] == 'wind_dir2':
                if round((row['value'][0] + row['value'][1])/2, 2) > inf:
                    print('WIND SPEED 2 WARNING!')
                return influxdb_client.Point.measurement("wind_speed_2").tag("measure", "WIND") \
                    .field("Max", row['value'][0]).field("Min", row['value'][1]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .field("Dir", row['value'][2]) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'humidity_min' and row['key'][1] == 'humidity_max':
                if round((row['value'][0] + row['value'][1])/2, 2) > 90:
                    print('\n---------- HUMIDITY WARNING - Possibile attacco di bolla! ----------\n')
                return influxdb_client.Point.measurement("humidity").tag("measure", "HUM") \
                    .field("Max", row['value'][1]).field("Min", row['value'][0]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'humidity_min2' and row['key'][1] == 'humidity_max2':
                if round((row['value'][0] + row['value'][1])/2, 2) > 90:
                    print('\n---------- HUMIDITY 2 WARNING - Possibile attacco di bolla! ----------\n')
                return influxdb_client.Point.measurement("humidity_2").tag("measure", "HUM") \
                    .field("Max", row['value'][1]).field("Min", row['value'][0]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'temperature_min' and row['key'][1] == 'temperature_max':
                if round((row['value'][0] + row['value'][1])/2, 2) > inf:
                    print('TEMP WARNING!')
                return influxdb_client.Point.measurement("temperature").tag("measure", "TEMP") \
                    .field("Max", row['value'][1]).field("Min", row['value'][0]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'temperature_min2' and row['key'][1] == 'temperature_max2':
                if round((row['value'][0] + row['value'][1])/2, 2) > inf:
                    print('TEMP 2 WARNING!')
                return influxdb_client.Point.measurement("temperature_2").tag("measure", "TEMP") \
                    .field("Max", row['value'][1]).field("Min", row['value'][0]).field("Mean", round(((row['value'][0] + row['value'][1])/2), 2)) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'top_page_raw' and row['key'][1] == 'bottom_page_raw' and row['key'][2] == 'top_page_perc' and row['key'][3] == 'bottom_page_perc':
                if round(row['value'][0], 2) > inf or round(row['value'][1], 2) > inf or round(row['value'][2], 2) > inf or round(row['value'][3], 2) > inf:
                    print('WARNING!')
                return influxdb_client.Point.measurement("leaf_wetness").tag("measure", "LW") \
                    .field("TopPageRaw", row['value'][0]).field("BottomPageRaw ", row['value'][1]) \
                    .field("TopPagePerc", row['value'][2]).field("BottomPagePerc ", row['value'][3]) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'top_page_raw2' and row['key'][1] == 'bottom_page_raw2' and row['key'][2] == 'top_page_perc2' and row['key'][3] == 'bottom_page_perc2':
                if round(row['value'][0], 2) > inf or round(row['value'][1], 2) > inf or round(row['value'][2], 2) > inf or round(row['value'][3], 2) > inf:
                    print('WARNING!')
                return influxdb_client.Point.measurement("leaf_wetness_2").tag("measure", "LW") \
                    .field("TopPageRaw", row['value'][0]).field("BottomPageRaw ", row['value'][1]) \
                    .field("TopPagePerc", row['value'][2]).field("BottomPagePerc ", row['value'][3]) \
                    .time(row['ts'], write_precision='s')
        else:
            if row['key'][0] == 'rain':
                return influxdb_client.Point.measurement("rain").tag("measure", "RAIN") \
                    .field("Value", row['value'][0]) \
                    .time(row['ts'], write_precision='s')

            elif row['key'][0] == 'solar':
                return influxdb_client.Point.measurement("solar").tag("measure", "SOLAR") \
                    .field("Value", row['value'][0]) \
                    .time(row['ts'], write_precision='s')


if __name__ == "__main__":

    # initialize the SparkSession
    spark = SparkSession \
        .builder \
        .appName("Structured Streaming application with Kafka") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    # DF that is cyclically reads events from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test, test2, anemometer, anemometer2, humidity_sensor, humidity_sensor2, leaf_wetness, leaf_wetness2, \
            rain_sensor, solar_radiation, thermometer, thermometer2") \
        .load()

    df.printSchema()
    
    df1 = df.selectExpr("CAST(value AS STRING)").select(
        from_json(col("value"), messageSchema).alias("data")).select("data.*")

    df1.printSchema()

    # Save on DB
    df1.writeStream \
        .foreach(InfluxDBWriter()) \
        .start() \
        .awaitTermination()

    # Print console
    # df1.writeStream \
    #     .outputMode("update") \
    #     .format("console") \
    #     .option("truncate", False) \
    #     .start() \
    #     .awaitTermination()

    df1.show()
