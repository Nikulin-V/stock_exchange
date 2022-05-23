from django.contrib.auth.decorators import login_required
from django.urls import path

from companies.views import *

urlpatterns = [
    path(
        '',
        CompaniesView.as_view(),
        name='companies'
    ),
    path(
        'new/',
        login_required(NewCompanyView.as_view()),
        name='new_company'
    ),
    path(
        '<str:company_name>/',
        CompanyView.as_view(),
        name='company'
    ),
]
