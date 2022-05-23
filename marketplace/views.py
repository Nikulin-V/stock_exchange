from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from companies.models import Company
from marketplace.forms import SellSharesForm, BuySharesForm
from marketplace.models import Lot, Shares
from stock_exchange.game_config import FEE_PERCENT
from users.models import CustomUser


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
            except MultiValueDictKeyError:
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


class BuySharesView(View):
    template = 'marketplace/buy_shares.html'
    form = BuySharesForm

    def get(self, request):
        context = {}
        try:
            seller = request.GET['seller']
            company = request.GET['company']
            shares = int(request.GET['shares'])
            price = float(request.GET['price'])
            form = self.form(initial={
                'seller': seller,
                'company': company,
                'price': price,
                'shares': shares
            })
            context = {'form': form,
                       'cost': shares * price * (1 + FEE_PERCENT),
                       'fee': FEE_PERCENT * 100}
        except ValueError:
            pass
        except MultiValueDictKeyError:
            pass

        return render(request, self.template, context)

    def post(self, request):
        user = request.user
        form = self.form(request.POST)
        context = {'form': form}
        try:
            seller = CustomUser.objects.get(username=request.GET['seller'])
            company = Company.companies.get(name=request.GET['company'])
            price = float(request.GET['price'])
        except ValueError:
            context = {
                'form': form,
                'errors': ['Неверные данные формы.']
            }
            return render(request, self.template, context)
        except MultiValueDictKeyError:
            context = {
                'form': form,
                'errors': ['Неверные данные формы.']
            }
            return render(request, self.template, context)
        except ObjectDoesNotExist:
            context = {
                'form': form,
                'errors': ['Предложение недействительно.']
            }
            return render(request, self.template, context)

        if form.is_valid():
            shares = int(form.cleaned_data['shares'])

            seller_shares = Lot.lots.filter(
                company=company,
                user=seller,
                price=price
            ).all()

            if not seller_shares or seller_shares[0].count < shares:
                context = {
                    'form': form,
                    'errors': ['Предложение недействительно']
                }
                return render(request, self.template, context)

            seller_shares = seller_shares[0]
            if seller_shares.count == shares:
                seller_shares.delete()
            else:
                seller_shares.count -= shares
                seller_shares.save()

            user_shares = Shares.shares.filter(
                company=company,
                user=user
            ).all()

            if user_shares:
                user_shares[0].count += shares
                user_shares[0].save()
            else:
                Shares.shares.create(
                    company=company,
                    count=shares,
                    user=user
                )

            user.balance -= price * shares * (1 + FEE_PERCENT)
            user.save()
            seller.balance += price * shares
            seller.save()

            other_stockholders_shares = Shares.shares.filter(
                company=company
            ).exclude(user__username=user.username).all()
            if other_stockholders_shares:
                total_company_shares = sum(map(lambda x: x.count, other_stockholders_shares))
                profit_per_share = price * shares * FEE_PERCENT / total_company_shares
                for share in other_stockholders_shares:
                    stockholder = share.user
                    stockholder.balance += share.count * profit_per_share
                    stockholder.save()

            context = {
                'form': form,
                'messages': ['Акции успешно приобретены']
            }

        return render(request, self.template, context)
