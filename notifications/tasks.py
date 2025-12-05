import logging
from celery import shared_task

from notifications.consumers.dead_letter_consumer import DeadLetterConsumer
from notifications.consumers.order_consumer import OrderConsumer
from notifications.consumers.user_consumer import UserConsumer

logger = logging.getLogger("consumer")

@shared_task
def consume_messages():
    try:
        user_consumer = UserConsumer()
        order_consumer = OrderConsumer()
        dead_letter_consumer = DeadLetterConsumer(topics=["user", "order"])
        user_consumer.subscribe()
        order_consumer.subscribe()
        dead_letter_consumer.subscribe()
    except Exception as e:
        logger.error(f"Error initializing Consumers: {e}", exc_info=True)
