
from django.http import Http404


class BlockUnauthorizedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Allow admin & login to behave normally
        if request.path.startswith("/admin/") or request.path.startswith("/login/"):
            return self.get_response(request)

        response = self.get_response(request)

        if response.status_code == 403:
            raise Http404

        return response
