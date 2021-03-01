from django.urls import path, re_path

from .views import Customers

urlpatterns = [
    path('dashboard/', Customers.dashboard, name='customer_dashboard'),
    path('track-complaint/', Customers.track_complaint,
         name='customer_track_complaint'),
    path('edit-profile/', Customers.edit_profile, name='customer_edit_profile'),
    path('api-notification/', Customers.notif_api, name="notif_api")
]
