from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_index=True, null=False)
    tagline = models.CharField(max_length=128, blank=True, verbose_name='тэги')
    about_me = models.TextField(blank=True, verbose_name='о себе', null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=5, verbose_name='пол')
    langs = models.CharField(max_length=128, blank=True, verbose_name='языки')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
