from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip
from user_agents import parse
from .models import Visitor, PageVisit
import hashlib
from geoip2.database import Reader
from django.conf import settings

def get_canvas_fp(request):
    if request.method == 'POST' and 'canvas_data' in request.POST:
        return hashlib.md5(request.POST['canvas_data'].encode()).hexdigest()
    return ''

class TrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(('/admin', '/static', '/track-behavior')):
            return

        ip, _ = get_client_ip(request)
        if not ip:
            return

        ua_string = request.META.get('HTTP_USER_AGENT', '')
        ua = parse(ua_string)
        device_info = f"{ua.browser.family} / {ua.os.family} / {ua.device.family}"

        lang = request.headers.get('Accept-Language', '').split(',')[0]
        tz = request.COOKIES.get('tz')  # JavaScript imposta timezone nei cookie se possibile

        Visitor.objects.update_or_create(
            ip_address=ip,
            defaults={
                'user_agent': ua_string,
                'device_info': device_info,
                'language': lang,
                'timezone': tz,
            }
        )