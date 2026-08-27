from django.contrib import admin
from .models import ContactQuery, Subscriber, ContactDetails


@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']


@admin.register(ContactDetails)
class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']