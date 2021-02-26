from authentication.models import Customer
from django.db import models
from django.urls import reverse


class Complaint(models.Model):

    COMPLAINT_CATEGORIES = [
        (1, 'Others'),
        (2, 'Electricity'),
        (3, 'House Keeping'),
    ]

    LOCATION_CHOICES = [
        (1, 'Others'),
        (2, 'Hostel'),
        (3, 'New Acad Block'),
        (4, 'Library'),
    ]

    complaint_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.IntegerField(
        choices=COMPLAINT_CATEGORIES,
        default=1
    )
    description = models.TextField(default="", blank=True)
    location = models.IntegerField(
        choices=LOCATION_CHOICES,
        default=1
    )
    location_desc = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Complaint No: " + str(self.complaint_id)
