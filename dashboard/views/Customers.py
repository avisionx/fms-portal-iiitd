from authentication.decorators import customer_required
from dashboard.forms import ComplaintForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import redirect, render


@customer_required
def dashboard(request):
    context = {"dashboard_link": "active"}
    return render(request, 'customer/dashboard.html', context)


@customer_required
def track_complaint(request):
    context = {"track_link": "active"}
    return render(request, 'customer/track_complaint.html', context)


@customer_required
def register_complaint(request):

    complaintForm = ComplaintForm(request.POST or None)

    context = {
        "register_link": "active",
        "complaintForm": complaintForm
    }

    if complaintForm.is_valid():
        complaintForm.save(request.user)
        messages.success(
            request, "Your complaint has been registerd!")
        return redirect('customer_track_complaint')

    return render(request, 'customer/register_complaint.html', context)


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
