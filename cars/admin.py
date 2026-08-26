from django.contrib import admin
from .models import Brand, Car


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # list_display controls what shows in the table view — picked the
    # fields that actually help distinguish one car from another at a
    # glance, rather than dumping every field into the list
    list_display = ['name', 'brand', 'category', 'price_per_day', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured', 'brand']
    search_fields = ['name', 'brand__name']