from django.urls import path, re_path

from .views import Admin, Common, Customers

urlpatterns = [

    path('api-notification/', Common.notif_api, name="notif_api"),
    re_path(r'^api-complaint/(?P<slug>[\w-]+)/$', Common.complaint_api),

    path('dashboard/', Customers.dashboard, name='customer_dashboard'),
    path('track-complaint/', Customers.track_complaint,
         name='customer_track_complaint'),
    path('edit-profile/', Customers.edit_profile, name='customer_edit_profile'),
    path('submit-feedback/', Customers.submit_feedback, name="submit_feedback"),

    path('admin/dashboard', Admin.dashboard, name='admin_dashboard'),
    re_path(r'^admin/complaints/$', Admin.complaints, name='admin_complaints'),
    path('admin/fms-users/', Admin.fms_users, name='admin_fms_users'),
    path('admin/notifications/', Admin.notifications, name='admin_notifications'),
    path('admin/edit-profile/', Admin.edit_profile, name='admin_edit_profile'),
    path('complaint-action/', Admin.complaint_action, name='complaint_action'),
    path('notification-action/', Admin.notification_action,
         name='notification_action'),
    path('fms-user-action/', Admin.fms_user_action,
         name='fms_user_action'),
    re_path(r'^last-complaint/(?P<slug>[\w-]+)/$', Admin.last_complaint),

]
