from django.urls import path
from .views import create_or_update_record, finalize_record

urlpatterns = [
    path(
        'doctor/record/<int:appointment_id>/',
        create_or_update_record
    ),
    path(
        'doctor/record/<int:appointment_id>/finalize/',
        finalize_record
    ),
]
