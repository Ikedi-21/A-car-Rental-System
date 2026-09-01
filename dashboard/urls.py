from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),

    path('brands/', views.brand_list_view, name='admin_brand_list'),
    path('brands/add/', views.brand_form_view, name='admin_brand_add'),
    path('brands/<int:brand_id>/edit/', views.brand_form_view, name='admin_brand_edit'),
    path('brands/<int:brand_id>/delete/', views.brand_delete_view, name='admin_brand_delete'),

    path('cars/', views.car_list_admin_view, name='admin_car_list'),
    path('cars/add/', views.car_form_view, name='admin_car_add'),
    path('cars/<int:car_id>/edit/', views.car_form_view, name='admin_car_edit'),
    path('cars/<int:car_id>/delete/', views.car_delete_view, name='admin_car_delete'),

    path('bookings/', views.booking_list_admin_view, name='admin_booking_list'),
    path('bookings/<int:booking_id>/status/', views.booking_update_status_view, name='admin_booking_status'),

    path('testimonials/', views.testimonial_list_admin_view, name='admin_testimonial_list'),
    path('testimonials/<int:testimonial_id>/toggle/', views.testimonial_toggle_view, name='admin_testimonial_toggle'),

    path('queries/', views.query_list_admin_view, name='admin_query_list'),
    path('queries/<int:query_id>/resolve/', views.query_resolve_view, name='admin_query_resolve'),

    path('users/', views.user_list_admin_view, name='admin_user_list'),

    path('subscribers/', views.subscriber_list_admin_view, name='admin_subscriber_list'),
    path('subscribers/<int:subscriber_id>/delete/', views.subscriber_delete_view, name='admin_subscriber_delete'),

    path('content/', views.site_content_view, name='admin_site_content'),
    path('contact-details/', views.contact_details_view, name='admin_contact_details'),
    path('change-password/', views.admin_change_password_view, name='admin_change_password'),
]