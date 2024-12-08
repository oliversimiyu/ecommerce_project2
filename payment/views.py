from django.shortcuts import render
from django.conf import settings
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))

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
            cancel_url=cancel_url
        )
        return redirect(session.url, code=303)
    
    return render(request, 'payment/process.html', {'order': order})

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
