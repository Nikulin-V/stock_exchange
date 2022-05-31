from django import forms

from companies.models import Company
from marketplace.models import Shares
from rating.models import Rating
from users.models import CustomUser


class NewCompanyForm(forms.ModelForm):
    logo = forms.ImageField(label='Логотип', required=False)
    photo1 = forms.ImageField(label='Фотография 1', required=False)
    photo2 = forms.ImageField(label='Фотография 2', required=False)
    photo3 = forms.ImageField(label='Фотография 3', required=False)

    class Meta:
        model = Company
        fields = ('name', 'description', 'industry')


class ChangeTrustPointsForm(forms.ModelForm):
    def __init__(self, user: CustomUser, *args, **kwargs):
        """
        Form of changing companies trust points

        :param user: current user object
        """
        super().__init__(*args, **kwargs)
        company_names = (
            Company.companies.get_sorted_companies_by_industry()
            .values_list('name', flat=True)
            .all()
        )
        user_rating = (
            Rating.rating.filter(user=user)
            .select_related('company')
            .values_list(
                'company__name',
                'points',
            )
            .all()
        )

        user_companies_names = Shares.shares.get_user_companies(user)
        for company_name in company_names:
            field_name = f'points_{company_name}'
            self.fields[field_name] = forms.IntegerField(
                min_value=0,
                max_value=100,
                required=False,
                disabled=True if company_name in user_companies_names else False,
                widget=forms.NumberInput(attrs={'id': company_name}),
            )
            init = list(filter(lambda x: company_name in x, user_rating))
            self.initial[field_name] = init[0][1] if init else 0

    class Meta:
        model = Rating
        exclude = ('points', 'company', 'user')

    def get_points_fields(self):
        """Returns form points fields"""
        for field_name in self.fields:
            if field_name.startswith('points_'):
                yield self[field_name]
