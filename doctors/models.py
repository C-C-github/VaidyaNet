from django.conf import settings
from django.db import models


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
