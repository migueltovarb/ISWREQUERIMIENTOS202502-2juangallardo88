from django.contrib import admin
from .models import Claim, ClaimHistory, Notification, AdminActivity, FAQ

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('number', 'full_name', 'priority', 'status', 'zone', 'created_at', 'assigned_to')
    search_fields = ('number', 'order_number', 'full_name', 'email', 'phone')
    list_filter = ('status', 'priority', 'zone', 'created_at')
    readonly_fields = ('number', 'created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('number', 'full_name', 'email', 'phone', 'contact')
        }),
        ('Detalle del Reclamo', {
            'fields': ('order_number', 'description', 'evidence', 'zone')
        }),
        ('Prioridad y Estado', {
            'fields': ('priority', 'status', 'assigned_to')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ClaimHistory)
class ClaimHistoryAdmin(admin.ModelAdmin):
    list_display = ('claim', 'old_status', 'new_status', 'changed_by', 'change_date')
    search_fields = ('claim__number',)
    list_filter = ('change_date',)
    readonly_fields = ('claim', 'old_status', 'new_status', 'changed_by', 'change_date')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('claim', 'notification_type', 'sent', 'created_at')
    search_fields = ('claim__number', 'user_email')
    list_filter = ('notification_type', 'sent', 'created_at')
    readonly_fields = ('claim', 'created_at')

@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'claim', 'created_at')
    search_fields = ('user__username', 'claim__number', 'action')
    list_filter = ('user', 'created_at')
    readonly_fields = ('user', 'claim', 'action', 'description', 'created_at')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    search_fields = ('question', 'answer')
    list_filter = ('is_active',)
    ordering = ('order',)
