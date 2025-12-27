from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if not user:
            return render(request, "auth/login.html", {"error": "Invalid credentials"})

        login(request, user)

        if user.role == "PATIENT":
            return redirect("/patients/dashboard/")
        elif user.role == "DOCTOR":
            return redirect("/doctors/dashboard/")
        else:
            return redirect("/admin/")

    return render(request, "auth/login.html")
