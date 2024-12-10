from django.shortcuts import render
from django.conf import settings
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from orders.models import Order
from .models import Transaction
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .reports import (
    generate_daily_report, generate_weekly_report,
    generate_monthly_report, get_latest_reports
)

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_transaction(order, payment_method, status='pending', payment_details=None):
    """Helper function to create a transaction record"""
    return Transaction.objects.create(
        transaction_id=str(uuid.uuid4()),
        order=order,
        amount=order.get_total_cost(),
        payment_method=payment_method,
        status=status,
        payment_details=payment_details or {},
        reference_number=f"REF-{timezone.now().strftime('%Y%m%d')}-{order.id}"
    )

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')
        
        if payment_method == 'mpesa':
            # Create a pending transaction for M-Pesa
            transaction = create_transaction(order, 'mpesa')
            # Redirect to M-Pesa payment page
            return redirect(reverse('payment:mpesa_payment'))
        
        # For card payments (Stripe)
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))

        # Create a pending transaction
        transaction = create_transaction(order, 'card')

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(order.get_total_cost() * 100),
                    'product_data': {
                        'name': f'Order {order.id}'
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'transaction_id': transaction.transaction_id,
                'order_id': order.id
            }
        )
        
        # Update transaction with Stripe session ID
        transaction.payment_details = {'stripe_session_id': session.id}
        transaction.save()
        
        return redirect(session.url, code=303)
    
    return render(request, 'payment/process.html', {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
        if event.type == 'checkout.session.completed':
            session = event.data.object
            transaction = Transaction.objects.get(
                payment_details__stripe_session_id=session.id
            )
            # Update transaction status
            transaction.status = 'completed'
            transaction.payment_details.update({
                'stripe_payment_id': session.payment_intent,
                'payment_status': 'paid'
            })
            transaction.save()
            
            # Update order status
            order = transaction.order
            order.paid = True
            order.save()
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'status': 'success'})

def payment_completed(request):
    # Get the latest completed transaction for display
    try:
        order_id = request.session.get('order_id')
        transaction = Transaction.objects.filter(
            order_id=order_id,
            status='completed'
        ).latest('created_at')
        return render(request, 'payment/completed.html', {
            'transaction': transaction
        })
    except Transaction.DoesNotExist:
        return render(request, 'payment/completed.html')

def payment_canceled(request):
    # Update transaction status to failed if exists
    try:
        order_id = request.session.get('order_id')
        transaction = Transaction.objects.filter(
            order_id=order_id,
            status='pending'
        ).latest('created_at')
        transaction.status = 'failed'
        transaction.save()
    except Transaction.DoesNotExist:
        pass
    
    return render(request, 'payment/canceled.html')

def mpesa_payment(request):
    """Handle M-Pesa payment process"""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Here you would integrate with M-Pesa API
        # For now, we'll simulate a successful payment
        transaction = Transaction.objects.filter(
            order_id=order_id,
            status='pending',
            payment_method='mpesa'
        ).latest('created_at')
        
        # Update transaction details
        transaction.status = 'completed'
        transaction.payment_details = {
            'mpesa_receipt': f"MPESA{timezone.now().strftime('%Y%m%d%H%M%S')}",
            'payment_status': 'paid'
        }
        transaction.save()
        
        # Update order status
        order.paid = True
        order.save()
        
        return redirect('payment:completed')
    
    return render(request, 'payment/mpesa.html', {'order': order})

@staff_member_required
def payment_dashboard(request):
    """Dashboard view for payment reports"""
    # Generate latest reports
    daily_report = generate_daily_report()
    weekly_report = generate_weekly_report()
    monthly_report = generate_monthly_report()
    
    return render(request, 'payment/dashboard.html', {
        'daily_report': daily_report,
        'weekly_report': weekly_report,
        'monthly_report': monthly_report
    })

@staff_member_required
def refresh_reports(request):
    """AJAX endpoint to refresh report data"""
    report_type = request.GET.get('type', 'all')
    date_str = request.GET.get('date')
    
    try:
        if date_str:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
            
        if report_type == 'daily':
            report = generate_daily_report(date)
        elif report_type == 'weekly':
            report = generate_weekly_report(date)
        elif report_type == 'monthly':
            report = generate_monthly_report(date)
        else:
            # Generate all reports
            daily = generate_daily_report(date)
            weekly = generate_weekly_report(date)
            monthly = generate_monthly_report(date)
            return JsonResponse({
                'daily': {
                    'total_amount': float(daily.total_amount),
                    'total_transactions': daily.total_transactions,
                    'successful_transactions': daily.successful_transactions,
                    'report_data': daily.report_data
                },
                'weekly': {
                    'total_amount': float(weekly.total_amount),
                    'total_transactions': weekly.total_transactions,
                    'successful_transactions': weekly.successful_transactions,
                    'report_data': weekly.report_data
                },
                'monthly': {
                    'total_amount': float(monthly.total_amount),
                    'total_transactions': monthly.total_transactions,
                    'successful_transactions': monthly.successful_transactions,
                    'report_data': monthly.report_data
                }
            })
            
        return JsonResponse({
            'total_amount': float(report.total_amount),
            'total_transactions': report.total_transactions,
            'successful_transactions': report.successful_transactions,
            'report_data': report.report_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
