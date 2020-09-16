from django.urls import path
from account.api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns([
    # Account registration
    path('', views.AccountList.as_view(), name='account-cr'),
    path('<int:pk>', views.AccountDetail.as_view(), name='account-rud'),
    path('change/avatar/<int:pk>', views.AccountAvatarUpdate.as_view(), name='account-change-avatar'),
    path('change/password/<int:pk>', views.AccountPasswordChange.as_view(), name='account-change-password'),
    path('delete/<int:pk>', views.AccountForceDelete.as_view(), name='account-delete'),
    path('restore/<int:pk>', views.AccountRestore.as_view(), name='account-restore'),
])
