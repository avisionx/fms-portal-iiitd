import csv
from datetime import datetime

from authentication.decorators import fms_required
from authentication.forms import FMSUserForm
from authentication.models import FMS
from dashboard.forms import (ComplaintCategoriesForm, LocationChoicesForm,
                             NotificationForm)
from dashboard.models import ComplaintCategories, LocationChoices
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.forms.widgets import TextInput
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_filters import (CharFilter, ChoiceFilter, DateTimeFilter,
                            FilterSet, OrderingFilter)
from django_filters.filters import NumberFilter

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


class ChartFilter(FilterSet):

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

    year = NumberFilter(field_name='created_at',
                        lookup_expr='year', label="Year", widget=TextInput(attrs={
                            'placeholder': 'Year', 'type': 'number', 'max': datetime.now().date().year}))

    active = ChoiceFilter(field_name='active', label='Status',
                          empty_label='All', choices=((True, 'Active'), (False, 'Closed')))

    def custom_search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(customer__user__username__contains=value) | Q(
                customer__contact__contains=value) | Q(complaint_id__contains=value) | Q(customer__user__first_name__contains=value) | Q(customer__user__last_name__contains=value)
        )


class RemindersFilter(FilterSet):

    search = CharFilter(method='custom_search_filter', label='Search', widget=TextInput(
        attrs={'placeholder': 'Search by Complaint ID, Username, Email, Contact'}))

    category = ChoiceFilter(
        field_name='category', empty_label='All', choices=Complaint.COMPLAINT_CATEGORIES, label='Complaint Category')

    location = ChoiceFilter(field_name='location',
                            empty_label='All', choices=Complaint.LOCATION_CHOICES, label='Complaint Location')

    rating = ChoiceFilter(field_name='rating',
                          empty_label='Any', choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), ), label='Rating')

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

    countActive = Complaint.objects.filter(
        active=True).count()
    countTotal = Complaint.objects.count()
    activePercent = (countActive * 100) // countTotal

    topComplaints = Complaint.objects.all().order_by('-created_at')[:3]

    yearCount = Complaint.objects.filter(
        created_at__year=datetime.now().year).values_list('created_at__month').annotate(total=Count('pk'))

    yearCounts = [0] * 12
    for (month, count) in yearCount:
        yearCounts[month - 1] = count

    context = {
        "dashboard_link": "active",
        "last_complaint": Complaint.objects.latest('created_at').complaint_id,
        "activePercent": activePercent,
        "countActive": countActive,
        "countTotal": countTotal,
        'complaints': topComplaints,
        'yearCounts': list(yearCounts)
    }

    return render(request, 'admin/dashboard.html', context)


@ fms_required
def complaints(request):

    filtered_complaints = ComplaintFilter(
        request.GET, queryset=Complaint.objects.all().order_by('-created_at')
    )

    paginator = Paginator(filtered_complaints.qs, 18)
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


@ fms_required
def charts(request):

    filtered_complaints = ChartFilter(
        request.GET, queryset=Complaint.objects.all()
    )

    yearCount = filtered_complaints.qs.values_list(
        'created_at__month').annotate(total=Count('pk'))

    yearCounts = [0] * 12
    for (month, count) in yearCount:
        yearCounts[month - 1] = count

    context = {
        "charts_link": "active",
        'filter': filtered_complaints,
        'yearCounts': yearCounts
    }

    if request.POST:
        complaints = filtered_complaints.qs
        keys = complaints[0].csv().keys()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fms-complaints-' + \
            datetime.now().strftime("%Y-%m-%d-%H:%M")+'.csv"'
        writer = csv.writer(response)
        writer.writerow(keys)
        for complaint in filtered_complaints.qs:
            writer.writerow(complaint.csv().values())
        return response
    return render(request, 'admin/charts.html', context)


@ fms_required
def reminders(request):

    filtered_complaints = RemindersFilter(
        request.GET, queryset=Complaint.objects.filter(
            active=True, reminder__lte=datetime.today()).order_by('-reminder')
    )

    paginator = Paginator(filtered_complaints.qs, 18)
    page = request.GET.get('page', 1)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)

    context = {
        "reminders_link": "active",
        'filter': filtered_complaints,
        'complaints': res
    }

    return render(request, 'admin/reminders.html', context)


