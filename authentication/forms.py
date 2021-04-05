from crispy_forms.helper import FormHelper
from crispy_forms.layout import (ButtonHolder, Div, Fieldset, Layout, Row,
                                 Submit)
from django import forms
from django.conf import settings

from authentication.models import User

from .models import FMS


class FMSUserForm(forms.Form):

    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': "First Name"}),
        required=True
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': "Last Name"}),
        required=True
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={'placeholder': "Enter Email Address"}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'mb-0'
        self.helper.field_class = 'mb-2 mb-lg-3'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Div('first_name', css_class="col-md-6"),
                    Div('last_name', css_class="col-md-6"),
                    css_class="row"
                ),
                'email'
            ),
            ButtonHolder(
                Submit('submit', 'Create User',
                       css_class="btn-success px-4 py-2")
            )
        )

    def save(self):
        data = self.cleaned_data
        username = data["email"]
        password = settings.ADMIN_PASSWORD
        first_name = data["first_name"]
        last_name = data["last_name"]

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=username,
                first_name=first_name,
                last_name=last_name
            )
            user.is_fms = True
            user.save()
            fms = FMS.objects.create(user=user)
            fms.save()
        except Exception as inst:
            return inst
        return None
