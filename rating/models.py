from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class RatingManager(models.Manager):
    def get_queryset(self):
        return super(RatingManager, self).get_queryset().filter(company__is_active=True).all()

    def get_companies_rating_dict(self):
        from companies.models import Industry, Company
        rating_dict = {}
        industries_names = Industry.industries.all()
        for industry in industries_names:
            industry_companies = Company.companies.filter(is_active=True, industry=industry)
            if industry_companies:
                rating_dict[industry.name] = {'total_points': 0}
                for company in industry_companies:
                    rating_dict[industry.name][company.name] = 0
        for user in CustomUser.objects.all():
            for industry in industries_names:
                industry_companies = Company.companies.filter(is_active=True, industry=industry)
                if industry_companies:
                    points = 100
                    rating_dict[industry.name]['total_points'] += points
                    for company in industry_companies:
                        company_points = self.get_queryset().filter(user=user, company=company)
                        if company_points:
                            points -= company_points[0].points
                            rating_dict[industry.name][company.name] = company_points[0].points
                    if points != 0:
                        odd_points_per_company = points / len(industry_companies)
                        for company in industry_companies:
                            rating_dict[industry.name][company.name] += odd_points_per_company
        return rating_dict


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
