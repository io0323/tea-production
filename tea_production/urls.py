from django.urls import path
from . import views

app_name = 'tea_production'

urlpatterns = [
    path('', views.index, name='index'),
    path('production/', views.production_list, name='production_list'),
    path('production/create/', views.production_create, name='production_create'),
    path('shipment/', views.shipment_list, name='shipment_list'),
    path('shipment/create/', views.shipment_create, name='shipment_create'),
    path('inventory/', views.inventory_list, name='inventory_list'),
] 