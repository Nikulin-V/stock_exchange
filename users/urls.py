from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path("signup/", views.SignupView.as_view(), name='signup'),
]
