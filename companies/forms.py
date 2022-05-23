from django import forms
from django.db.models import Prefetch, Sum

from companies.models import Company
from rating.models import Rating


class NewCompanyForm(forms.ModelForm):
    logo = forms.ImageField(label='Логотип', required=False)
    photo1 = forms.ImageField(label='Фотография 1', required=False)
    photo2 = forms.ImageField(label='Фотография 2', required=False)
    photo3 = forms.ImageField(label='Фотография 3', required=False)

    class Meta:
        model = Company
        fields = ('name', 'description', 'industry')


class ChangeTrustPointsForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ('points', 'company', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        company_names = (
            Company.companies.filter(is_active=True)
            .select_related('industry').prefetch_related(
                Prefetch('rating', queryset=Rating.rating.all()))
            .annotate(sum_points=Sum('rating__points'))
            .order_by('industry__name', '-sum_points')
            .values_list('name', flat=True)
            .all()
        )
        for i in range(len(company_names)):
            name = company_names[i]
            field_name = f'points_{name}'
            self.fields[field_name] = forms.IntegerField(
                min_value=0, max_value=100, required=False,
                widget=forms.NumberInput(attrs={'id': i}))
            self.initial[field_name] = 0

    def get_points_fields(self):
        for field_name in self.fields:
            if field_name.startswith('points_'):
                yield self[field_name]
