from django.db import models
from core.models import User


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    problem_summary = models.TextField(blank=True, null=True)

    # ✅ DJONGO-SAFE FIELDS
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username
