from django.urls import path
from .views import assigned_patients

urlpatterns = [
    path('assigned/', assigned_patients),
]
