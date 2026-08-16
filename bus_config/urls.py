from django.contrib import admin
from django.urls import path
from bus import views


urlpatterns = [

    # Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Login
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Bus Tracking Page
    path(
        "track/<int:bus_id>/",
        views.track_bus,
        name="track_bus"
    ),

    # Driver Dashboard
    path(
        "driver/",
        views.driver_dashboard,
        name="driver_dashboard"
    ),

    # Student Dashboard
    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    # --------------------------------
    # LIVE GPS API
    # --------------------------------

    # Driver sends GPS location
    path(
        "api/bus/<int:bus_id>/location/update/",
        views.update_bus_location,
        name="update_bus_location"
    ),

    # Student gets current GPS location
    path(
        "api/bus/<int:bus_id>/location/",
        views.get_bus_location,
        name="get_bus_location"
    ),
]