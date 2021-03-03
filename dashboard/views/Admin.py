from datetime import datetime

from authentication.decorators import fms_required
from django.db.models import Q
from django.forms.widgets import TextInput
from django.shortcuts import render
from django_filters import (CharFilter, ChoiceFilter, DateTimeFilter,
                            FilterSet, OrderingFilter)

from ..models import Complaint


@fms_required
def dashboard(request):

    context = {
        "dashboard_link": "active"
    }

    return render(request, 'admin/dashboard.html', context)


class ComplaintFilter(FilterSet):

    search = CharFilter(method='custom_search_filter', label='Search', widget=TextInput(
        attrs={'placeholder': 'Search by Complaint ID, Username, Email, Contact'}))

    category = ChoiceFilter(
        field_name='category', empty_label='All', choices=Complaint.COMPLAINT_CATEGORIES, label='Complaint Category')

    location = ChoiceFilter(field_name='location',
                            empty_label='All', choices=Complaint.LOCATION_CHOICES, label='Complaint Location')

    created_at = DateTimeFilter(
        field_name='created_at',
        label='Created On/After',
        lookup_expr='gte',
        widget=TextInput(attrs={
                         'type': 'date', 'placeholder': 'DD-MM-YYYY', 'max': datetime.now().date()})
    )

    active = ChoiceFilter(field_name='active', label='Status',
                          empty_label='All', choices=((True, 'Active'), (False, 'Closed')))

    createdSort = OrderingFilter(
        choices=(
            ('created_at', 'Old to New'),
        ), label='Sort By Created', empty_label='New to Old'
    )

    def custom_search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(customer__user__username__contains=value) | Q(
                customer__contact__contains=value) | Q(complaint_id__contains=value) | Q(customer__user__first_name__contains=value) | Q(customer__user__last_name__contains=value)
        )


@ fms_required
def complaints(request):

    f = ComplaintFilter(
        request.GET, queryset=Complaint.objects.all().order_by('-created_at')
    )

    context = {
        "complaints_link": "active",
        'filter': f
    }

    return render(request, 'admin/complaints.html', context)


@ fms_required
def feedbacks(request):

    context = {
        "feedbacks_link": "active"
    }

    return render(request, 'admin/feedbacks.html', context)


@ fms_required
def fms_users(request):

    context = {
        "fms_users_link": "active"
    }

    return render(request, 'admin/fms_users.html', context)


@ fms_required
def notifications(request):

    context = {
        "notifications_link": "active"
    }

    return render(request, 'admin/notifications.html', context)


@ fms_required
def edit_profile(request):
    msg = {
        "save": False
    }

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        request.user.customer.save()
        msg["save"] = True

    formData = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, "admin/edit_profile.html", {'msg': msg, 'formData': formData})
