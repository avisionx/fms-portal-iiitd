import json
from datetime import datetime

from authentication.decorators import customer_required
from dashboard.forms import ComplaintForm
from dashboard.models import (Complaint, complaint_get_category,
                              complaint_get_location, serialize)
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_datetime


@customer_required
def dashboard(request):
    complaintForm = ComplaintForm(request.POST or None)

    userComplaints = Complaint.objects.filter(
        customer=request.user.customer).order_by('-created_at')[:3]

    complaints = []
    complaintsData = json.loads(serialize(userComplaints))

    for complaint in complaintsData:
        created_at = parse_datetime(
            complaint['fields']['created_at']).strftime("%I:%M %p, %d %b %Y")
        temp = {
            'id': complaint['pk'],
            'location': complaint_get_location(complaint['fields']['location']),
            'category': complaint_get_category(complaint['fields']['category']),
            'desc': complaint['fields']['description'],
            'created_at': created_at,
            'active': complaint['fields']['active']
        }
        complaints.append(temp)

    context = {
        "dashboard_link": "active",
        "complaintForm": complaintForm,
        "complaints": complaints
    }

    if complaintForm.is_valid():
        complaintForm.save(request.user)
        messages.success(
            request, "Your complaint has been registerd!")
        return redirect('customer_dashboard')

    return render(request, 'customer/dashboard.html', context)


@customer_required
def track_complaint(request):
    context = {"track_link": "active"}
    return render(request, 'customer/track_complaint.html', context)


@customer_required
def edit_profile(request):
    msg = {
        "save": False
    }

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        contact = request.POST["contact"]
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        request.user.customer.contact = contact
        request.user.customer.save()
        msg["save"] = True

    formData = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'contact': request.user.customer.contact
    }

    return render(request, "customer/edit_profile.html", {'msg': msg, 'formData': formData})
