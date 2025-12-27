from django.shortcuts import render
from core.permissions import doctor_required
from doctors.models import DoctorProfile
from appointments.models import Appointment


@doctor_required
def doctor_dashboard(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "doctors/dashboard.html", {
        "appointments": appointments
    })
