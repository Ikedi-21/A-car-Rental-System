from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list_view, name='car_list'),
    path('<int:car_id>/', views.car_detail_view, name='car_detail'),
]