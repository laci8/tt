from django.http import JsonResponse
from .models import Visitor, BehaviorData, PageVisit
from ipware import get_client_ip
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def register_page_visit(visitor, url, referrer=''):
    PageVisit.objects.create(
        visitor=visitor,
        url=url,
        referrer=referrer or '',
        timestamp=timezone.now()
    )

@csrf_exempt
def track_behavior(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip, _ = get_client_ip(request)
            if not ip:
                return JsonResponse({'status': 'error', 'message': 'IP not found'}, status=400)

            visitor, created = Visitor.objects.get_or_create(
                ip_address=ip,
                defaults={
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'device_info': request.META.get('HTTP_USER_AGENT', '')[:200],
                }
            )

            # Aggiorna dati fingerprint/geolocalizzazione
            visitor.canvas_fp = data.get('canvas_fp', visitor.canvas_fp)
            visitor.webgl_fp = data.get('webgl_fp', visitor.webgl_fp)
            visitor.audio_fp = data.get('audio_fp', visitor.audio_fp)
            visitor.device_fp = data.get('device_fp', visitor.device_fp)
            visitor.plugins = json.dumps(data.get('plugins', []))
            visitor.screen_resolution = data.get('screen_resolution', visitor.screen_resolution)
            visitor.cpu_cores = data.get('cpu_cores', visitor.cpu_cores)
            visitor.device_memory = data.get('device_memory', visitor.device_memory)
            visitor.latitude = data.get('latitude', visitor.latitude)
            visitor.longitude = data.get('longitude', visitor.longitude)
            visitor.city = data.get('city', visitor.city)
            visitor.country = data.get('country', visitor.country)
            visitor.region = data.get('region', visitor.region)
            visitor.is_touch_device = data.get('is_touch_device', visitor.is_touch_device)
            visitor.webrtc_support = data.get('webrtc_support', visitor.webrtc_support)
            visitor.is_vpn = data.get('is_vpn', visitor.is_vpn)
            visitor.is_tor = data.get('is_tor', visitor.is_tor)
            visitor.is_bot = data.get('is_bot', visitor.is_bot)
            visitor.threat_score = data.get('threat_score', visitor.threat_score)
            visitor.language = data.get('language', visitor.language)
            visitor.save()

            # Traccia la visita alla pagina
            register_page_visit(visitor, data.get('page_url', request.path), request.META.get('HTTP_REFERER', ''))

            # Salva solo se c'è almeno un evento
            if data.get('mouse') or data.get('clicks') or data.get('scroll'):
                BehaviorData.objects.create(
                    visitor=visitor,
                    page_url=data.get('page_url', request.path),
                    mouse_movements=data.get('mouse', []),
                    clicks=data.get('clicks', []),
                    scroll_events=data.get('scroll', [])
                )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)

@csrf_exempt
def track_end(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip, _ = get_client_ip(request)
            visitor = Visitor.objects.filter(ip_address=ip).first()
            if not visitor:
                return JsonResponse({'status': 'error', 'message': 'visitor not found'}, status=404)

            visit = PageVisit.objects.filter(visitor=visitor, url=data.get('page_url')).last()
            if visit:
                visit.duration = (timezone.now() - visit.timestamp).total_seconds()
                visit.save()

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)
