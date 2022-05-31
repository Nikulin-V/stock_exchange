from django.urls import path

from companies.views import CompanyView, CompaniesView, NewCompanyView

urlpatterns = [
    path('', CompaniesView.as_view(), name='companies'),
    path('new/', NewCompanyView.as_view(), name='new_company'),
    path('<str:company_name>/', CompanyView.as_view(), name='company'),
]
