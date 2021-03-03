from authentication.decorators import fms_required
from django.shortcuts import render
from django_filters import (CharFilter, FilterSet, NumberFilter,
                            OrderingFilter, TimeRangeFilter)

from ..models import Complaint


@fms_required
def dashboard(request):

    context = {
        "dashboard_link": "active"
    }

    return render(request, 'admin/dashboard.html', context)


class ComplaintFilter(FilterSet):

    o = OrderingFilter(
        choices=(
            ('rating', 'Rating Asc'),
            ('-rating', 'Rating Desc'),
            ('created_at', 'Created Oldest First'),
            ('-created_at', 'Created Latest First'),
            ('updated_at', 'Updated Oldest First'),
            ('-updated_at', 'Updated Lastest First'),
        )
    )

    customer__user__username = CharFilter(lookup_expr='contains')
    customer__contact = NumberFilter(lookup_expr='contains')
    complaint_id = NumberFilter(
        field_name='complaint_id', lookup_expr='contains')

    class Meta:
        model = Complaint
        fields = {
            'category': ['exact'],
            'location': ['exact'],
            'rating': ['gte'],
            'created_at': ['gte'],
            'updated_at': ['gte'],
            'active': ['exact']
        }


@fms_required
def complaints(request):

    f = ComplaintFilter(
        request.GET, queryset=Complaint.objects.all().order_by('-created_at'))

    context = {
        "complaints_link": "active",
        'filter': f
    }

    return render(request, 'admin/complaints.html', context)


@fms_required
def feedbacks(request):

    context = {
        "feedbacks_link": "active"
    }

    return render(request, 'admin/feedbacks.html', context)


@fms_required
def fms_users(request):

    context = {
        "fms_users_link": "active"
    }

    return render(request, 'admin/fms_users.html', context)


@fms_required
def notifications(request):

    context = {
        "notifications_link": "active"
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
