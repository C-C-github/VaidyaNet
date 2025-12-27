from django.http import JsonResponse, Http404
from core.permissions import doctor_required
from .models import DoctorProfile
from appointments.models import Appointment


@doctor_required
def assigned_patients(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        raise Http404

    appointments = Appointment.objects.filter(doctor=doctor)

    data = []
    for appt in appointments:
        data.append({
            "patient": appt.patient.user.username,
            "problem_summary": appt.patient.problem_summary,
            "status": appt.status
        })

    return JsonResponse({"assigned_patients": data})
