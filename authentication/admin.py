from django.contrib.auth.models import Group
from django.contrib import admin

from .models import FMS, Student, User


class StudentAdmin(admin.ModelAdmin):
    model = Student
    verbose_name_plural = 'Students'


class FMSAdmin(admin.ModelAdmin):
    model = FMS
    verbose_name_plural = 'FMS'


class UserAdmin(admin.ModelAdmin):
    model = User
    verbose_name_plural = 'Users'


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(FMS, FMSAdmin)
