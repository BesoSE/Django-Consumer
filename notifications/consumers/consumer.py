import logging
import pulsar
from django.conf import settings

from pulsar.schema import JsonSchema
from pulsar_schemas.schemas.order import Order
from pulsar_schemas.schemas.user import User

logger = logging.getLogger(__name__)
schemas = {
    "order": Order,
    "user": User,
    "order-DTL": Order,
    "user-DTL": User,
}

class Consumer():
    def __init__(self, topic, message_listener, dead_letter_topic=None):
        self.__client = pulsar.Client(settings.PULSAR_HOST)
        self.__topic = topic
        self.__message_listener=message_listener
        self.schema = self.get_schema()
        self.dead_letter_topic = dead_letter_topic


    def subscribe(self):
        dead_letter_policy = None
        if self.dead_letter_topic:
            dead_letter_policy = pulsar.ConsumerDeadLetterPolicy(
                max_redeliver_count=3,
                dead_letter_topic=self.dead_letter_topic
            )

        self.__client.subscribe(
                                topic=self.get_topic(),
                                subscription_name="my-sub",
                                schema=JsonSchema(self.schema),
                                message_listener=self.__message_listener,
                                consumer_type=pulsar.ConsumerType.Shared,
                                dead_letter_policy=dead_letter_policy
                                )
        logging.info(f"Subscribed to topic: {self.__topic}")
        return self


    # based on tenant and namespace you can get topic
    def get_topic(self):
        return self.__topic

    def get_schema(self):
        return schemas[self.__topic]