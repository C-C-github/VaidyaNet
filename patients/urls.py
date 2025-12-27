from django.urls import path
from .views import patient_dashboard, admin_patient_problem_view

urlpatterns = [
    path("dashboard/", patient_dashboard, name="patient_dashboard"),
    path("admin/problem/<int:patient_id>/", admin_patient_problem_view),
]
