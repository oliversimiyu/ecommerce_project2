from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1
    fields = ['product', 'price', 'quantity']
    can_delete = True
    show_change_link = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'total_cost',
                   'paid', 'payment_status', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    list_editable = ['paid']
    list_per_page = 20
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': (('first_name', 'last_name'), 'email')
        }),
        ('Shipping Information', {
            'fields': ('address', ('postal_code', 'city'))
        }),
        ('Order Status', {
            'fields': ('paid',)
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Customer Name'

    def total_cost(self, obj):
        total = obj.get_total_cost()
        formatted_cost = 'KSh {:.2f}'.format(float(total))
        return format_html('<span>{}</span>', formatted_cost)
    total_cost.short_description = 'Total Cost'

    def payment_status(self, obj):
        if obj.paid:
            return format_html('<span style="color: green;">✔ Paid</span>')
        return format_html('<span style="color: red;">✘ Pending</span>')
    payment_status.short_description = 'Payment Status'

    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    class Media:
        css = {
            'all': ('admin/css/order_admin.css',)
        }
        js = ('admin/js/order_admin.js',)
