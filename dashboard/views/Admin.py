from authentication.decorators import fms_required
from django.shortcuts import render


@fms_required
def dashboard(request):

    context = {
        "dashboard_link": "active"
    }

    return render(request, 'admin/dashboard.html', context)


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
