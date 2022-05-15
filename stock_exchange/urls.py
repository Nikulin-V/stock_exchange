from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from marketplace.views import MarketplaceView
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

from homepage.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('auth/', include('users.urls')),
    path('marketplace/', MarketplaceView.as_view()),
    path('tinymce/', include('tinymce.urls')),
]

if DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
