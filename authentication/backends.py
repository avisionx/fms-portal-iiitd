import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from .models import FMS, Customer, User


class OSAAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        r = requests.post(settings.AUTHENTICATION_OSA_URL,
                          data={'username': username, 'password': password})
        if r.status_code == 200:
            userData = r.json()['user']
            username_osa = userData['username_osa']
            username_retreived = userData['username']
            first_name = userData['first_name']
            last_name = userData['last_name']
            try:
                user = User.objects.get(username_osa=username_osa)
                user.first_name = first_name
                user.last_name = last_name
                user.last_name = last_name
                user.email = username_retreived
                user.username = username_retreived
                user.save()
            except User.DoesNotExist:
                user = User.objects.create(
                    username=username_retreived,
                    username_osa=username_osa,
                    password=password,
                    email=username_retreived,
                    first_name=first_name,
                    last_name=last_name,
                    is_customer=True,
                )
                Customer.objects.create(user=user)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FMSAdminBackend(BaseBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN
    ADMIN_PASSWORD
    """

    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = (password == settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, is_fms=True,
                            first_name="FMS", last_name="Admin", email=username, is_superuser=True)
                user.set_password(password)
                user.save()
                fms = FMS(user=user)
                fms.save()
            return user
        try:
            user = User.objects.get(username=username)
            if (user.is_fms and user.check_password(password)):
                return user
        except:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
