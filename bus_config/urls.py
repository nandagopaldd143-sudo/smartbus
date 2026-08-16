from django.contrib import admin
from django.urls import path
from bus import views


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Premium Login
    path("login/", views.login_view, name="login"),

    # Logout
    path("logout/", views.logout_view, name="logout"),

    # Home Dashboard
    path("", views.home, name="home"),

    # Bus Tracking
    path(
        "track/<int:bus_id>/",
        views.track_bus,
        name="track_bus"
    ),

    # DRIVER DASHBOARD
    path(
        "driver/",
        views.driver_dashboard,
        name="driver_dashboard"
    ),

    # STUDENT DASHBOARD
    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),
]