from django.http import HttpResponse
from django.conf import settings

class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == settings.HEALTH_CHECK_URL:
            return HttpResponse("OK", content_type="text/plain")
        return self.get_response(request) 