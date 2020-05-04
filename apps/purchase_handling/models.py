from django.db import models

from apps.image_handling.models import Image
from apps.myauth.models import Consumer, Author


class Purchase(models.Model):
    buyer = models.ForeignKey(Consumer, related_name='purchases', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Author, related_name='sales', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, related_name='buyers', on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=12)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total = self.image.price
        super(Purchase, self).save()
