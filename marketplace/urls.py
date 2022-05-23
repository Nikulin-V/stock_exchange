from django.urls import path

from marketplace.views import MarketplaceView, SellSharesView, BuySharesView

urlpatterns = [
    path('', MarketplaceView.as_view(), name='marketplace'),
    path('buy-shares/', BuySharesView.as_view(), name='buy-shares'),
    path('sell-shares/', SellSharesView.as_view(), name='sell-shares'),
]
