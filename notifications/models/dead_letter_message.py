from django.db import models

class DeadLetterMessage(models.Model):
    topic = models.CharField(max_length=255)
    message_data = models.JSONField()
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"DeadLetterMessage(topic={self.topic})"