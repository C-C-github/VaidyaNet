from django.http import JsonResponse, Http404
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST
from core.permissions import patient_required, doctor_required
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from .models import Appointment
from audit.utils import log_action

@require_POST
@patient_required
def book_appointment(request):
    try:
        patient = PatientProfile.objects.get(user=request.user)
        doctor_id = request.POST.get("doctor_id")
        date = request.POST.get("date")
        time = request.POST.get("time")

        doctor = DoctorProfile.objects.get(id=doctor_id)
    except (PatientProfile.DoesNotExist, DoctorProfile.DoesNotExist):
        raise Http404

    try:
        # 🔒 Atomic booking (prevents race conditions)
        with transaction.atomic():
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=date,
                appointment_time=time,
                status="requested"
            )
    except IntegrityError:
        return JsonResponse(
            {"error": "This slot is already booked"},
            status=400
        )
    log_action(
    user=request.user,
    action="appointment_requested",
    resource_type="appointment",
    resource_id=appointment.id,
    request=request
)

    return JsonResponse({
        "status": "Appointment requested",
        "appointment_id": appointment.id
    })
@doctor_required
def doctor_update_appointment(request, appointment_id):
    if request.method != "POST":
        raise Http404

    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        appointment = Appointment.objects.get(
            id=appointment_id,
            doctor=doctor
        )
    except (DoctorProfile.DoesNotExist, Appointment.DoesNotExist):
        raise Http404

    action = request.POST.get("action")

    if action == "confirm":
        appointment.status = "confirmed"
    elif action == "complete":
        appointment.status = "completed"
    elif action == "cancel":
        appointment.status = "cancelled"
    else:
        return JsonResponse({"error": "Invalid action"}, status=400)

    appointment.save()
    log_action(
        user=request.user,
        action=f"appointment_{appointment.status}",
        resource_type="appointment",
        resource_id=appointment.id,
        request=request
    )
    return JsonResponse({
        "status": f"Appointment {appointment.status}"
    })
@patient_required
def my_appointments(request):
    patient = PatientProfile.objects.get(user=request.user)

    appointments = Appointment.objects.filter(patient=patient)

    data = []
    for a in appointments:
        data.append({
            "doctor": a.doctor.user.username,
            "date": a.appointment_date,
            "time": a.appointment_time,
            "status": a.status
        })
    return JsonResponse({"appointments": data})
