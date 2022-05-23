from django.db import models

from stock_exchange.middleware import get_current_user


class SharesManager(models.Manager):
    def get_company_stockholders(self, company):
        return sorted(
            self.get_queryset().
            filter(company=company).
            values_list('user__username', flat=True)
        )


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
