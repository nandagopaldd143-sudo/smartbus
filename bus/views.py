from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Bus


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "bus/login.html",
            {
                "error": "Incorrect username or password"
            }
        )

    return render(request, "bus/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    buses = Bus.objects.all()

    return render(
        request,
        "bus/home.html",
        {
            "buses": buses
        }
    )


def track_bus(request, bus_id):
    if not request.user.is_authenticated:
        return redirect("login")

    bus = Bus.objects.get(id=bus_id)

    return render(
        request,
        "bus/track.html",
        {
            "bus": bus
        }
    )


# DRIVER DASHBOARD
def driver_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "bus/driver_dashboard.html"
    )


# STUDENT DASHBOARD
def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    buses = Bus.objects.all()

    return render(
        request,
        "bus/student_dashboard.html",
        {
            "buses": buses
        }
    )