import time
import json
import sys
from kafka import KafkaProducer

IOT_NAME = None

def generate_messages(keys, timestamp, values):
    messages = {
        "key": keys,
        "value": values, 
        "ts": timestamp,
    }
    print(messages)
    return json.dumps(messages).encode('UTF-8')

if __name__ == "__main__":
    IOT_NAME = sys.argv[1]

    print('IOT_NAME: ', IOT_NAME)

    producer = KafkaProducer(bootstrap_servers='kafka:9093') # local -> localhost:9092
    print(producer)
    print()

    with open('./data/' + IOT_NAME + '.json') as jsonFile:
        data = json.load(jsonFile)
        keys = data.keys()

        for i in reversed(range(len(data[list(keys)[0]]))):
            print('sent message: ')
            values = []
            timestamp = int(data[list(keys)[0]][i]['ts']/1000)
            new_keys = []
            for key in keys:
                if key != None and 'average' not in key:
                    if "2" in IOT_NAME:
                        new_keys.append(key + "2")
                    else:
                        new_keys.append(key)
                    values.append(round(float(data[key][i]['value']), 2))
            producer.send(IOT_NAME, generate_messages(new_keys, timestamp, values))
            time.sleep(5)
