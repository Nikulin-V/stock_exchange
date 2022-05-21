from django.shortcuts import render
from django.views import View

from companies.models import Company, Photo
from marketplace.models import Shares


class CompaniesView(View):
    template = 'companies/companies.html'

    def get(self, request, company_name):
        company = (
            Company.companies.filter(name=company_name)
            .select_related('industry')
            .only('name', 'industry__name', 'description', 'upload')
            .first()
        )
        photos = Photo.objects.filter(company=company, is_active=True).all()
        context = {
            'company': company,
            'stockholders': Shares.shares.get_company_stockholders(company),
            'photos': photos,
        }
        return render(request, self.template, context)
