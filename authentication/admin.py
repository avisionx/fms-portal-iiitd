from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FMS, Customer, User


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    verbose_name_plural = 'Customers'


class FMSAdmin(admin.ModelAdmin):
    model = FMS
    verbose_name_plural = 'FMS'


class UserAdmin(admin.ModelAdmin):
    model = User
    verbose_name_plural = 'Users'


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FMS, FMSAdmin)
