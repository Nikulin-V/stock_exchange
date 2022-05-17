from django.shortcuts import render
from django.views import View

from companies.models import Company, Photo


class CompanyView(View):
    template = 'companies/company.html'

    def get(self, request, pk):
        company = Company.objects.filter(pk=pk) \
            .select_related('industry').prefetch_related('owners') \
            .only('name', 'is_active', 'industry__name', 'description',
                  'owners__first_name', 'upload') \
            .first()
        photos = Photo.objects.filter(company=company)
        context = {'company': company, 'photos': photos}
        return render(request, self.template, context)
