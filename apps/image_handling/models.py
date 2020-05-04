import os
from django.db import models
from apps.myauth.models import Author


class Image(models.Model):
    author = models.ForeignKey(Author, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')
    category = models.ForeignKey('Category', related_name='images', on_delete=models.CASCADE)
    original = models.ImageField(upload_to='imgs/author_works/originals')
    with_label = models.ImageField(upload_to='imgs/author_works/with_label', null=True)
    purchase_count = models.IntegerField(default=0)

    def delete(self, using=None, keep_parents=False):
        def delete_file(path):
            if os.path.isfile(path):
                os.remove(path)
        super(Image, self).delete(using, keep_parents)
        original = self.original
        with_label = self.with_label
        delete_file(original.path)
        if with_label:
            delete_file(with_label.path)

    def __str__(self):
        return '%s' % self.name


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.lower()
        super(Tag, self).save()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name
