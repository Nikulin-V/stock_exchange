from django.shortcuts import render
from django.views import View

from marketplace.models import Lot


class MarketplaceView(View):
    template = 'marketplace/marketplace.html'

    def get(self, request):
        context = {
            'user_lots': Lot.lots.get_user_lots(),
            'marketplace_lots': Lot.lots.get_marketplace_lots(),
        }
        return render(request, self.template, context)
