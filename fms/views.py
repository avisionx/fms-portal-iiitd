from authentication.decorators import customer_required
from django.contrib.auth import logout
from django.shortcuts import render


def HomeView(request):
    return render(request, "index.html")


def LogoutView(request):
    logout(request)
    return render(request, "registration/logged_out.html")
