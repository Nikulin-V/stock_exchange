from django.db import models
from django.db.models import Prefetch, Sum

from rating.models import Rating


class IndustryManager(models.Manager):
    def get_companies_by_industry(self):
        companies_by_industry = dict()
        for industry in self.get_queryset().filter(companies__is_active=True).all():
            if len(industry.companies.all()) > 0:
                companies_by_industry[industry] = industry.companies.all()
        return companies_by_industry


class CompanyManager(models.Manager):
    def get_sorted_companies_by_industry(self):
        return (
            self.get_queryset()
                .filter(is_active=True)
                .select_related('industry')
                .prefetch_related(Prefetch('rating', queryset=Rating.rating.all()))
                .only('name', 'industry__name', 'upload')
                .annotate(sum_points=Sum('rating__points'))
                .order_by('industry__name', '-sum_points')
        )
