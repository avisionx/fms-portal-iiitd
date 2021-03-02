from authentication.views import CustomerSignUpView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import HomeView, LoginRedirectView, LogoutView

urlpatterns = [
    path('', HomeView, name='index'),
    path('login_redirects/', LoginRedirectView, name='login-redirects'),
    path('', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/customer/',
         CustomerSignUpView, name='customer_signup'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             html_email_template_name="registration/html_password_reset_email.html",
             subject_template_name="registration/password_reset_subject.txt",
         ), name="password_reset"),
    path('accounts/logout',
         LogoutView, name='logout')
]
