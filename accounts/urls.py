from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path('register/', views.register_view, name='register'),

     # Django's built-in LoginView/LogoutView — just pointed at our templates
     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),

     # Password reset — the 4-step flow. template_name for each must match
     # the templates we already built, and success_url chains one step
     # to the next.
     path('password-reset/',
          auth_views.PasswordResetView.as_view(
               template_name='accounts/password_reset.html',
               email_template_name='accounts/password_reset_email.txt',  # plain text email body sent to the user
               success_url='/accounts/password-reset/done/'
          ),
          name='password_reset'),

     path('password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
          name='password_reset_done'),

     path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
               template_name='accounts/password_reset_confirm.html',
               success_url='/accounts/password-reset-complete/'
          ),
          name='password_reset_confirm'),

     path('password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
          name='password_reset_complete'),
     
     path('profile/', views.profile_view, name='profile'),
     path('change-password/', views.change_password_view, name='change_password'),
]