from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:car_id>/', views.create_booking_view, name='create_booking'),
    path('history/', views.booking_history_view, name='booking_history'),
]