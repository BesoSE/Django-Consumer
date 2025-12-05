import json
import logging

from notifications.consumers.consumer import Consumer
from notifications.models.user import User

logger = logging.getLogger("consumer")


class UserConsumer(Consumer):
    def __init__(self, topic="user", *args, **kwargs):
        """
        Initializes the UserConsumer for consuming messages on the 'user' topic.
        Inherits from the base Consumer class.
        """
        # Initialize the parent Consumer class
        super().__init__(topic=topic, message_listener=self.user_message_listener, dead_letter_topic=f"{topic}-DTL", *args, **kwargs)

    def user_message_listener(self, consumer, message):
        """
        Custom message listener function for processing user messages.
        """
        try:
            user_data = message.value()
            action = message.properties().get('action', None)
            logger.info(f"Received user message: {user_data}")
            logger.info(f"Action: {action}")
            if action == 'INSERT' or action == 'UPDATE':
                User.objects.update_or_create(
                    email=user_data.email,
                    defaults={ 
                        'first_name': user_data.first_name,
                        'last_name': user_data.last_name,
                        'status': user_data.status,
                        'phone': user_data.phone,
                        'address': user_data.address,
                        }
                )
            elif action == 'DELETE':
                User.objects.filter(email=user_data.email).delete()
            consumer.acknowledge(message)  
        except Exception as e:
            logger.error(f"Error processing user message: {e}", exc_info=True)
            consumer.negative_acknowledge(message)
