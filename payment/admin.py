from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count, Q
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
    list_per_page = 20
    
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

@admin.register(PaymentReport)
class PaymentReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'report_type', 'total_transactions', 
                   'total_amount', 'successful_transactions', 'total_profit',
                   'total_loss', 'net_revenue', 'generated_at']
    list_filter = ['report_type', 'report_date']
    readonly_fields = ['generated_at']
    date_hierarchy = 'report_date'
    list_per_page = 20
    search_fields = ['report_type']
    
    fieldsets = (
        ('Report Overview', {
            'fields': ('report_date', 'report_type', 'generated_at')
        }),
        ('Transaction Statistics', {
            'fields': ('total_transactions', 'successful_transactions',
                      'failed_transactions', 'refunded_transactions',
                      'average_transaction_amount')
        }),
        ('Financial Summary', {
            'fields': ('total_amount', 'total_profit', 'total_loss',
                      'net_revenue'),
            'classes': ('wide',)
        }),
        ('Detailed Data', {
            'fields': ('report_data',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    actions = ['generate_report']

    @admin.action(description='Generate new report')
    def generate_report(self, request, queryset):
        today = timezone.now().date()
        
        # Calculate daily statistics
        transactions = Transaction.objects.filter(created_at__date=today)
        daily_stats = transactions.aggregate(
            total_count=Count('id'),
            total_amount=Sum('amount'),
            successful=Count('id', filter=Q(status='completed')),
            failed=Count('id', filter=Q(status='failed')),
            refunded=Count('id', filter=Q(status='refunded'))
        )

        # Calculate profits and losses
        completed_transactions = transactions.filter(status='completed')
        refunded_transactions = transactions.filter(status='refunded')
        
        total_profit = completed_transactions.aggregate(
            profit=Sum('amount', default=0))['profit'] or 0
        
        total_loss = refunded_transactions.aggregate(
            loss=Sum('amount', default=0))['loss'] or 0
        
        net_revenue = total_profit - total_loss

        if daily_stats['total_count'] > 0:
            avg_amount = daily_stats['total_amount'] / daily_stats['total_count']
        else:
            avg_amount = 0

        # Enhance report data with payment method breakdown
        payment_methods = transactions.values('payment_method').annotate(
            count=Count('id'),
            total=Sum('amount', default=0)
        ).order_by('payment_method')

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
                'total_profit': total_profit,
                'total_loss': total_loss,
                'net_revenue': net_revenue,
                'report_data': {
                    'statistics': {
                        'total_count': daily_stats['total_count'] or 0,
                        'total_amount': float(daily_stats['total_amount'] or 0),
                        'successful': daily_stats['successful'] or 0,
                        'failed': daily_stats['failed'] or 0,
                        'refunded': daily_stats['refunded'] or 0
                    },
                    'payment_methods': [
                        {
                            'payment_method': pm['payment_method'],
                            'count': pm['count'],
                            'total': float(pm['total'] or 0)
                        } for pm in payment_methods
                    ],
                    'financial_summary': {
                        'total_profit': float(total_profit),
                        'total_loss': float(total_loss),
                        'net_revenue': float(net_revenue)
                    }
                }
            }
        )

    class Media:
        css = {
            'all': ('admin/css/payment_report.css',)
        }
        js = ('admin/js/payment_report.js',)
