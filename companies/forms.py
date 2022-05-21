from django import forms
from companies.models import Company


class NewCompanyForm(forms.ModelForm):
    logo = forms.ImageField(label='Логотип', required=False)
    photo1 = forms.ImageField(label='Фотография 1', required=False)
    photo2 = forms.ImageField(label='Фотография 2', required=False)
    photo3 = forms.ImageField(label='Фотография 3', required=False)

    class Meta:
        model = Company
        fields = 'name', 'description', 'industry'
