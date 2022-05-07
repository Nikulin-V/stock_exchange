from django.contrib.auth.models import User
from django.db import models


class IndustryManager(models.Manager):
    def get_companies_by_industry(self):
        companies_by_industry = dict()
        for industry in self.get_queryset().filter(companies__is_active=True).all():
            if len(industry.companies.all()) > 0:
                companies_by_industry[industry] = industry.companies.all()
        return companies_by_industry


class Industry(models.Model):
    industries = IndustryManager()

    name = models.CharField('Название отрасли', unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'


class Company(models.Model):
    name = models.CharField('Название компании', unique=True, max_length=255)
    is_active = models.BooleanField('Активно', default=True)
    industry = models.ForeignKey(Industry, default='Другое', verbose_name='Отрасль',
                                 on_delete=models.SET_DEFAULT, related_name='companies')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Shares(models.Model):
    count = models.IntegerField('Акции')
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Акционер', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} ({self.count}) - {self.user.username}'

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'user'],
                name='У одного пользователя может быть только одно хранилище акций одной компании.'
            )
        ]
