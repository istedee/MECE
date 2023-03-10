import json 
from kafka import KafkaConsumer

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        #bOPj3nrR
        #M8mZs81j
        #w0TnHx5p
        'bOPj3nrR',
        bootstrap_servers='kafka-route-chatexperience.rahtiapp.fi/',
        # 10.131.6.19
        #kafka-route-chatexperience.rahtiapp.fi
        auto_offset_reset='earliest',
        api_version=(0, 10, 2)
    )
    for message in consumer:
        print(json.loads(message.value))