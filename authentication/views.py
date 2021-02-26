from django.contrib.auth import login
from django.shortcuts import redirect, render

from .models import FMS, Customer, User


def CustomerSignUpView(request):

    error = {
        "password": False,
        "unique": False,
        "iiitd": False
    }

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        contact = request.POST["contact"]

        if(not username.endswith("@iiitd.ac.in")):
            error["iiitd"] = True
        elif(pass1 != pass2):
            error["password"] = True
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    email=username,
                    first_name=first_name,
                    last_name=last_name
                )
                user.is_customer = True
                user.save()
                customer = Customer.objects.create(user=user, contact=contact)
                customer.save()
                login(request, user)
                return redirect('customer_dashboard')
            except Exception as inst:
                error["unique"] = True

    return render(request, "registration/register_customer.html", {'error': error})
