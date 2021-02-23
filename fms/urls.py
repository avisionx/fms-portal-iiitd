from django.contrib import admin
from django.urls import path, include
from authentication.views import StudentSignUpView
from django.contrib.auth import views as auth_views

from .views import StudentHomeView, LogoutView, HomeView


urlpatterns = [
    path('', HomeView, name='index'),
    path('admin/', admin.site.urls),
    path('student/', StudentHomeView, name='student_home'),
    path('track-complaint/', StudentHomeView, name='track_complaint'),
    path('register-complaint/', StudentHomeView, name='regsiter_complaint'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/student/',
          StudentSignUpView, name='student_signup'),
    path('password_reset/',
          auth_views.PasswordResetView.as_view(
               template_name='registration/password_reset_form.html',
               html_email_template_name="registration/html_password_reset_email.html",
               subject_template_name="registration/password_reset_subject.txt",
          ), name="password_reset"),
    path('accounts/logout',
         LogoutView, name='logout')
]
