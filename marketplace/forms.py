from django import forms

from marketplace.models import Shares


class SellSharesForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
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
    seller = forms.CharField(label='Продавец', max_length=255, disabled=True, required=False)
    company = forms.CharField(label='Компания', disabled=True, required=False)
    price = forms.FloatField(label='Цена за акцию', disabled=True, required=False)
    shares = forms.IntegerField(label='Акции', required=True, min_value=1)
