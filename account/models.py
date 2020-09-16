import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver
from company.models import Company
from account.managers import AccountManager


USER_ROLE_CHOICES = [
    ('SA', 'System administrator'),
    ('AD', 'Administrator'),
    ('GM', 'Company\'s general manager'),
    ('MA', 'Company\'s manager'),
    ('EM', 'Company\'s employee'),
]


class Account(AbstractBaseUser):
    """
    Custom user model
    """
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    # User role | SA - superuser (system admin), AD - staff, GM - company's general manager,
    # MA - company's manager, EM -company's employee:
    role = models.CharField(verbose_name='Role', max_length=40, choices=USER_ROLE_CHOICES)
    first_name = models.CharField(verbose_name='First name', max_length=150)
    last_name = models.CharField(verbose_name='Last name', max_length=150)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last login', blank=True, null=True, default=None)
    phone_number = models.CharField(
        verbose_name='Phone number', max_length=45, null=True, blank=True, default=None
    )
    avatar = models.ImageField(
        verbose_name='Avatar', upload_to='images/account/%Y/%m/%d/',
        blank=True, null=True, default=None, max_length=254
    )
    company = models.ForeignKey(
        to=Company, verbose_name='Company', on_delete=models.CASCADE,
        null=True, blank=True, default=None
    )

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """
        Does the user have access to the admin panel?
        """
        return self.role == 'AD' or self.role == 'SA'

    @property
    def is_admin(self):
        """
        Is the user a admin member?
        """
        return self.role == 'SA'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


@receiver(models.signals.post_delete, sender=Account)
def auto_delete_avatar_on_delete(sender, instance, **kwargs):
    """
    Deletes avatar from filesystem
    when corresponding `Account` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(models.signals.pre_save, sender=Account)
def auto_delete_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes old avatar from filesystem
    when corresponding `Account` object is updated
    with new avatar.
    """
    if not instance.pk:
        return False

    try:
        old_avatar = Account.objects.get(pk=instance.pk).avatar
    except Account.DoesNotExist:
        return False

    if not old_avatar:
        return False

    new_avatar = instance.avatar
    if not old_avatar == new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
