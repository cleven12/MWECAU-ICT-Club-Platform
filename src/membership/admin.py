from django.contrib import admin
from django.utils.html import format_html
from .models import MembershipPayment, PaymentWebhookLog


class MembershipPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'user_name', 'amount', 'provider',
        'status_badge', 'created_at'
    )
    list_filter = ('status', 'provider', 'created_at')
    search_fields = ('user__full_name', 'transaction_id', 'reference_code')
    readonly_fields = ('created_at', 'updated_at', 'paid_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Payment Details', {
            'fields': ('amount', 'provider', 'status', 'transaction_id', 'reference_code')
        }),
        ('Additional Info', {
            'fields': ('payment_method_details',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_failed']
    
    def user_name(self, obj):
        return obj.user.full_name
    user_name.short_description = 'Member'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'processing': '#17a2b8',
            'success': '#28a745',
            'failed': '#dc3545',
            'cancelled': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px;">{obj.get_status_display()}</span>'
        )
    status_badge.short_description = 'Payment Status'
    
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(status='success', paid_at=timezone.now())
        self.message_user(request, f'{count} payments marked as successful.')
    mark_as_paid.short_description = 'Mark selected as paid'
    
    def mark_as_failed(self, request, queryset):
        count = queryset.update(status='failed')
        self.message_user(request, f'{count} payments marked as failed.')
    mark_as_failed.short_description = 'Mark selected as failed'


class PaymentWebhookLogAdmin(admin.ModelAdmin):
    list_display = ('provider', 'event_type', 'processed_badge', 'payment', 'created_at')
    list_filter = ('provider', 'event_type', 'processed', 'created_at')
    search_fields = ('provider', 'event_type')
    readonly_fields = ('created_at', 'raw_data')
    
    def processed_badge(self, obj):
        if obj.processed:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Processed</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
            )
    processed_badge.short_description = 'Status'


admin.site.register(MembershipPayment, MembershipPaymentAdmin)
admin.site.register(PaymentWebhookLog, PaymentWebhookLogAdmin)
