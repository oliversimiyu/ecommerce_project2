# Generated by Django 5.0 on 2024-12-07 23:57

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0004_remove_order_orders_orde_status_c6dd84_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
