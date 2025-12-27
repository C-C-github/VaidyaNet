from django.http import JsonResponse, Http404
from core.permissions import admin_required
from core.mongo import audit_logs


@admin_required
def view_audit_logs(request):
    logs = audit_logs.find().sort("timestamp", -1).limit(100)

    data = []
    for log in logs:
        data.append({
            "user": log.get("username"),
            "role": log.get("role"),
            "action": log.get("action"),
            "resource": log.get("resource_type"),
            "resource_id": log.get("resource_id"),
            "ip": log.get("ip_address"),
            "time": log.get("timestamp"),
        })

    return JsonResponse({"audit_logs": data})
