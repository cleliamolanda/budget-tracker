from django.http import HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == settings.HEALTH_CHECK_URL:
            return HttpResponse("OK", content_type="text/plain", status=200)
        return None 