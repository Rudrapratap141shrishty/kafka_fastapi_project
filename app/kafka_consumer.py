import os
import json

from dotenv import load_dotenv

from kafka import KafkaConsumer

load_dotenv()


KAFKA_SERVER = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC"
)

GROUP_ID = os.getenv(
    "KAFKA_GROUP_ID"
)


consumer = KafkaConsumer(

    KAFKA_TOPIC,

    bootstrap_servers=KAFKA_SERVER,

    group_id=GROUP_ID,

    auto_offset_reset="earliest",

    enable_auto_commit=True,

    key_deserializer=lambda key:
        int(key.decode())
        if key else None,

    value_deserializer=lambda value:
        json.loads(
            value.decode("utf-8")
        )
)


print("Kafka consumer started...")


for message in consumer:

    print("\nNew order received")

    print(
        "Topic:",
        message.topic
    )

    print(
        "Partition:",
        message.partition
    )

    print(
        "Offset:",
        message.offset
    )

    print(
        "Order:",
        message.value
    )