from django.contrib import admin
from .models import Production, Shipment, Inventory

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('tea_type', 'production_date', 'quantity', 'quality_check', 'created_at')
    list_filter = ('tea_type', 'quality_check', 'production_date')
    search_fields = ('tea_type', 'quality_notes')
    ordering = ('-production_date',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('production', 'shipment_date', 'quantity', 'customer_name', 'created_at')
    list_filter = ('shipment_date', 'production__tea_type')
    search_fields = ('customer_name', 'customer_contact')
    ordering = ('-shipment_date',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('production', 'quantity', 'last_updated')
    list_filter = ('production__tea_type',)
    search_fields = ('production__tea_type',)
    ordering = ('-last_updated',) 