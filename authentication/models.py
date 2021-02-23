import json

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_fms = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    contact = models.IntegerField()

    def __str__(self):
        return 'Student: ' + str(self.user.username)


class FMS(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'FMS: ' + str(self.user.username)
