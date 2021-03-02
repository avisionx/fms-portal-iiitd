from django.urls import path, re_path

from .views import Admin, Common, Customers

urlpatterns = [

    path('api-notification/', Common.notif_api, name="notif_api"),

    path('dashboard/', Customers.dashboard, name='customer_dashboard'),
    path('track-complaint/', Customers.track_complaint,
         name='customer_track_complaint'),
    path('edit-profile/', Customers.edit_profile, name='customer_edit_profile'),
    re_path(r'^api-complaint/(?P<slug>[\w-]+)/$', Customers.complaint_api),
    path('submit-feedback/', Customers.submit_feedback, name="submit_feedback"),

    path('admin/dashboard', Admin.dashboard, name='admin_dashboard'),
    path('admin/edit-profile/', Admin.edit_profile, name='admin_edit_profile'),

]
