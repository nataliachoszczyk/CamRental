from django.contrib import admin
from .models import Category, Equipment, Rental

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_day', 'image')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'equipment', 'start_date', 'end_date', 'payment_method', 'total_days', 'total_price', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('user__username', 'equipment__name')

