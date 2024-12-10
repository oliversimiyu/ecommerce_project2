from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractHour
from .models import Transaction, PaymentReport

def get_hourly_breakdown(transactions):
    """Helper function to get hourly transaction breakdown"""
    breakdown = list(transactions.annotate(
        hour=ExtractHour('created_at')
    ).values('hour').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('hour'))
    
    # Convert Decimal to float for JSON serialization
    for item in breakdown:
        if 'total' in item and item['total'] is not None:
            item['total'] = float(item['total'])
    return breakdown

def generate_daily_report(date=None):
    if date is None:
        date = timezone.now().date()
    
    # Get transactions for the day
    transactions = Transaction.objects.filter(
        created_at__date=date
    )
    
    stats = transactions.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id'),
        successful=Count('id', filter=Q(status='completed')),
        failed=Count('id', filter=Q(status='failed')),
        refunded=Count('id', filter=Q(status='refunded')),
        avg_amount=Avg('amount')
    )
    
    # Calculate profits and losses
    completed_transactions = transactions.filter(status='completed')
    refunded_transactions = transactions.filter(status='refunded')
    
    total_profit = completed_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loss = refunded_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    net_revenue = total_profit - total_loss
    
    # Get payment method breakdown
    payment_methods = transactions.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    )
    
    # Convert Decimal values to float for JSON serialization
    payment_methods_list = list(payment_methods)
    for method in payment_methods_list:
        if 'total' in method and method['total'] is not None:
            method['total'] = float(method['total'])
    
    # Create or update the report
    report, created = PaymentReport.objects.update_or_create(
        report_date=date,
        report_type='daily',
        defaults={
            'total_transactions': stats['total_count'] or 0,
            'total_amount': stats['total_amount'] or 0,
            'successful_transactions': stats['successful'] or 0,
            'failed_transactions': stats['failed'] or 0,
            'refunded_transactions': stats['refunded'] or 0,
            'average_transaction_amount': float(stats['avg_amount'] or 0),
            'total_profit': float(total_profit),
            'total_loss': float(total_loss),
            'net_revenue': float(net_revenue),
            'report_data': {
                'payment_methods': payment_methods_list,
                'hourly_breakdown': get_hourly_breakdown(transactions),
                'financial_summary': {
                    'total_profit': float(total_profit),
                    'total_loss': float(total_loss),
                    'net_revenue': float(net_revenue),
                    'total_amount': float(stats['total_amount'] or 0),
                    'average_amount': float(stats['avg_amount'] or 0)
                }
            }
        }
    )
    return report

def generate_weekly_report(date=None):
    if date is None:
        date = timezone.now().date()
    
    # Get start and end of week
    start_date = date - timedelta(days=date.weekday())
    end_date = start_date + timedelta(days=6)
    
    transactions = Transaction.objects.filter(
        created_at__date__range=[start_date, end_date]
    )
    
    stats = transactions.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id'),
        successful=Count('id', filter=Q(status='completed')),
        failed=Count('id', filter=Q(status='failed')),
        refunded=Count('id', filter=Q(status='refunded')),
        avg_amount=Avg('amount')
    )
    
    # Calculate profits and losses
    completed_transactions = transactions.filter(status='completed')
    refunded_transactions = transactions.filter(status='refunded')
    
    total_profit = completed_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loss = refunded_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    net_revenue = total_profit - total_loss
    
    # Daily breakdown for the week
    daily_stats = list(transactions.values('created_at__date').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('created_at__date'))
    
    # Convert Decimal values to float and dates to strings
    for stat in daily_stats:
        if 'total' in stat and stat['total'] is not None:
            stat['total'] = float(stat['total'])
        if 'created_at__date' in stat and stat['created_at__date'] is not None:
            stat['created_at__date'] = stat['created_at__date'].isoformat()
    
    report, created = PaymentReport.objects.update_or_create(
        report_date=start_date,
        report_type='weekly',
        defaults={
            'total_transactions': stats['total_count'] or 0,
            'total_amount': stats['total_amount'] or 0,
            'successful_transactions': stats['successful'] or 0,
            'failed_transactions': stats['failed'] or 0,
            'refunded_transactions': stats['refunded'] or 0,
            'average_transaction_amount': float(stats['avg_amount'] or 0),
            'total_profit': float(total_profit),
            'total_loss': float(total_loss),
            'net_revenue': float(net_revenue),
            'report_data': {
                'daily_breakdown': daily_stats,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'financial_summary': {
                    'total_profit': float(total_profit),
                    'total_loss': float(total_loss),
                    'net_revenue': float(net_revenue),
                    'total_amount': float(stats['total_amount'] or 0),
                    'average_amount': float(stats['avg_amount'] or 0)
                }
            }
        }
    )
    return report

def generate_monthly_report(date=None):
    if date is None:
        date = timezone.now().date()
    
    transactions = Transaction.objects.filter(
        created_at__year=date.year,
        created_at__month=date.month
    )
    
    stats = transactions.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id'),
        successful=Count('id', filter=Q(status='completed')),
        failed=Count('id', filter=Q(status='failed')),
        refunded=Count('id', filter=Q(status='refunded')),
        avg_amount=Avg('amount')
    )
    
    # Calculate profits and losses
    completed_transactions = transactions.filter(status='completed')
    refunded_transactions = transactions.filter(status='refunded')
    
    total_profit = completed_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loss = refunded_transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    net_revenue = total_profit - total_loss
    
    # Weekly breakdown for the month
    weekly_stats = []
    current = date.replace(day=1)
    while current.month == date.month:
        week_end = min(current + timedelta(days=6), date.replace(day=1) + timedelta(days=32))
        if week_end.month != date.month:
            week_end = date.replace(day=1) + timedelta(days=32)
            week_end = week_end.replace(day=1) - timedelta(days=1)
        
        week_transactions = transactions.filter(
            created_at__date__range=[current, week_end]
        )
        week_stats = week_transactions.aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        weekly_stats.append({
            'start_date': current.isoformat(),
            'end_date': week_end.isoformat(),
            'total': float(week_stats['total'] or 0),
            'count': week_stats['count'] or 0
        })
        
        current = week_end + timedelta(days=1)
        if current.month != date.month:
            break
    
    report, created = PaymentReport.objects.update_or_create(
        report_date=date.replace(day=1),
        report_type='monthly',
        defaults={
            'total_transactions': stats['total_count'] or 0,
            'total_amount': stats['total_amount'] or 0,
            'successful_transactions': stats['successful'] or 0,
            'failed_transactions': stats['failed'] or 0,
            'refunded_transactions': stats['refunded'] or 0,
            'average_transaction_amount': float(stats['avg_amount'] or 0),
            'total_profit': float(total_profit),
            'total_loss': float(total_loss),
            'net_revenue': float(net_revenue),
            'report_data': {
                'weekly_breakdown': weekly_stats,
                'month': date.strftime('%B %Y'),
                'financial_summary': {
                    'total_profit': float(total_profit),
                    'total_loss': float(total_loss),
                    'net_revenue': float(net_revenue),
                    'total_amount': float(stats['total_amount'] or 0),
                    'average_amount': float(stats['avg_amount'] or 0)
                }
            }
        }
    )
    return report

def get_latest_reports():
    """Get the most recent daily, weekly, and monthly reports"""
    return {
        'daily': PaymentReport.objects.filter(report_type='daily').order_by('-report_date').first(),
        'weekly': PaymentReport.objects.filter(report_type='weekly').order_by('-report_date').first(),
        'monthly': PaymentReport.objects.filter(report_type='monthly').order_by('-report_date').first()
    }
