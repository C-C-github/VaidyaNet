from django.urls import path
from .views import view_audit_logs

urlpatterns = [
    path("logs/", view_audit_logs),
]
