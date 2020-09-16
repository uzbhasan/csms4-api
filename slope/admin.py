from django.contrib import admin
from slope.forms import (
    SlopeCreateUpdateAdminForm,
    OrderCreateUpdateAdminForm
)
from slope.models import (
    Slope, ExpertImage,
    DModel, Order, OrderImage
)


class SlopeAdmin(admin.ModelAdmin):
    """
    Setting admin panel for slopes
    """
    form = SlopeCreateUpdateAdminForm
    list_display = ('id', 'name', 'company', 'announced_at', 'deadline', 'is_inactive')
    list_filter = ('is_inactive', )
    list_display_links = ('name', )
    fieldsets = (
        (None, {'fields': ('name', 'is_inactive', 'created_at')}),
        ('Location', {'fields': ('lat', 'lng', 'address')}),
        ('Created by', {'fields': ('company',)}),
        ('Announcement', {'fields': ('announced_at', 'deadline')}),
    )
    readonly_fields = ('created_at', )
    search_fields = ('name', 'company', 'address')
    ordering = ('-created_at', 'name')
    filter_horizontal = ()


class OrderAdmin(admin.ModelAdmin):
    """
    Setting admin panel for orders
    """
    form = OrderCreateUpdateAdminForm
    list_display = ('id', 'slope', 'company', 'deadline', 'status', 'is_inactive')
    list_display_links = ('id', )
    list_filter = ('status', 'is_inactive')
    readonly_fields = ('ordered_at', 'modified_at')
    search_fields = ('slope', 'company')
    ordering = ('-ordered_at', )
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('slope', 'company', 'deadline', 'status', 'is_inactive', 'ordered_at', 'modified_at')}),
    )


admin.site.register(Slope, SlopeAdmin)
admin.site.register(ExpertImage)
admin.site.register(DModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderImage)
