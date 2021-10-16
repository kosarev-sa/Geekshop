from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from datetime import timedelta

NULL_INSTALL = {'null': True, 'blank': True}
# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to = 'users_images', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, **NULL_INSTALL)

    # activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    activation_key_created = models.DateTimeField(auto_now_add=True, **NULL_INSTALL)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return True
