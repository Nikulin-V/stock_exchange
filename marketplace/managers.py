from django.db import models

from companies.models import Company
from marketplace.models import Lot
from stock_exchange.middleware import get_current_user
from users.models import CustomUser


class SharesManager(models.Manager):
    def get_user_companies(self, user: CustomUser) -> list[Company.name]:
        """
        Get companies where user is stockholder

        :param user: current user object
        :return: list of companies where user is stockholder
        """
        return sorted(
            self.get_queryset()
            .filter(user=user, company__is_active=True)
            .values_list('company__name', flat=True)
        )

    def get_company_stockholders(self, company: Company) -> list[CustomUser.username]:
        """
        Get company stockholders usernames

        :param company: company object
        :return: list of company stockholders usernames
        """
        return sorted(
            self.get_queryset().filter(company=company).values_list('user__username', flat=True)
        )


class LotManager(models.Manager):
    def get_user_lots(self, user: CustomUser = get_current_user()) -> list[Lot]:
        """
        Get user lots on marketplace

        :param user: user object
        :return: list of user lots
        """
        return (
            self.get_queryset()
            .filter(user=user)
            .only('count', 'price', 'company__name', 'company__upload')
            .all()
        )

    def get_marketplace_lots(self, user: CustomUser = get_current_user()) -> list[Lot]:
        """
        Get marketplace lots except user lots

        :param user: user object
        :return: list of marketplace lots
        """
        return (
            self.get_queryset()
            .exclude(user=user)
            .only('count', 'price', 'company__name', 'company__upload', 'user__username')
            .order_by('price')
            .all()
        )
