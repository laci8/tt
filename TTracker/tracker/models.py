from django.db import models

class Visitor(models.Model):
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    device_info = models.CharField(max_length=200, blank=True)

    screen_resolution = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=20, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)

    canvas_fp = models.CharField(max_length=128, blank=True, null=True)
    webgl_fp = models.CharField(max_length=128, blank=True, null=True)
    fonts_fp = models.TextField(blank=True, null=True)
    audio_fp = models.CharField(max_length=128, blank=True, null=True)
    device_fp = models.CharField(max_length=128, blank=True, null=True)
    plugins = models.TextField(blank=True, null=True)

    is_touch_device = models.BooleanField(default=False)
    webrtc_support = models.BooleanField(default=False)
    cpu_cores = models.PositiveSmallIntegerField(blank=True, null=True)
    device_memory = models.PositiveSmallIntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)

    is_vpn = models.BooleanField(default=False)
    is_tor = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    threat_score = models.PositiveSmallIntegerField(default=0)

    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"

    def __str__(self):
        return f"Visitor {self.ip_address} from {self.country}"


class PageVisit(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='visits')
    url = models.CharField(max_length=500)
    referrer = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit to {self.url} by {self.visitor.ip_address}"


class BehaviorData(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    page_url = models.CharField(max_length=500)
    mouse_movements = models.JSONField(default=list)
    clicks = models.JSONField(default=list)
    scroll_events = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Behavior data for {self.visitor.ip_address} on {self.page_url}"
