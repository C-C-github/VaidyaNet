import json
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from core.permissions import doctor_required
from core.mongo import medical_records
from appointments.models import Appointment
from doctors.models import DoctorProfile
from audit.utils import log_action


@csrf_exempt
@doctor_required
def create_or_update_record(request, appointment_id):
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

    record = medical_records.find_one({"appointment_id": appointment_id})

    if record and record.get("finalized"):
        return JsonResponse(
            {"error": "Record is finalized and cannot be modified"},
            status=403
        )

    # ✅ Parse RAW JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400
        )

    diagnosis = payload.get("diagnosis")
    prescriptions = payload.get("prescriptions")
    lab_reports = payload.get("lab_reports")

    if not diagnosis:
        return JsonResponse(
            {"error": "Diagnosis is required"},
            status=400
        )

    data = {
        "appointment_id": appointment_id,
        "patient_id": appointment.patient.id,
        "doctor_id": doctor.id,
        "diagnosis": diagnosis,
        "prescriptions": prescriptions,
        "lab_reports": lab_reports,
        "finalized": False
    }

    if record:
        medical_records.update_one(
            {"appointment_id": appointment_id},
            {"$set": data}
        )
        action = "updated"
    else:
        medical_records.insert_one(data)
        action = "created"

    # ✅ Audit log INSIDE function
    log_action(
        user=request.user,
        action=f"medical_record_{action}",
        resource_type="appointment",
        resource_id=appointment_id,
        request=request
    )

    return JsonResponse({"status": f"Record {action} successfully"})


@csrf_exempt
@doctor_required
def finalize_record(request, appointment_id):
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

    record = medical_records.find_one({"appointment_id": appointment_id})

    if not record:
        raise Http404

    medical_records.update_one(
        {"appointment_id": appointment_id},
        {"$set": {"finalized": True}}
    )

    # ✅ Audit log for finalize
    log_action(
        user=request.user,
        action="medical_record_finalized",
        resource_type="appointment",
        resource_id=appointment_id,
        request=request
    )

    return JsonResponse({"status": "Record finalized and locked"})
