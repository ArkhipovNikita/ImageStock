from django.db import models
from django.contrib.postgres.fields import ArrayField


class MailingHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    receivers = ArrayField(models.EmailField())

