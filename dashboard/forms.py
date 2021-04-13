from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from dashboard.models import ComplaintCategories, LocationChoices

from .models import (Complaint, ComplaintCategories, LocationChoices,
                     Notification)


class ComplaintForm(forms.Form):

    category = forms.ModelChoiceField(
        label="Complaint Category",
        empty_label="Select Category",
        queryset=ComplaintCategories.objects.filter(active=True),
        required=True
    )

    location = forms.ModelChoiceField(
        empty_label="Select Location",
        label="Complaint Location",
        queryset=LocationChoices.objects.filter(active=True),
        required=True
    )

    location_desc = forms.CharField(
        label="Location Details",
        max_length=100,
        widget=forms.Textarea(
            attrs={'placeholder': "Enter Complaint Location", 'rows': 3}),
        required=True
    )

    complaint_media = forms.FileField(
        label="Complaint Image", required=False, widget=forms.FileInput(attrs={'accept': "image/*", 'id': 'complaint_media'}))

    description = forms.CharField(
        label="Complaint Description",
        widget=forms.Textarea(
            attrs={'placeholder': "Enter Complaint Description", 'rows': 10}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'mb-0 mb-lg-1'
        self.helper.field_class = 'mb-2 mb-lg-3'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'category',
                'location',
                'location_desc',
                'description',
                'complaint_media',
            ),
            ButtonHolder(
                Submit('submit', 'Register Complaint',
                       css_class="btn-success px-4 py-2 mt-1")
            )
        )

    def save(self, user, files):
        data = self.cleaned_data
        media = None
        if files:
            media = files['complaint_media']
        newComplaint = Complaint(
            customer=user.customer,
            category=data['category'],
            description=data['description'],
            location=data['location'],
            location_desc=data['location_desc'],
            media=media
        )
        newComplaint.save()


class NotificationForm(forms.Form):

    active = forms.BooleanField(
        label="Notification Active",
        initial=True,
        required=False
    )

    msg = forms.CharField(
        label="Notification Message",
        widget=forms.Textarea(
            attrs={'placeholder': "Enter New Notification Message...", 'rows': 5, 'class': "mb-2"}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'mb-0'
        self.helper.field_class = 'mb-0'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'msg',
                'active'
            ),
            ButtonHolder(
                Submit('submit', 'Create Notification',
                       css_class="btn-success px-4 py-2")
            )
        )

    def save(self):
        data = self.cleaned_data
        newNotificaion = Notification(
            msg=data['msg'],
            active=data['active'],
        )
        newNotificaion.save()


class ComplaintCategoriesForm(forms.Form):

    active = forms.BooleanField(
        label="Category Active",
        initial=True,
        required=False
    )

    name = forms.CharField(
        label="Category Name",
        widget=forms.TextInput(
            attrs={'placeholder': "Category Name...",  'class': "mb-2", 'maxlength': '50'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'mb-0'
        self.helper.field_class = 'mb-0'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'active'
            ),
            ButtonHolder(
                Submit('submit', 'Create Complaint Category',
                       css_class="btn-success px-4 py-2")
            )
        )

    def save(self):
        data = self.cleaned_data
        newComplaintCategory = ComplaintCategories(
            name=data['name'],
            active=data['active'],
        )
        newComplaintCategory.save()


class LocationChoicesForm(forms.Form):

    active1 = forms.BooleanField(
        label="Location Active",
        initial=True,
        required=False
    )

    name1 = forms.CharField(
        label="Location Name",
        widget=forms.TextInput(
            attrs={'placeholder': "Location Name...",  'class': "mb-2", 'maxlength': '50'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'mb-0'
        self.helper.field_class = 'mb-0'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name1',
                'active1'
            ),
            ButtonHolder(
                Submit('submit', 'Create Location Choice',
                       css_class="btn-success px-4 py-2")
            )
        )

    def save(self):
        data = self.cleaned_data
        newLocationChoice = LocationChoices(
            name=data['name1'],
            active=data['active1'],
        )
        newLocationChoice.save()
