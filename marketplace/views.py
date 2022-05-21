from django.shortcuts import render
from django.views import View

from companies.models import Company
from marketplace.forms import SellSharesForm
from marketplace.models import Lot, Shares


class MarketplaceView(View):
    template = 'marketplace/marketplace.html'

    def get(self, request):
        context = {
            'user_lots': Lot.lots.get_user_lots(),
            'marketplace_lots': Lot.lots.get_marketplace_lots(),
        }
        return render(request, self.template, context)


class SellSharesView(View):
    template = 'marketplace/sell_shares.html'

    def get(self, request):
        user = request.user
        context = {}
        if Shares.shares.get_user_companies(user):
            try:
                company = request.GET['company']
                shares = request.GET['shares']
                form = SellSharesForm(user, initial={
                    'company': company,
                    'shares': shares
                })
            except ValueError:
                form = SellSharesForm(user)
            context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        user = request.user
        context = {}
        if Shares.shares.get_user_companies(user):
            form = SellSharesForm(user, request.POST)
            context = {'form': form}
            if form.is_valid():
                company = Company.companies.get(name=form.cleaned_data['company'])
                shares = form.cleaned_data['shares']
                price = form.cleaned_data['price']

                user_shares = Shares.shares.get(
                    company=company,
                    user=user
                )
                if user_shares.count < shares:
                    context = {
                        'form': form,
                        'errors': ['Недостаточно акций в портфеле']
                    }
                    return render(request, self.template, context)

                if user_shares.count == shares:
                    user_shares.delete()
                else:
                    user_shares.count -= shares
                    user_shares.save()

                lots = Lot.lots.filter(
                    company=company,
                    price=price,
                    user=user
                ).all()
                context = {
                    'form': form,
                    'messages': ['Акции успешно выставлены на продажу.']
                }
                if lots:
                    lots[0].count += shares
                    lots[0].save()
                    context['messages'].append('Акции были добавлены к уже существующему лоту.')
                else:
                    Lot.lots.create(
                        company=company,
                        count=shares,
                        price=price,
                        user=user
                    )
                    context['messages'].append('Был создан новый лот.')

        return render(request, self.template, context)
