from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils import timezone
from .models import Transaction, PaymentReport

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order_link', 'amount', 'payment_method', 
                   'status', 'created_at', 'reference_number']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'reference_number', 'order__id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_id', 'order', 'amount', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'reference_number', 'payment_details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, f"Order #{obj.order.id}")
    order_link.short_description = 'Order'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of completed transactions
        if obj and obj.status == 'completed':
            return False
        return super().has_delete_permission(request, obj)

@admin.register(PaymentReport)
class PaymentReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'report_type', 'total_transactions', 
                   'total_amount', 'successful_transactions', 'generated_at']
    list_filter = ['report_type', 'report_date']
    readonly_fields = ['generated_at', 'total_transactions', 'total_amount',
                      'successful_transactions', 'failed_transactions',
                      'refunded_transactions', 'average_transaction_amount']
    date_hierarchy = 'report_date'
    
    def has_add_permission(self, request):
        # Reports should only be generated through the custom action
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of reports
        return False

    actions = ['generate_report']

    @admin.action(description='Generate new report')
    def generate_report(self, request, queryset):
        today = timezone.now().date()
        
        # Calculate daily statistics
        daily_stats = Transaction.objects.filter(
            created_at__date=today
        ).aggregate(
            total_count=Count('id'),
            total_amount=Sum('amount'),
            successful=Count('id', filter={'status': 'completed'}),
            failed=Count('id', filter={'status': 'failed'}),
            refunded=Count('id', filter={'status': 'refunded'})
        )

        if daily_stats['total_count'] > 0:
            avg_amount = daily_stats['total_amount'] / daily_stats['total_count']
        else:
            avg_amount = 0

        # Create or update daily report
        PaymentReport.objects.update_or_create(
            report_date=today,
            report_type='daily',
            defaults={
                'total_transactions': daily_stats['total_count'] or 0,
                'total_amount': daily_stats['total_amount'] or 0,
                'successful_transactions': daily_stats['successful'] or 0,
                'failed_transactions': daily_stats['failed'] or 0,
                'refunded_transactions': daily_stats['refunded'] or 0,
                'average_transaction_amount': avg_amount,
                'report_data': daily_stats
            }
        )

    class Media:
        css = {
            'all': ('admin/css/payment_report.css',)
        }
        js = ('admin/js/payment_report.js',)
