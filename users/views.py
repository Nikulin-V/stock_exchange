from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from marketplace.models import Shares
from rating.models import Rating
from stock_exchange.game_config import EARNING, EARNING_TIME_SECONDS

from users.forms import UserChangeForm, UserRegistrationForm

User = get_user_model()
last_time = timezone.now()


class ProfileView(View):
    template = 'users/profile.html'
    form = UserChangeForm

    def get(self, request):
        global last_time
        if (timezone.now() - last_time).seconds >= EARNING_TIME_SECONDS:
            multiplier = (timezone.now() - last_time).seconds // EARNING_TIME_SECONDS
            last_time = timezone.now() + timedelta(seconds=(
                    (timezone.now() - last_time).seconds % EARNING_TIME_SECONDS)
            )

            data = Rating.rating.get_companies_rating_dict()
            for key in data:
                for company, percentage in data[key].items():
                    if company == 'total_points':
                        continue
                    company_profit = percentage * multiplier * EARNING / 100
                    count_count = (
                        Shares.shares.select_related('company')
                        .filter(company__name=company)
                        .aggregate(amount=Sum('count'))['amount']
                    )

                    stockholders = (
                        Shares.shares.select_related("company")
                        .filter(company__name=company)
                        .select_related("user")
                    )
                    for stockholder in stockholders:
                        user = stockholder.user
                        user.balance += stockholder.count / count_count * company_profit
                        user.save()

        user = request.user

        shares = (
            Shares.shares.filter(user=user)
            .select_related('company')
            .select_related('company__industry')
            .only(
                'count',
                'company__name',
                'company__is_active',
                'company__industry__name',
            )
            .order_by('-count', 'company__industry__name')
            .all()
        )
        form = ProfileView.form(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )
        context = {'form': form, 'shares': shares}
        return render(request, self.template, context)

    def post(self, request):
        user = request.user
        form = ProfileView.form(request.POST)
        if form.is_valid():
            user.first_name = (
                form.cleaned_data['first_name']
                if form.cleaned_data['first_name']
                else user.first_name
            )
            user.last_name = (
                form.cleaned_data['last_name'] if form.cleaned_data['last_name'] else user.last_name
            )
            user.email = form.cleaned_data['email'] if form.cleaned_data['email'] else user.email
            user.save()
            return HttpResponseRedirect(reverse('profile'))

        context = {'form': form}
        return render(request, self.template, context)


class SignupView(View):
    template = 'users/signup.html'

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
        context = {'form': form}
        return render(request, self.template, context)
