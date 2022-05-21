from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import SocketAuthView

from companies.views import CompaniesView
from homepage.views import HomeView
from marketplace.views import MarketplaceView
from stock_exchange import settings

urlpatterns = (
        [
            path('admin/', admin.site.urls),
            path('', HomeView.as_view()),
            path('auth/', include('users.urls')),
            path('marketplace/', MarketplaceView.as_view()),
            path('tinymce/', include('tinymce.urls')),
            path('companies/<str:company_name>/', CompaniesView.as_view()),
            path('socket-auth/', SocketAuthView.as_view()),
        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
