from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("requested", "Requested"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    appointment_date = models.DateField(default="2025-01-01")
    appointment_time = models.TimeField(default="09:00")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="requested"
    )

    # ✅ DJONGO-SAFE
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("doctor", "appointment_date", "appointment_time")
