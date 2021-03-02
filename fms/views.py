from django.contrib.auth import logout
from django.shortcuts import redirect, render


def HomeView(request):
    return render(request, "index.html")


def LoginRedirectView(request):
    if request.user.is_superuser:
        request.user.is_fms = True
        request.user.is_customer = False
        request.user.save()
    if request.user.is_customer:
        return redirect('customer_dashboard')
    elif request.user.is_fms:
        return redirect('admin_dashboard')
    return redirect('index')


def LogoutView(request):
    logout(request)
    return render(request, "registration/logged_out.html")
