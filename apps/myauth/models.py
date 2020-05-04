from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from .managers import UserManager
from .signals import auto_delete_file_on_change


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='imgs/avatars/',
                               default='imgs/avatars/base_avatar.jpg', blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        pre_save.connect(auto_delete_file_on_change, sender=cls)

    def get_short_name(self):
        return self.username


class Author(User):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class Consumer(User):
    pass
