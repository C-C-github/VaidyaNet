from django.http import Http404
from django.shortcuts import redirect
from django.conf import settings

def patient_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if request.user.role != "PATIENT":
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper

def doctor_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if request.user.role != "DOCTOR":
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper

def admin_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_staff:
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper
