# doctors/urls.py
from django.urls import path
from .views import doctor_dashboard

urlpatterns += [
    path("dashboard/", doctor_dashboard),
]
