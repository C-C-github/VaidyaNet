from django.shortcuts import render
from core.permissions import admin_required
from patients.models import PatientProfile


@admin_required
def admin_patient_ui(request, patient_id):
    patient = PatientProfile.objects.get(id=patient_id)

    return render(request, "admin/patient_summary.html", {
        "patient": patient
    })
