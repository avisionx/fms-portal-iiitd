from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import Complaint


class ComplaintForm(forms.Form):

    category = forms.IntegerField(
        label="Complaint Category",
        widget=forms.Select(
            choices=[('', "Select Category")] + Complaint.COMPLAINT_CATEGORIES),
        required=True
    )

    location = forms.IntegerField(
        label="Complaint Location",
        widget=forms.Select(
            choices=[('', "Select Location")] + Complaint.LOCATION_CHOICES),
        required=True
    )

    location_desc = forms.CharField(
        label="Location Details",
        max_length=100,
        widget=forms.Textarea(
            attrs={'placeholder': "Enter Complaint Location", 'rows': 3}),
        required=True
    )

    description = forms.CharField(
        label="Complaint Description",
        widget=forms.Textarea(
            attrs={'placeholder': "Enter Complaint Description", 'rows': 10}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2 mb-lg-3'
        self.helper.field_class = 'col-lg-10 mb-2 mb-lg-3'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'category',
                'location',
                'location_desc',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Register Complaint',
                       css_class="btn-success px-4 py-2 mt-1")
            )
        )

    def save(self, user):
        data = self.cleaned_data
        newComplaint = Complaint(
            customer=user.customer,
            category=data['category'],
            description=data['description'],
            location=data['location'],
            location_desc=data['location_desc']
        )
        newComplaint.save()
