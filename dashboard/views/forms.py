from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models import Complaint 


class ComplaintForm(forms.ModelForm):


    class Meta: 
        model = Complaint 
        fields = "__all__"

