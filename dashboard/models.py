from datetime import datetime

from authentication.models import Customer
from django.core import serializers
from django.db import models
from django.urls import reverse


class ComplaintCategories(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ": " + str(self.name)


def GetComplaintCategoryList():
    return list(ComplaintCategories.objects.filter(
        active=True).values_list('id', 'name'))


class LocationChoices(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ": " + str(self.name)


def GetLocationChoicesList():
    return list(LocationChoices.objects.filter(
        active=True).values_list('id', 'name'))


def user_directory_path(instance, filename):
    return '{0}/uploads/{1}/{2}'.format(instance.customer.user.username, datetime.now().strftime("%Y/%m/%d"), filename)


class Complaint(models.Model):

    COMPLAINT_CATEGORIES = GetComplaintCategoryList()

    LOCATION_CHOICES = GetLocationChoicesList()

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
    rating = models.IntegerField(
        default=0
    )
    feedback = models.TextField(default="", blank=True)
    location_desc = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    media = models.FileField(null=True, upload_to=user_directory_path)

    def __str__(self):
        return "Complaint No: " + str(self.complaint_id)

    def csv(self):
        return {
            'Complaint ID': self.complaint_id,
            'First Name': self.customer.user.first_name,
            'Last Name': self.customer.user.last_name,
            'Email': self.customer.user.username,
            'Contact': self.customer.contact,
            'Category': [x[1] for x in self.COMPLAINT_CATEGORIES if x[0] == self.category][0],
            'Location': [x[1] for x in self.LOCATION_CHOICES if x[0] == self.location][0],
            'Location Description': self.location_desc,
            'Complaint Description': self.description,
            'Created': self.created_at.strftime("%I:%M %p, %d %b %Y"),
            'Last Updated': self.updated_at.strftime("%I:%M %p, %d %b %Y"),
            'Reminder': self.reminder.strftime("%I:%M %p, %d %b %Y") if self.reminder else '',
            'Rating': self.rating,
            'Feedback': self.feedback,
            'Status': "Active" if self.active else "Closed"
        }


class Notification(models.Model):
    msg = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.msg


def complaint_get_location(val):
    for a, b in Complaint.LOCATION_CHOICES:
        if a == val:
            return b
    return Complaint.LOCATION_CHOICES[0][1]


def complaint_get_category(val):
    for a, b in Complaint.COMPLAINT_CATEGORIES:
        if a == val:
            return b
    return Complaint.COMPLAINT_CATEGORIES[0][1]


def serialize(object):
    return serializers.serialize("json", object)
