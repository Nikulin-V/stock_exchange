from django.contrib.auth import get_user_model
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

User = get_user_model()


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
