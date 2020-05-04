from django.db import models
from apps.image_handling.models import Image
from apps.myauth.models import Author


class Collection(models.Model):
    name = models.CharField(max_length=30, unique=True)
    author = models.ForeignKey(Author, related_name='collections', on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(default='imgs/author_works/coll_covers/base_cover.jpg',
                              upload_to='imgs/author_works/coll_covers/',
                              blank=True)
    # subscribers

    def __str__(self):
        return '%s' % self.name
