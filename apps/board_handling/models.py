from django.db import models

from apps.image_handling.models import Image
from apps.myauth.models import Consumer


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(Consumer, related_name='boards', on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    # cover

    def __str__(self):
        return '%s' % self.name
