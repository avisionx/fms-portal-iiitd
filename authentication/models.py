import json

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    username_osa = models.CharField(max_length=150, unique=True)
    is_customer = models.BooleanField(default=False)
    is_fms = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Customer(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    contact = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return str(self.user.username)


class FMS(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = 'FMS'
        verbose_name_plural = 'FMS'

    def __str__(self):
        return str(self.user.username)
