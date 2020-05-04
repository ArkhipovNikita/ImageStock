import os
from django.db import models
from django.dispatch import receiver


@receiver(models.signals.pre_save, sender='myauth.User')
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        old_path = os.path.relpath(old_file.path)
        default_path = os.path.join('media', sender._meta.get_field('avatar').default)
        if os.path.isfile(old_file.path) and old_path != default_path:
            os.remove(old_file.path)
