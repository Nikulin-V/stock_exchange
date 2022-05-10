from django.contrib import admin
from django.urls import path, include

from homepage.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('auth/', include('users.urls')),
]
