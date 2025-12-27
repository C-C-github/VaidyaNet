from django.db import models
from appointments.models import Appointment


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    is_finalized = models.BooleanField(default=False)
