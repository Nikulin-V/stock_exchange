from django.urls import path

from marketplace.views import MarketplaceView, SellSharesView

urlpatterns = [
    path('', MarketplaceView.as_view(), name='marketplace'),
    path('sell-shares/', SellSharesView.as_view(), name='sell-shares')
]
