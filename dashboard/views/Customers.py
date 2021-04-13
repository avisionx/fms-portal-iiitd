import json

from authentication.decorators import customer_required
from dashboard.forms import ComplaintForm
from dashboard.models import (Complaint, ComplaintCategories, LocationChoices,
                              serialize)
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import utc


@customer_required
def dashboard(request):
    complaintForm = ComplaintForm(request.POST or None)

    userComplaints = Complaint.objects.filter(
        customer=request.user.customer).order_by('-created_at')[:3]

    complaints = []
    complaintsData = json.loads(serialize(userComplaints))

    for complaint in complaintsData:
        complaints.append(extractComplaintObj(complaint))

    context = {
        "dashboard_link": "active",
        "complaintForm": complaintForm,
        "complaints": complaints
    }

    if complaintForm.is_valid():
        complaintForm.save(request.user, request.FILES)
        messages.success(
            request, "Your complaint has been registerd!")
        return redirect('customer_dashboard')

    return render(request, 'customer/dashboard.html', context)


@customer_required
def track_complaint(request):

    userComplaints = Complaint.objects.filter(
        customer=request.user.customer).order_by('-created_at')

    complaints = []
    complaintsData = json.loads(serialize(userComplaints))

    for complaint in complaintsData:
        complaints.append(extractComplaintObj(complaint))

    context = {
        "track_link": "active",
        "complaints": complaints
    }

    return render(request, 'customer/track_complaint.html', context)


@customer_required
def edit_profile(request):
    msg = {
        "save": False
    }

    if request.method == "POST":
        contact = request.POST["contact"]
        request.user.customer.contact = contact
        request.user.customer.save()
        msg["save"] = True

    if not request.user.customer.contact:
        contact = ''
    else:
        contact = request.user.customer.contact

    formData = {
        'contact': contact
    }

    return render(request, "customer/edit_profile.html", {'msg': msg, 'formData': formData, 'osa_main_app': settings.OSA_APP_URL, })


@customer_required
def submit_feedback(request):
    stars = request.POST['stars']
    feedbackDesc = request.POST['feedbackDesc']
    complaintId = request.POST['complaintId']
    complaint = Complaint.objects.get(complaint_id=complaintId)
    complaint.rating = stars
    complaint.feedback = feedbackDesc
    complaint.save()
    return JsonResponse({"status": 200}, safe=False)


def extractComplaintObj(complaint):
    created_at = parse_datetime(
        complaint['fields']['created_at']).strftime("%I:%M %p, %d %b %Y")
    if complaint['fields']['reminder']:
        reminder = parse_datetime(
            complaint['fields']['reminder']).strftime("%I:%M %p, %d %b %Y")
    else:
        reminder = None
    try:
        location = str(LocationChoices.objects.get(
            pk=complaint['fields']['location']))
    except LocationChoices.DoesNotExist:
        location = 'Location'
    try:
        category = str(ComplaintCategories.objects.get(
            pk=complaint['fields']['category']))
    except ComplaintCategories.DoesNotExist:
        category = 'Category'
    temp = {
        'id': complaint['pk'],
        'location': location,
        'category': category,
        'desc': complaint['fields']['description'],
        'location_desc': complaint['fields']['location_desc'],
        'created_at': created_at,
        'active': complaint['fields']['active'],
        'rating': complaint['fields']['rating'],
        'feedback': complaint['fields']['feedback'],
        'reminder':  reminder,
        'media': complaint['fields']['media']
    }
    return temp
