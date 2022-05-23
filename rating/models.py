from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class RatingManager(models.Manager):
    def get_queryset(self):
        return super(RatingManager, self).get_queryset().filter(company__is_active=True).all()

    def get_company_rating(self, company):
        return sum(
            self.get_queryset().filter(company=company).values_list('points', flat=True)
        )


class Rating(models.Model):
    rating = RatingManager()

    points = models.IntegerField(
        'Очки доверия',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    company = models.ForeignKey(
        'companies.Company',
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
