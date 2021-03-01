from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FMS, Customer, User


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = (
        'user',
        'contact'
    )


class FMSAdmin(admin.ModelAdmin):
    model = FMS
    list_display = (
        'user',
    )


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'first_name',
        'last_name',
        'email',
        'is_customer',
        'is_fms'
    )
    list_filter = (
        'is_customer',
        'is_fms'
    )


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FMS, FMSAdmin)
