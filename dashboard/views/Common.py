
import json
from datetime import datetime

from dashboard.models import Complaint, Notification, serialize
from dashboard.views.Customers import extractComplaintObj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect


@login_required
def notif_api(request):
    if request.is_ajax():
        now = datetime.now()
        qs = Notification.objects.filter(active=True).values(
            'msg', 'created_at').order_by('-created_at')

        for q in qs:
            timediff = now - q['created_at']
            q['created_at'] = get_days(timediff.total_seconds())

        return JsonResponse({"data": list(qs)}, safe=False)
    else:
        return redirect("customer_dashboard")


@login_required
def complaint_api(request, slug):
    if request.is_ajax():
        try:
            complaint = Complaint.objects.get(complaint_id=slug)
        except:
            return JsonResponse({"status": 404}, safe=False)

        customer_info = {'name': complaint.customer.user.first_name + " " + complaint.customer.user.last_name,
                         'email': complaint.customer.user.email,
                         'contact': complaint.customer.contact}

        complaint = json.loads(serialize([complaint]))[0]
        return JsonResponse({"status": 200, "data": {**extractComplaintObj(complaint), **customer_info}}, safe=False)
    else:
        return redirect("login-redirects")


def get_days(ttime):
    day = ttime // (24 * 3600)
    ttime = ttime % (24 * 3600)
    hour = ttime // 3600
    if day:
        return ("%d days ago" % (day))
    else:
        return ("%d hrs ago" % (hour))
