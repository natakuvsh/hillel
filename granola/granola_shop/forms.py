from django import forms
from django.contrib.auth import get_user_model
from granola_shop.models import Product, OrderProduct, CheckoutAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return password_confirm

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class ContactForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CheckoutForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100', 'onchange': ''}))

    class Meta:
        model = CheckoutAddress
        exclude = ('user', 'last_name', 'first_name')
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': 'Ivana Franko str 10'}),
            'apartment_address': forms.TextInput(attrs={'required': False, 'placeholder': 'Apartment 10'}),
            'zip': forms.TextInput(),

        }

        def __init__(self, *args, **kwargs):
            super(CheckoutForm, self).__init__(*args, **kwargs)
            self.fields['user'].required = False
