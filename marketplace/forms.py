from django import forms

from marketplace.models import Shares
from users.models import CustomUser


class SellSharesForm(forms.Form):
    """
    Form of selling shares

    :param user: current user object
    """
    def __init__(self, user: CustomUser, *args, **kwargs):
        super(SellSharesForm, self).__init__(*args, **kwargs)
        self.fields['company'] = forms.ChoiceField(
            label='Компания',
            choices=[
                (company_name, company_name)
                for company_name in Shares.shares.get_user_companies(user)
            ],
            required=True,
        )

    company = forms.ChoiceField(required=True)
    shares = forms.IntegerField(label='Акции', required=True, min_value=1)
    price = forms.FloatField(label='Цена за акцию', required=True, min_value=0)


class BuySharesForm(forms.Form):
    """Form of shares purchase"""
    seller = forms.CharField(label='Продавец', max_length=255, disabled=True, required=False)
    company = forms.CharField(label='Компания', disabled=True, required=False)
    price = forms.FloatField(label='Цена за акцию', disabled=True, required=False)
    shares = forms.IntegerField(label='Акции', required=True, min_value=1)