@ fms_required
def fms_users(request):

    fmsUserForm = FMSUserForm(request.POST or None)

    qs = FMS.objects.filter(user__is_superuser=False).order_by(
        '-user__date_joined')

    context = {
        "fms_users_link": "active",
        'fmsUsers': qs,
        'fmsUserForm': fmsUserForm
    }

    if fmsUserForm.is_valid():
        error = fmsUserForm.save()
        if error:
            messages.error(
                request, "User already exists!")
        else:
            messages.success(
                request, "New FMS User has been registerd!")
        return redirect('admin_fms_users')

    return render(request, 'admin/fms_users.html', context)


@ fms_required
def notifications(request):

    notificationForm = NotificationForm(request.POST or None)

    qs = Notification.objects.all().order_by('-created_at')

    context = {
        "notifications_link": "active",
        'notifications': qs,
        'notificationForm': notificationForm
    }

    if notificationForm.is_valid():
        notificationForm.save()
        messages.success(
            request, "Your notification has been registerd!")
        return redirect('admin_notifications')

    return render(request, 'admin/notifications.html', context)


@fms_required
@user_passes_test(lambda u: u.is_superuser)
def settings(request):

    complaintCategoriesForm = ComplaintCategoriesForm(request.POST or None)
    ComplaintCategories_QS = ComplaintCategories.objects.all().order_by('-active', 'name')

    locationChoicesForm = LocationChoicesForm(request.POST or None)
    LocationChoices_QS = LocationChoices.objects.all().order_by('-active', 'name')

    context = {
        "settings_link": "active",
        'complaint_categories': ComplaintCategories_QS,
        'complaintCategoriesForm': complaintCategoriesForm,
        'location_choices': LocationChoices_QS,
        'locationChoicesForm': locationChoicesForm
    }

    if complaintCategoriesForm.is_valid():
        complaintCategoriesForm.save()
        messages.success(
            request, "New complaint category has been created!")
        return redirect('admin_settings')

    if locationChoicesForm.is_valid():
        locationChoicesForm.save()
        messages.success(
            request, "New location choice has been created!")
        return redirect('admin_settings')

    return render(request, 'admin/settings.html', context)


@ fms_required
def edit_profile(request):
    msg = {
        "save": False
    }

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        password1 = request.POST["password1"]
        if(password and (password == password1)):
            request.user.set_password(password)
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            msg["save"] = True
        elif(password):
            msg["err"] = True
        else:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            msg["save"] = True

    formData = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, "admin/edit_profile.html", {'msg': msg, 'formData': formData})


@ fms_required
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


@ fms_required
def set_complaint_reminder(request):
    complaintId = request.POST['id']
    date = request.POST['date']
    complaint = Complaint.objects.get(complaint_id=complaintId)
    complaint.reminder = datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    complaint.save()
    return JsonResponse({"status": 200}, safe=False)


@ fms_required
def notification_action(request):
    pk = request.POST['id']
    status = request.POST['status']
    notification = Notification.objects.get(pk=pk)
    if int(status) == 1:
        notification.delete()
    else:
        notification.active = False
        notification.save()
    return JsonResponse({"status": 200}, safe=False)


@ fms_required
def complaint_category_action(request):
    id = request.POST['id']
    status = request.POST['status']
    complaintcat = ComplaintCategories.objects.get(id=id)
    if int(status) == 1:
        complaintcat.active = True
    else:
        complaintcat.active = False
    complaintcat.save()
    return JsonResponse({"status": 200}, safe=False)


@ fms_required
def location_choice_action(request):
    id = request.POST['id']
    status = request.POST['status']
    locationchoc = LocationChoices.objects.get(id=id)
    if int(status) == 1:
        locationchoc.active = True
    else:
        locationchoc.active = False
    locationchoc.save()
    return JsonResponse({"status": 200}, safe=False)


@ fms_required
def fms_user_action(request):
    pk = request.POST['id']
    status = int(request.POST['status'])
    fmsUser = FMS.objects.get(pk=pk)
    activeCount = FMS.objects.filter(user__is_active=True).count()
    if activeCount > 1:
        if status == -1:
            fmsUser.user.delete()
        elif status != 1:
            fmsUser.user.is_active = False
    if status == 1:
        fmsUser.user.is_active = True
    fmsUser.user.save()
    return JsonResponse({"status": 200}, safe=False)


@ fms_required
def last_complaint(request, slug):
    if request.is_ajax():
        complaint_id = Complaint.objects.latest('created_at').complaint_id
        if str(complaint_id) == str(slug):
            return JsonResponse(slug, safe=False)
        else:
            return JsonResponse(complaint_id, safe=False)
    else:
        return redirect("admin_dashboard")
