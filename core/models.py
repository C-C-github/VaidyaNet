from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Hospital Admin'),
        ('DEVELOPER', 'Developer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
def save(self, *args, **kwargs):
    if self.role in ["DOCTOR", "PATIENT"]:
        self.is_staff = False
        self.is_superuser = False
    elif self.role == "ADMIN":
        self.is_staff = True
        self.is_superuser = False
    elif self.role == "DEVELOPER":
        self.is_staff = True
        self.is_superuser = True

    super().save(*args, **kwargs)
