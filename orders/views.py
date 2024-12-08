from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                       product=item['product'],
                                       price=item['price'],
                                       quantity=item['quantity'])
            cart.clear()
            # Store the order ID in the session
            request.session['order_id'] = order.id
            # Redirect to payment
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(request,
                 'orders/create.html',
                 {'cart': cart, 'form': form})

@login_required
def order_created(request):
    return render(request, 'orders/created.html')
