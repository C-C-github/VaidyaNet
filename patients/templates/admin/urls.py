# patients/urls.py
urlpatterns += [
    path("admin/ui/<int:patient_id>/", admin_patient_ui),
]
