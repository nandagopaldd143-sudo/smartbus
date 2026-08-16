from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Bus


# -------------------------------
# LOGIN
# -------------------------------

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

    return render(
        request,
        "bus/login.html"
    )


# -------------------------------
# LOGOUT
# -------------------------------

def logout_view(request):

    logout(request)

    return redirect("login")


# -------------------------------
# HOME
# -------------------------------

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


# -------------------------------
# TRACK BUS
# -------------------------------

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


# -------------------------------
# DRIVER DASHBOARD
# NO LOGIN REQUIRED
# -------------------------------

@ensure_csrf_cookie
def driver_dashboard(request):

    return render(
        request,
        "bus/driver_dashboard.html"
    )


# -------------------------------
# STUDENT DASHBOARD
# LOGIN REQUIRED
# -------------------------------

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


# -------------------------------
# LIVE GPS API
# DRIVER LOGIN NOT REQUIRED
# -------------------------------

@require_POST
def update_bus_location(request, bus_id):

    try:

        bus = Bus.objects.get(id=bus_id)

        latitude = float(
            request.POST.get("latitude")
        )

        longitude = float(
            request.POST.get("longitude")
        )

        bus.latitude = latitude
        bus.longitude = longitude

        bus.save(
            update_fields=[
                "latitude",
                "longitude"
            ]
        )

        return JsonResponse({

            "success": True,

            "bus": bus.bus_number,

            "latitude": bus.latitude,

            "longitude": bus.longitude

        })

    except Bus.DoesNotExist:

        return JsonResponse(
            {
                "error": "Bus not found"
            },
            status=404
        )

    except (TypeError, ValueError):

        return JsonResponse(
            {
                "error": "Invalid GPS coordinates"
            },
            status=400
        )


# -------------------------------
# GET CURRENT BUS LOCATION
# STUDENT LOGIN REQUIRED
# -------------------------------

def get_bus_location(request, bus_id):

    if not request.user.is_authenticated:

        return JsonResponse(
            {
                "error": "Login required"
            },
            status=401
        )

    try:

        bus = Bus.objects.get(id=bus_id)

        return JsonResponse({

            "bus": bus.bus_number,

            "latitude": bus.latitude,

            "longitude": bus.longitude

        })

    except Bus.DoesNotExist:

        return JsonResponse(
            {
                "error": "Bus not found"
            },
            status=404
        )