from django.shortcuts import render
from django.views import View

from marketplace.models import Lot


class MarketplaceView(View):
    template = 'marketplace/marketplace.html'

    def get(self, request):
        context = {
            'user_lots': Lot.lots.get_user_lots(),
            'sell_lots': Lot.lots.get_sell_lots()
        }
        return render(request, self.template, context)
