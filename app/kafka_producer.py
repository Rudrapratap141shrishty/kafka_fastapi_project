import os
import json

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

KAFKA_SERVER = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC"
)


producer = KafkaProducer(

    bootstrap_servers=KAFKA_SERVER,

    key_serializer=lambda key:
        str(key).encode("utf-8"),

    value_serializer=lambda value:
        json.dumps(value).encode("utf-8")
)


def send_order_event(order):

    future = producer.send(
        KAFKA_TOPIC,
        key=order["id"],
        value=order
    )

    metadata = future.get(timeout=10)

    print(
        "Kafka event sent:",
        metadata.topic,
        metadata.partition,
        metadata.offset
    )