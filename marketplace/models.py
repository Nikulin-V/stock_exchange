from django.core.validators import MinValueValidator
from django.db import models

from companies.models import Company
from stock_exchange.middleware import get_current_user
from users.models import CustomUser


class SharesManager(models.Manager):
    def get_company_stockholders(self, company):
        return sorted(
            self.get_queryset().
            filter(company=company).
            values_list('user__username', flat=True)
        )


class Shares(models.Model):
    shares = SharesManager()

    count = models.PositiveIntegerField('Акции', validators=[MinValueValidator(1)])
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Акционер', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} ({self.count}) - {self.user.username}'

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'user'],
                name='У одного пользователя может быть только одно хранилище акций одной компании.',
            )
        ]


class LotManager(models.Manager):
    def get_user_lots(self, user=get_current_user()):
        return (
            self.get_queryset()
            .filter(user=user)
            .only('count', 'price', 'company__name')
            .all()
        )

    def get_marketplace_lots(self, user=get_current_user()):
        return (
            self.get_queryset()
            .exclude(user=user)
            .only('count', 'price', 'company__name', 'user__username')
            .all()
        )


class Lot(models.Model):
    lots = LotManager()

    count = models.PositiveIntegerField('Акции', validators=[MinValueValidator(1)])
    price = models.FloatField('Цена за акцию', validators=[MinValueValidator(0)])
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Акционер', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} ({self.count} * {self.price}) - {self.user.username}'

    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'price', 'user'],
                name='У одного пользователя не может быть больше одного лота акций одной компании '
                'с одинаковой ценой. ',
            )
        ]
