from django.contrib import admin
from django.utils.html import format_html
from .models import SystemSettings, Service, Counter, Ticket, DisplayAd 

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'enable_voice_alert', 'last_reset_date')
    def has_add_permission(self, request):
        return not SystemSettings.objects.exists()



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'avg_service_time', 'is_active')
    list_editable = ('is_active',)

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('number', 'display_services', 'staff_member', 'is_active')
    filter_horizontal = ('services',)
    
    def display_services(self, obj):
        return ", ".join([s.name for s in obj.services.all()])
    display_services.short_description = "الخدمات"

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('get_code', 'service', 'counter', 'colored_status', 'created_at', 'get_wait_time')
    list_filter = ('status', 'service', 'counter')
    
    fieldsets = (
        ("بيانات التذكرة", {'fields': ('service', 'number', 'status', 'counter')}),
        ("المواعيد", {'fields': ('created_at', 'called_at', 'started_at', 'finished_at')}),
    )
    readonly_fields = ('created_at',)

    def get_code(self, obj):
        return obj.ticket_code
    get_code.short_description = "الرمز"

    def colored_status(self, obj):
        colors = {'waiting': '#FFA500', 'calling': '#007bff', 'serving': '#28a745', 'completed': '#6c757d', 'skipped': '#dc3545'}
        return format_html('<b style="color: {};">{}</b>', colors.get(obj.status, 'black'), obj.get_status_display())
    colored_status.short_description = "الحالة"

    def get_wait_time(self, obj):
        wait = obj.wait_time
        return f"{wait} دقيقة" if wait is not None else "الانتظار..."
    get_wait_time.short_description = "الانتظار"

@admin.register(DisplayAd)
class DisplayAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')