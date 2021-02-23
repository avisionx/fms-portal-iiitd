from django.contrib.auth import login
from django.shortcuts import redirect, render

from .models import FMS, Student, User


def StudentSignUpView(request):

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
                user.is_student = True
                user.save()
                student = Student.objects.create(user=user, contact=contact)
                student.save()
                login(request, user)
                return redirect('student_home')
            except Exception as inst:
                error["unique"] = True

    return render(request, "registration/register_student.html", {'error': error})


# def FacultySignUpView(request):

#     error = {
#         "password": False,
#         "unique": False
#     }

#     if request.method == "POST":
#         username = request.POST["username"]
#         pass1 = request.POST["password1"]
#         pass2 = request.POST["password2"]
#         first_name = request.POST["first_name"]
#         last_name = request.POST["last_name"]

#         if(pass1 != pass2):
#             error["password"] = True
#         else:
#             try:
#                 user = User.objects.create_user(
#                     username=username,
#                     password=pass1,
#                     email=username,
#                     first_name=first_name,
#                     last_name=last_name
#                 )
#                 user.is_faculty = True
#                 user.save()
#                 faculty = Faculty.objects.create(user=user)
#                 login(request, user)
#                 return redirect('dashboard')
#             except Exception as inst:
#                 print(inst)
#                 error["unique"] = True

#     return render(request, "registration/register_faculty.html", {'error': error})
