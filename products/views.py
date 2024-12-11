from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    sort = request.GET.get('sort', '')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Apply sorting
    if sort == 'name':
        products = products.order_by('name')
    elif sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    
    return render(request,
                 'products/list.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'current_sort': sort})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                 'products/detail.html',
                 {'product': product,
                  'cart_product_form': cart_product_form})

def product_search(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    sort = request.GET.get('sort', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            available=True
        ).distinct()
    else:
        products = Product.objects.filter(available=True)
    
    # Apply sorting
    if sort == 'name':
        products = products.order_by('name')
    elif sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    
    return render(request,
                 'products/list.html',
                 {'products': products,
                  'categories': categories,
                  'search_query': query,
                  'current_sort': sort})
