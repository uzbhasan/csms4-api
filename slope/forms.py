from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from company.models import Company
from slope.models import Slope, Order


class SlopeCreateUpdateAdminForm(forms.ModelForm):
    """
    A form for creating/updating new slope by admin panel.
    """
    company = forms.ModelChoiceField(queryset=Company.objects.all().filter(is_inactive=False, type=False))

    class Meta:
        model = Slope
        fields = ('name', 'lat', 'lng', 'address', 'announced_at', 'deadline', 'company')

    def clean_company(self):
        company = self.cleaned_data.get('company')

        if not company:
            raise ValidationError('Slope must have a company')

        if company and company.type:
            raise ValidationError('The company must be an expert')

        return company

    def clean(self):
        # "Announced at" hamda "deadline" maydonlarining
        # qiymatlaridagi bog'liqlikning mosligini tekshirish
        cleaned_data = super().clean()
        announced_at = cleaned_data.get('announced_at')
        deadline = cleaned_data.get('deadline')

        if announced_at and deadline is None:
            self.add_error('deadline', 'Announced slopes must have a deadline')

        if announced_at is None and deadline:
            self.add_error('deadline', 'Unannounced slopes should not have a deadline')

        if announced_at and deadline and announced_at > deadline:
            self.add_error('deadline', 'The deadline of the order may not be less than the date of announce')


class OrderCreateUpdateAdminForm(forms.ModelForm):
    """
    A form for creating/updating new order by admin panel.
    """
    company = forms.ModelChoiceField(queryset=Company.objects.all().filter(is_inactive=False, type=True))

    class Meta:
        model = Order
        fields = ('slope', 'company', 'deadline')

    def clean_company(self):
        company = self.cleaned_data.get('company')

        if not company:
            raise ValidationError('Slope must have a company')

        if company and not company.type:
            raise ValidationError('The company must be an engineer')

        return company

    def clean(self):
        # "Announced at" hamda "deadline" maydonlarining
        # qiymatlaridagi bog'liqlikning mosligini tekshirish
        cleaned_data = super().clean()
        now = timezone.now()
        deadline = cleaned_data.get('deadline')

        if deadline and now > deadline:
            self.add_error(
                'deadline',
                f'The deadline of the order may not be less than the current time (current time: { now })'
            )
