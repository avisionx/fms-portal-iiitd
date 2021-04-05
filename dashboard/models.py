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

    def __str__(self):
        return "Complaint No: " + str(self.complaint_id)


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
