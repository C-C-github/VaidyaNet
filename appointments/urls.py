from django.urls import path
from .views import (
    book_appointment,
    doctor_update_appointment,
    my_appointments
)

urlpatterns = [
    path("book/", book_appointment),
    path("mine/", my_appointments),
    path("doctor/update/<int:appointment_id>/", doctor_update_appointment),
]
