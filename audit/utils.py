from core.mongo import audit_logs
from datetime import datetime


def log_action(
    *,
    user,
    action,
    resource_type,
    resource_id=None,
    request=None,
    extra=None
):
    audit_logs.insert_one({
        "username": user.username if user else None,
        "role": getattr(user, "role", None),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "ip_address": get_client_ip(request),
        "user_agent": request.META.get("HTTP_USER_AGENT") if request else None,
        "timestamp": datetime.utcnow(),
        "extra": extra or {}
    })


def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")
