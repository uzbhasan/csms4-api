from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.forms import AccountCreationAdminForm, AccountChangeAdminForm
from account.models import Account


class AccountAdmin(BaseUserAdmin):
    """
    Custom User Admin
    """
    # The forms to add and change account instances
    form = AccountChangeAdminForm
    add_form = AccountCreationAdminForm

    # The fields to be used in displaying the Account model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar')}),
        ('Company', {'fields': ('company', )}),
        ('Permissions', {'fields': ('role', 'is_active')}),
        ('Actions', {'fields': ('date_joined', 'last_login')}),
    )
    readonly_fields = ('date_joined', 'last_login')

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'company', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'role')
    filter_horizontal = ()


# Now register the new AccountAdmin...
admin.site.register(Account, AccountAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
