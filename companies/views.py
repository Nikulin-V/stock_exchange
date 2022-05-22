from django.db.models import Prefetch, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from companies.forms import NewCompanyForm
from companies.models import Company, Photo
from marketplace.models import Shares
from rating.models import Rating


class CompaniesView(View):
    template = 'companies/companies.html'

    def get(self, request):
        companies = (
            Company.companies.filter(is_active=True)
            .select_related('industry').prefetch_related(
                Prefetch('rating', queryset=Rating.rating.all()))
            .only('name', 'industry__name', 'upload')
            .annotate(sum_points=Sum('rating__points'))
            .order_by('industry__name', '-sum_points')
            .all()
        )

        industry_sort = dict()
        for company in companies:
            if company.industry in industry_sort:
                industry_sort[company.industry].append(company)
            else:
                industry_sort[company.industry] = [company]

        context = {'companies_by_industry': industry_sort}
        return render(request, self.template, context)


class CompanyView(View):
    template = 'companies/company.html'

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


class NewCompanyView(View):
    template = 'companies/new_company.html'
    form = NewCompanyForm

    def get(self, request):
        form = self.form()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        def save_photo(photo, company):
            Photo.objects.create(upload=photo, company=company).save()

        form = self.form(request.POST, request.FILES)
        context = {'form': form}
        if form.is_valid():
            user = request.user
            if user.balance >= 500:
                user.balance -= 500
                user.save()
            else:
                form.add_error('name', 'У вас недостаточно средств')
                return render(request, self.template, context)

            company = Company.companies.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                industry=form.cleaned_data['industry'],
                upload=form.cleaned_data['logo'],
            )
            if form.cleaned_data['photo1']:
                save_photo(form.cleaned_data['photo1'], company)
            if form.cleaned_data['photo2']:
                save_photo(form.cleaned_data['photo2'], company)
            if form.cleaned_data['photo3']:
                save_photo(form.cleaned_data['photo3'], company)
            company.save()

            return HttpResponseRedirect(
                reverse('company', kwargs={'company_name': form.cleaned_data['name']}))
        return render(request, self.template, context)
