from django.urls import path
from slope.api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns([
    # Account registration
    path('', views.SlopeList.as_view(), name='slope-cr'),
    path('<int:pk>', views.SlopeDetail.as_view(), name='slope-rud'),
    path('delete/<int:pk>', views.SlopeForceDelete.as_view(), name='slope-delete'),
    path('expert-image/', views.ExpertImageList.as_view(), name='expert-image-cr'),
    path('expert-image/<int:pk>', views.ExpertImageDetail.as_view(), name='expert-image-rud'),
    path('expert-image/delete/<int:pk>', views.ExpertImageForceDelete.as_view(), name='expert-image-delete'),
    path('model/', views.DModelList.as_view(), name='model-cr'),
    path('model/<int:pk>', views.DModelDetail.as_view(), name='model-rud'),
    path('model/delete/<int:pk>', views.DModelForceDelete.as_view(), name='model-delete'),
    path('order/', views.OrderList.as_view(), name='order-cr'),
    path('order/<int:pk>', views.OrderDetail.as_view(), name='order-rud'),
    path('order/delete/<int:pk>', views.OrderForceDelete.as_view(), name='order-delete'),
    path('order-image/', views.OrderImageList.as_view(), name='order-image-cr'),
    path('order-image/<int:pk>', views.OrderImageDetail.as_view(), name='order-image-rud'),
    path('order-image/delete/<int:pk>', views.OrderImageForceDelete.as_view(), name='order-image-delete'),
])
