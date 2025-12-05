from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from notifications.tasks import consume_messages
        from notifications.consumers.consumer import Consumer
        print("App is ready, triggering Celery task!")
        consume_messages.delay()