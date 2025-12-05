import json
import logging

from notifications.consumers.consumer import Consumer
from notifications.models.dead_letter_message import DeadLetterMessage
from notifications.models.user import User
from notifications.notification_service import NotificationService

logger = logging.getLogger("consumer")

class DeadLetterConsumer(Consumer):
    def __init__(self, topics):
        """
        Initializes a consumer that listens to multiple Dead Letter Topics.
        :param topics: List of dead-letter topics to subscribe to.
        """
        self.consumers = [
            Consumer(topic=f"{topic}-DTL", message_listener=self.dead_letter_message_listener)
            for topic in topics
        ]

    def dead_letter_message_listener(self, consumer, message):
        """
        Custom message listener function for processing messages.
        """
        try:
            data = message.value()
            action = message.properties().get('action', None)
            logger.info(f"Received dead letter topic message: {data}")
            logger.info(f"Action: {action}")
            DeadLetterMessage.objects.create(
                topic=message.topic_name(),
                message_data=json.loads(message.data().decode('utf-8')),
                action=action,
            )
        except Exception as e:
            logger.error(f"Error processing order message: {e}", exc_info=True)
            NotificationService.send_pulsar_notification(message)
        finally:
            consumer.acknowledge(message)  

    def subscribe(self):
        """
        Subscribes to all dead-letter topics.
        """
        for consumer in self.consumers:
            consumer.subscribe()
        logger.info("Subscribed to multiple dead-letter topics")
