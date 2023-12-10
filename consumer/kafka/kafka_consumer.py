from confluent_kafka import Consumer, KafkaError
from mongo.mongodb import save_pepper, save_potato, save_tomato
import os
import json

running = True


def get_kafka_server_url():
    file = None
    try:
        env = os.environ.get("ENV") or "dev"
        file = f"kafka.{env}.json"

        print(f"Used the following Kafka config: {file}")

        with open(f"{os.getcwd()}/configs/{file}") as f:
            kafka_data = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {file} was not found in configs folder!")

    return kafka_data


def set_consumer_configs():
    kafka_config = get_kafka_server_url()

    consumer_conf = {
        'bootstrap.servers': kafka_config['bootstrap.servers'],
        'group.id': kafka_config['group.id'],
        'client.id': kafka_config['client.id'],
        'auto.offset.reset': kafka_config['auto.offset.reset']
    }

    consumer = Consumer(consumer_conf)

    print("consumer successfully set")

    return consumer


def filter_data(message):
    message_data = json.loads(message)
    if 'data' in message_data:
        message_data.pop('data')
    return message_data


def process_pepper_message(message):
    message = filter_data(message)
    print(f"Received pepper message: {message}")
    save_pepper(message)
    pass


def process_potato_message(message):
    message = filter_data(message)
    print(f"Received potato message: {message}")
    save_potato(message)
    pass


def process_tomato_message(message):
    message = filter_data(message)
    print(f"Received tomato message: {message}")
    save_tomato(message)
    pass


def consume_messages():
    consumer = set_consumer_configs()

    topics = ['pepper', 'potato', 'tomato']
    consumer.subscribe(topics)

    try:
        while running:

            msg = consumer.poll(timeout=11.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    continue

            received_message = msg.value().decode('utf-8')

            topic = msg.topic()

            if topic is None:
                print(f"Unknown topic")
                continue

            if topic == 'pepper':
                process_pepper_message(received_message)
            elif topic == 'potato':
                process_potato_message(received_message)
            elif topic == 'tomato':
                process_tomato_message(received_message)

    finally:
        consumer.close()
        print("Error consuming message")


def shutdown():
    running = False
