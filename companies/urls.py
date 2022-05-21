from django.contrib.auth.decorators import login_required
from django.urls import path

from companies.views import *

urlpatterns = [
    path(
        'new/',
        login_required(NewCompanyView.as_view()),
        name='new_company'
    ),
    path(
        '<str:company_name>/',
        CompaniesView.as_view(),
        name='company'
    ),
]
