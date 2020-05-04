from django.db import models
from apps.myauth.models import Consumer, Author


class Subscription(models.Model):
    who = models.ForeignKey(Consumer, related_name='subscriptions', on_delete=models.CASCADE)
    on_whom = models.ForeignKey(Author, related_name='subscribers', on_delete=models.CASCADE)
