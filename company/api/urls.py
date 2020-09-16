from django.urls import path
from company.api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    # Get company list or create new:
    path('', views.CompanyList.as_view(), name='company-list'),
    path('<int:pk>', views.CompanyDetail.as_view(), name='company-detail')
])
