from django.contrib import admin

from .models import Complaint, Notification


class ComplaintAdmin(admin.ModelAdmin):
    model = Complaint
    verbose_name_plural = 'Complaints'
    list_display = (
        'complaint_id',
        'customer',
        'category',
        'location',
        'created_at',
        'active'
    )
    list_filter = (
        'active',
    )
    readonly_fields = ('created_at', 'updated_at', )


class NotifAdmin(admin.ModelAdmin):
    model = Notification
    verbose_name_plural = 'Notifications'
    list_display = (
        'msg',
        'created_at',
        'active'
    )
    list_filter = (
        'active',
    )


admin.site.register(Notification, NotifAdmin)
admin.site.register(Complaint, ComplaintAdmin)
