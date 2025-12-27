from django.http import Http404

def patient_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "PATIENT":
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper

def doctor_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "DOCTOR":
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper

def admin_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper
