from django.contrib.auth import get_user_model
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from companies.models import Shares

User = get_user_model()


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileView(View):
    template = 'users/profile.html'
    form = UserChangeForm

    def get(self, request):
        user = request.user
        shares = Shares.objects.filter(user=user).select_related(
            'company').select_related('company__industry').only('count', 'company__name',
                                                                'company__is_active',
                                                                'company__industry__name').order_by(
            '-count', 'company__industry__name').all()
        form = ProfileView.form(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        context = {'form': form, 'shares': shares}
        return render(request, ProfileView.template, context)

    def post(self, request):
        user = request.user
        form = ProfileView.form(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name'] if form.cleaned_data[
                'first_name'] else user.first_name
            user.last_name = form.cleaned_data['last_name'] if form.cleaned_data[
                'last_name'] else user.last_name
            user.email = form.cleaned_data['email'] if form.cleaned_data[
                'email'] else user.email
            user.save()
            return HttpResponseRedirect(reverse('profile'))

        context = {'form': form}
        return render(request, ProfileView.template, context)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data['password']


class SignupView(View):
    template = 'users/signup.html'

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, SignupView.template, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['username'],
                                       first_name=form.cleaned_data['first_name'],
                                       last_name=form.cleaned_data['last_name'])

            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
        context = {'form': form}
        return render(request, SignupView.template, context)
