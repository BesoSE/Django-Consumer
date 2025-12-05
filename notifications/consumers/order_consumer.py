from datetime import datetime
import logging

from notifications.consumers.consumer import Consumer
from notifications.models.user import User
from notifications.notification_service import NotificationService

logger = logging.getLogger("consumer")
NOTIFICATION_MESSAGES = {
    'INSERT': "Your order has been placed successfully!",
    'UPDATE': "Your order details have been updated.",
    'DELETE': "Your order has been cancelled."
}

class OrderConsumer(Consumer):
    def __init__(self, topic="order", *args, **kwargs):
        """
        Initializes the OrderConsumer for consuming messages on the 'order' topic.
        Inherits from the base Consumer class.
        """
        # Initialize the parent Consumer class
        super().__init__(topic=topic, message_listener=self.order_message_listener, dead_letter_topic=f"{topic}-DTL", *args, **kwargs)

    def order_message_listener(self, consumer, message):
        """
        Custom message listener function for processing order messages.
        """
        try:
            order_data = message.value()
            action = message.properties().get('action', None)
            user = User.objects.get(email=order_data.email)
            logger.info(f"Received order message: {order_data}")
            logger.info(f"Action: {action}")
            # created_at = datetime.strptime(order_data.created_at, "%Y-%m-%d %H:%M:%S")

            NotificationService.send_notification(user, order_data, NOTIFICATION_MESSAGES.get(action,  "Order notification received."))
            consumer.acknowledge(message)  
        except Exception as e:
            logger.error(f"Error processing order message: {e}", exc_info=True)
            consumer.negative_acknowledge(message)
