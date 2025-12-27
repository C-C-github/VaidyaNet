from django.contrib import admin
from django.urls import path, include
from core.views import user_login

urlpatterns = [
    path("login/", user_login),
    path("admin/", admin.site.urls),

    path("patients/", include("patients.urls")),
    path("doctors/", include("doctors.urls")),
    path("appointments/", include("appointments.urls")),
    path("records/", include("records.urls")),
]
