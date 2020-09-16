import os
from django.db import models
from django.dispatch import receiver

from company.models import Company


class Slope(models.Model):
    """
    Slope table model
    """
    name = models.CharField(verbose_name='Name', max_length=254)
    lat = models.DecimalField(verbose_name='Latitude', max_digits=10, decimal_places=8)
    lng = models.DecimalField(verbose_name='Longitude', max_digits=11, decimal_places=8)
    address = models.CharField(verbose_name='Address', max_length=254)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    is_inactive = models.BooleanField(verbose_name='Is inactive', default=False)
    announced_at = models.DateTimeField(
        verbose_name='Announced at', blank=True, null=True, default=None
    )
    deadline = models.DateTimeField(
        verbose_name='Deadline for order fulfilment', blank=True, null=True, default=None
    )
    # The expert company that created this slope
    company = models.ForeignKey(
        to=Company, verbose_name='Company', on_delete=models.CASCADE
    )
    orders = models.ManyToManyField(
        to=Company, through='Order', related_name='orders', through_fields=('slope', 'company')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Slope'
        verbose_name_plural = 'Slopes'


class ExpertImage(models.Model):
    """
    Expert company' images
    """
    image = models.ImageField(
        verbose_name='Image', upload_to='images/slope/expert/%Y/%m/%d/', max_length=254
    )
    uploaded_at = models.DateTimeField(verbose_name='Uploaded at', auto_now_add=True)
    is_inactive = models.BooleanField(verbose_name='Is inactive', default=False)
    slope = models.ForeignKey(to=Slope, verbose_name='Slope', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Expert image'
        verbose_name_plural = 'Expert images'

    def __str__(self):
        return os.path.basename(self.image.name)


class DModel(models.Model):
    """
    Generated 3D models
    """
    file = models.FileField(
        verbose_name='3D model', upload_to='files/models/%Y/%m/%d/', max_length=254
    )
    generated_at = models.DateTimeField(verbose_name='Generated at', auto_now_add=True)
    is_inactive = models.BooleanField(verbose_name='Is inactive', default=False)
    slope = models.ForeignKey(to=Slope, verbose_name='Slope', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '3D model'
        verbose_name_plural = '3D models'

    def __str__(self):
        return os.path.basename(self.file.name)


class Order(models.Model):
    """
    Orders
    """
    slope = models.ForeignKey(to=Slope, verbose_name='Slope', on_delete=models.CASCADE)
    company = models.ForeignKey(to=Company, verbose_name='Company', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Is open', default=True)
    deadline = models.DateTimeField(verbose_name='Deadline')
    ordered_at = models.DateTimeField(verbose_name='Ordered at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)
    is_inactive = models.BooleanField(verbose_name='Is inactive', default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        unique_together = ['slope', 'company']

    def __str__(self):
        return f'{self.slope.company} || {self.company}'


class OrderImage(models.Model):
    """
    Images uploaded by engineer
    """
    image = models.ImageField(
        verbose_name='Image', upload_to='images/slope/engineer/%Y/%m/%d/', max_length=254
    )
    uploaded_at = models.DateTimeField(verbose_name='Uploaded at', auto_now_add=True)
    is_inactive = models.BooleanField(verbose_name='Is inactive', default=False)
    order = models.ForeignKey(to=Order, verbose_name='Order', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Order image'
        verbose_name_plural = 'Order images'

    def __str__(self):
        return os.path.basename(self.image.name)


def auto_delete_file_on_instance_delete(instance, field_name='image'):
    """
    Deletes file from filesystem
    when corresponding instance object is deleted.
    """
    field = getattr(instance, field_name)
    if field:
        if os.path.isfile(field.path):
            os.remove(field.path)


def auto_delete_file_on_instance_change(model, field_name, instance):
    """
    Deletes old file from filesystem
    when corresponding instance object is updated
    with new image.
    """
    if not instance.pk:
        return False

    try:
        obj = model.objects.get(pk=instance.pk)
        old_file = getattr(obj, field_name)
    except model.DoesNotExist:
        return False

    if not old_file:
        return False

    new_file = getattr(instance, field_name)
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    return True


@receiver(models.signals.post_delete, sender=ExpertImage)
def auto_delete_expert_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `ExpertImage` object is deleted.
    """
    auto_delete_file_on_instance_delete(instance)


@receiver(models.signals.pre_save, sender=ExpertImage)
def auto_delete_expert_image_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `ExpertImage` object is updated
    with new image.
    """
    return auto_delete_file_on_instance_change(ExpertImage, 'image', instance)


@receiver(models.signals.post_delete, sender=DModel)
def auto_delete_d_model_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `DModel` object is deleted.
    """
    auto_delete_file_on_instance_delete(instance, 'file')


@receiver(models.signals.pre_save, sender=DModel)
def auto_delete_d_model_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `DModel` object is updated
    with new file.
    """
    return auto_delete_file_on_instance_change(DModel, 'file', instance)


@receiver(models.signals.post_delete, sender=OrderImage)
def auto_delete_order_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `OrderImage` object is deleted.
    """
    auto_delete_file_on_instance_delete(instance)


@receiver(models.signals.pre_save, sender=OrderImage)
def auto_delete_order_image_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `OrderImage` object is updated
    with new image.
    """
    return auto_delete_file_on_instance_change(OrderImage, 'image', instance)
