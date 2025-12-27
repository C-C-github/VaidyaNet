from django.shortcuts import render
from django.http import Http404
from core.permissions import patient_required
from patients.models import PatientProfile
from appointments.models import Appointment


@patient_required
def patient_dashboard(request):
    try:
        patient = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        raise Http404

    appointments = Appointment.objects.filter(patient=patient)

    return render(request, "patients/dashboard.html", {
        "appointments": appointments
    })
