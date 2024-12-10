from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('mpesa/', views.mpesa_payment, name='mpesa_payment'),
    path('dashboard/', views.payment_dashboard, name='dashboard'),
    path('dashboard/refresh/', views.refresh_reports, name='refresh_reports'),
]
