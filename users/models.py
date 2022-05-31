from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from stock_exchange.game_config import DEFAULT_BALANCE


class CustomUser(AbstractUser):
    balance = models.FloatField(
        'Баланс', default=DEFAULT_BALANCE, validators=[MinValueValidator(0)]
    )


User = CustomUser


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
