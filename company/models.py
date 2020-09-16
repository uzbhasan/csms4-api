import os
from django.db import models
from django.dispatch import receiver


class Company(models.Model):
    """ Company model """
    email = models.EmailField(verbose_name='Email', max_length=254, unique=True)
    # type | False - Expert company, True - Engineer company:
    type = models.BooleanField(verbose_name='Is Engineer (default: Expert)')
    name = models.CharField(verbose_name='Name', max_length=254)
    phone_number = models.CharField(verbose_name='Phone', max_length=45)
    address = models.CharField(verbose_name='Address', max_length=254)
    about = models.TextField(verbose_name='About', max_length=500, blank=True, null=True, default=None)
    avatar = models.ImageField(
        verbose_name='Avatar', upload_to='images/company/%Y/%m/%d/',
        blank=True, null=True, default=None, max_length=254
    )
    # Inactive company: Company DB'dan o'chib ketmaydi, lekin
    # uning xodimlari uchun tizimga ruxsat yopiladi:
    is_inactive = models.BooleanField(verbose_name='Is inactive?', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


@receiver(models.signals.post_delete, sender=Company)
def auto_delete_avatar_on_delete(sender, instance, **kwargs):
    """
    Deletes avatar from filesystem
    when corresponding `Company` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(models.signals.pre_save, sender=Company)
def auto_delete_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes old avatar from filesystem
    when corresponding `Company` object is updated
    with new avatar.
    """
    if not instance.pk:
        return False

    try:
        old_avatar = Company.objects.get(pk=instance.pk).avatar
    except Company.DoesNotExist:
        return False

    if not old_avatar:
        return False

    new_avatar = instance.avatar
    if not old_avatar == new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
