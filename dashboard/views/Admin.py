from datetime import datetime

from authentication.decorators import fms_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.forms.widgets import TextInput
from django.http import JsonResponse
from django.shortcuts import render
from django_filters import (CharFilter, ChoiceFilter, DateTimeFilter,
                            FilterSet, OrderingFilter)

from ..models import Complaint, Notification


class ComplaintFilter(FilterSet):

    search = CharFilter(method='custom_search_filter', label='Search', widget=TextInput(
        attrs={'placeholder': 'Search by Complaint ID, Username, Email, Contact'}))

    category = ChoiceFilter(
        field_name='category', empty_label='All', choices=Complaint.COMPLAINT_CATEGORIES, label='Complaint Category')

    location = ChoiceFilter(field_name='location',
                            empty_label='All', choices=Complaint.LOCATION_CHOICES, label='Complaint Location')

    rating = ChoiceFilter(field_name='rating',
                          empty_label='Any', choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ), label='Rating')

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


@fms_required
def dashboard(request):

    context = {
        "dashboard_link": "active"
    }

    return render(request, 'admin/dashboard.html', context)


@fms_required
def complaints(request):

    filtered_complaints = ComplaintFilter(
        request.GET, queryset=Complaint.objects.all().order_by('-created_at')
    )

    paginator = Paginator(filtered_complaints.qs, 20)
    page = request.GET.get('page', 1)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)

    context = {
        "complaints_link": "active",
        'filter': filtered_complaints,
        'complaints': res
    }

    return render(request, 'admin/complaints.html', context)


@fms_required
def fms_users(request):

    context = {
        "fms_users_link": "active"
    }

    return render(request, 'admin/fms_users.html', context)


@fms_required
def notifications(request):

    qs = Notification.objects.all().order_by('created_at', '-active')

    context = {
        "notifications_link": "active",
        'notifications': qs
    }

    return render(request, 'admin/notifications.html', context)


@fms_required
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


@fms_required
def complaint_action(request):
    complaintId = request.POST['id']
    status = request.POST['status']
    complaint = Complaint.objects.get(complaint_id=complaintId)
    if int(status) == 1:
        complaint.active = True
    else:
        complaint.active = False
    complaint.save()
    return JsonResponse({"status": 200}, safe=False)
