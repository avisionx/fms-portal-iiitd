from authentication.views import CustomerSignUpView
# from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.urls import urlpatterns
from django.shortcuts import redirect
from django.urls import include, path

from .views import (HomeView, LoginRedirectView, LogoutView, MainOSAAPP,
                    PasswordResetView, SignUpView)

urlpatterns = [
    #     path('admin/', admin.site.urls),
    path('', HomeView, name='index'),
    path('login_redirects/', LoginRedirectView, name='login-redirects'),
    path('', include('dashboard.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #     path('accounts/signup/customer/',
    #          CustomerSignUpView, name='customer_signup'),
    #     path('password_reset/',
    #          auth_views.PasswordResetView.as_view(
    #              template_name='registration/password_reset_form.html',
    #              html_email_template_name="registration/html_password_reset_email.html",
    #              subject_template_name="registration/password_reset_subject.txt",
    #          ), name="password_reset"),
    path('accounts/signup/customer/',
         SignUpView, name='customer_signup'),
    path('password_reset/',
         PasswordResetView, name="password_reset"),
    path('main_osa_app/',
         MainOSAAPP, name="main_osa_app"),
    path('accounts/logout',
         LogoutView, name='logout')
]
