from django.shortcuts import render
from django.http import Http404, JsonResponse
from core.permissions import patient_required, admin_required
from .models import PatientProfile
from appointments.models import Appointment
from .serializers import AdminPatientMaskedSerializer


@patient_required
def patient_dashboard(request):
    try:
        patient = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        raise Http404

    appointments = Appointment.objects.filter(patient=patient)

    return render(
        request,
        "patients/dashboard.html",
        {"appointments": appointments}
    )


@admin_required
def admin_patient_problem_view(request, patient_id):
    try:
        patient = PatientProfile.objects.only(
            "id", "problem_summary"
        ).get(id=patient_id)
    except PatientProfile.DoesNotExist:
        raise Http404

    return JsonResponse(AdminPatientMaskedSerializer(patient).data)
