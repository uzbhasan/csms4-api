from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.models import Account


class AccountCreationAdminForm(forms.ModelForm):
    """
    A form for creating new users by admin panel. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'role', 'first_name', 'last_name', 'company')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean(self):
        """
        Administratorlar uchun company tanlanmaganligini va aksincha,
        company members uchun company tanlanganini tekshirish
        """
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        role = cleaned_data.get('role')

        if role in ['SA', 'AD'] and company is not None:
            self.add_error('company', 'Administrators should not have any kind of company')
            self.add_error('role', 'Administrators should not have any kind of company')

        if role in ['GM', 'MA', 'EM'] and company is None:
            self.add_error('company', 'Company members must have a company')
            self.add_error('role', 'Company members must have a company')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeAdminForm(forms.ModelForm):
    """
    A form for updating accounts by admin panel. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = (
            'email', 'password', 'role', 'first_name', 'last_name',
            'is_active', 'phone_number', 'avatar', 'company'
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean(self):
        """
        Administratorlar uchun company tanlanmaganligini va aksincha,
        company members uchun company tanlanganini tekshirish
        """
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        role = cleaned_data.get('role')

        if role in ['SA', 'AD'] and company is not None:
            self.add_error('company', 'Administrators should not have any kind of company')
            self.add_error('role', 'Administrators should not have any kind of company')

        if role in ['GM', 'MA', 'EM'] and company is None:
            self.add_error('company', 'Company members must have a company')
            self.add_error('role', 'Company members must have a company')
