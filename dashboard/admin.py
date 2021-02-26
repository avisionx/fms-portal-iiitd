from django.contrib import admin

from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):
    model = Complaint
    verbose_name_plural = 'Complaints'
    readonly_fields = ('created_at', 'updated_at', )


admin.site.register(Complaint, ComplaintAdmin)
