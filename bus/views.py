from django.shortcuts import render, redirect, get_object_or_404
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
        return redirect("driver_dashboard")

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
            return redirect("driver_dashboard")

        return render(
            request,
            "bus/login.html",
            {
                "error": "Incorrect username or password"
            }
        )

    return render(request, "bus/login.html")


# -------------------------------
# LOGOUT
# -------------------------------

def logout_view(request):

    logout(request)

    return redirect("login")


# -------------------------------
# BUS DETAILS
# -------------------------------

def create_default_buses():

    bus46, _ = Bus.objects.get_or_create(
        bus_number="46",
        defaults={
            "time": "07:50",
            "destination": "Shanmuga Industries Arts and Science College",
            "latitude": 0,
            "longitude": 0,
            "gps_active": False,
        }
    )

    bus5, _ = Bus.objects.get_or_create(
        bus_number="5",
        defaults={
            "time": "07:50",
            "destination": "Shanmuga Industries Arts and Science College",
            "latitude": 0,
            "longitude": 0,
            "gps_active": False,
        }
    )

    return bus46, bus5


# -------------------------------
# HOME
# -------------------------------

def home(request):

    if not request.user.is_authenticated:
        return redirect("login")

    bus46, bus5 = create_default_buses()

    return render(
        request,
        "bus/home.html",
        {
            "bus46": bus46,
            "bus5": bus5,

            "bus46_stop": "Polur Bus Stand",
            "bus5_stop": "Anjaneyar Kovil, Polur",

            "college": "Shanmuga Industries Arts and Science College",
        }
    )


# -------------------------------
# TRACK BUS
# -------------------------------

def track_bus(request, bus_id):

    if not request.user.is_authenticated:
        return redirect("login")

    bus = get_object_or_404(Bus, id=bus_id)

    return render(
        request,
        "bus/track.html",
        {
            "bus": bus
        }
    )


# -------------------------------
# DRIVER DASHBOARD
# -------------------------------

@ensure_csrf_cookie
def driver_dashboard(request):

    bus46, bus5 = create_default_buses()

    buses = Bus.objects.all().order_by("bus_number")

    return render(
        request,
        "bus/driver_dashboard.html",
        {
            "buses": buses,

            "bus46": bus46,
            "bus5": bus5,

            "bus46_stop": "Polur Bus Stand",
            "bus5_stop": "Anjaneyar Kovil, Polur",

            "bus46_time": "7:50 AM",
            "bus5_time": "7:50 AM",

            "college": "Shanmuga Industries Arts and Science College",
        }
    )


# -------------------------------
# STUDENT DASHBOARD
# -------------------------------

def student_dashboard(request):

    bus46, bus5 = create_default_buses()

    buses = Bus.objects.all().order_by("bus_number")

    return render(
        request,
        "bus/student_dashboard.html",
        {
            "buses": buses,

            "bus46": bus46,
            "bus5": bus5,

            "bus46_stop": "Polur Bus Stand",
            "bus5_stop": "Anjaneyar Kovil, Polur",

            "bus46_time": "7:50 AM",
            "bus5_time": "7:50 AM",

            "college": "Shanmuga Industries Arts and Science College",
        }
    )


# -------------------------------
# LIVE GPS UPDATE
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
        bus.gps_active = True

        bus.save(
            update_fields=[
                "latitude",
                "longitude",
                "gps_active"
            ]
        )

        return JsonResponse({
            "success": True,
            "bus": bus.bus_number,
            "latitude": bus.latitude,
            "longitude": bus.longitude,
            "gps_active": bus.gps_active
        })

    except Bus.DoesNotExist:

        return JsonResponse(
            {"error": "Bus not found"},
            status=404
        )

    except (TypeError, ValueError):

        return JsonResponse(
            {"error": "Invalid GPS coordinates"},
            status=400
        )


# -------------------------------
# GET BUS LOCATION
# -------------------------------

def get_bus_location(request, bus_id):

    if not request.user.is_authenticated:

        return JsonResponse(
            {"error": "Login required"},
            status=401
        )

    try:

        bus = Bus.objects.get(id=bus_id)

        return JsonResponse({
            "bus": bus.bus_number,
            "latitude": bus.latitude,
            "longitude": bus.longitude,
            "gps_active": bus.gps_active
        })

    except Bus.DoesNotExist:

        return JsonResponse(
            {"error": "Bus not found"},
            status=404
        )