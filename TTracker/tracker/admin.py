""" from django.contrib import admin
from .models import Visitor, PageVisit, BehaviorData

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address', 
        'device_info', 
        'screen_resolution', 
        'country', 
        'first_seen'
    )
    search_fields = ('ip_address', 'user_agent', 'country', 'city')
    readonly_fields = (
        'first_seen', 
        'last_seen', 
        'latitude', 
        'longitude'
    )


@admin.register(BehaviorData)
class BehaviorDataAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'page_url', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('visitor', 'created_at')

 """

""" 
@admin.register(BehaviorData)
class BehaviorDataAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'page_url', 'timestamp')
    readonly_fields = ('mouse_heatmap', 'click_map')
    
    def mouse_heatmap(self, obj):
        return format_html('<div style="width: 500px; height: 300px; background: #f0f0f0;">Heatmap placeholder</div>')
    
    def click_map(self, obj):
        return format_html('<div style="width: 500px; height: 300px; background: #f0f0f0;">Click map placeholder</div>') """




from django.contrib import admin
from .models import Visitor, PageVisit, BehaviorData

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'device_info', 'city', 'country', 'first_seen', 'last_seen', 'is_vpn', 'is_tor')
    search_fields = ('ip_address', 'user_agent', 'city', 'country')
    readonly_fields = ('first_seen', 'last_seen')
    fieldsets = (
        ('Identificazione', {
            'fields': ('ip_address', 'user_agent', 'device_info', 'language', 'screen_resolution', 'is_touch_device')
        }),
        ('Fingerprinting', {
            'fields': ('canvas_fp', 'webgl_fp', 'fonts_fp', 'audio_fp', 'device_fp', 'plugins')
        }),
        ('Geolocalizzazione', {
            'fields': ('latitude', 'longitude', 'city', 'country', 'region')
        }),
        ('Minacce', {
            'fields': ('is_vpn', 'is_tor', 'is_bot', 'threat_score')
        }),
        ('Altri Dati', {
            'fields': ('webrtc_support', 'device_memory', 'cpu_cores', 'timezone')
        }),
        ('Timestamps', {
            'fields': ('first_seen', 'last_seen')
        }),
    )
    ordering = ('-first_seen',)

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'url', 'referrer', 'timestamp')
"""     
    search_fields = ('visitor__ip_address',)
    list_filter = ('timestamp',)
 """
@admin.register(BehaviorData)
class BehaviorDataAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'page_url', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
