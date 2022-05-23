from django.db import models
from django.db.models import Prefetch, Sum

from rating.models import Rating


class CompanyManager(models.Manager):
    def get_sorted_companies_by_industry(self):
        return (
            self.get_queryset().filter(is_active=True)
            .select_related('industry').prefetch_related(
                Prefetch('rating', queryset=Rating.rating.all()))
            .only('name', 'industry__name', 'upload')
            .annotate(sum_points=Sum('rating__points'))
            .order_by('industry__name', '-sum_points')
        )
