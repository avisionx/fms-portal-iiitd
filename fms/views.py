from django.contrib.auth import logout
from django.shortcuts import render

from authentication.decorators import student_required

def HomeView(request):
    return render(request, "index.html")

@student_required
def StudentHomeView(request):
    return render(request, "students/home.html")


def LogoutView(request):
    logout(request)
    return render(request, "registration/logged_out.html")
