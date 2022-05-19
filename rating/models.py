from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from companies.models import Company
from users.models import CustomUser


class RatingManager(models.Manager):
    def get_queryset(self):
        return super(RatingManager, self).get_queryset().filter(company__is_active=True).all()


class Rating(models.Model):
    rating = RatingManager()

    points = models.IntegerField(
        'Очки доверия',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Компания',
        on_delete=models.CASCADE,
        related_name='rating',
    )
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} ({self.points}) - {self.user.username}'

    class Meta:
        verbose_name = 'Очки доверия'
        verbose_name_plural = 'Очки доверия'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'user'],
                name='Пользователь может дать очки доверия компании только один раз.',
            )
        ]
